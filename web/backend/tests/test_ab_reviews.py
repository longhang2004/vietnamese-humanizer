import csv
import json
from pathlib import Path
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.db.database import Base, get_db
from app.main import app


def test_assignment_vote_persists_one_normalized_ballot(client, db_session, monkeypatch):
    monkeypatch.setitem(settings.__dict__, "AB_REVIEW_ENABLED", True)

    response = client.post("/api/ab-review/assignments", json={})

    assert response.status_code == 200
    payload = response.json()
    assignment = payload["assignment"]
    seed = json.loads(
        (Path(__file__).parents[1] / "app/data/ab_review_pilot.json").read_text("utf-8")
    )
    case = next(case for case in seed["cases"] if case["id"] == assignment["case_id"])
    assert {assignment["a"], assignment["b"]} == {case["baseline"], case["with_skills"]}
    assert payload["completed"] == 0
    assert payload["total"] == 6
    assert set(assignment) == {
        "id",
        "case_id",
        "topic",
        "profile",
        "instruction",
        "input_text",
        "a",
        "b",
    }
    vote = {
        "session_id": payload["session_id"],
        "assignment_id": assignment["id"],
        "choice": "a",
        "reasons": ["readability"],
    }

    receipt = client.post("/api/ab-review/votes", json=vote)

    assert receipt.status_code == 200
    assert receipt.json()["completed"] == 1
    retry = client.post("/api/ab-review/votes", json=vote)
    assert retry.json() == receipt.json()
    rows = (
        db_session.execute(
            text(
                "SELECT v.choice, v.winner, v.provenance, a.a_condition, c.baseline, c.with_skills "
                "FROM ab_votes v JOIN ab_assignments a ON a.id = v.assignment_id "
                "JOIN ab_cases c ON c.id = a.case_id"
            )
        )
        .mappings()
        .all()
    )
    assert len(rows) == 1
    assert rows[0]["winner"] == rows[0]["a_condition"]
    assert rows[0]["provenance"] == "anonymous_web"
    assert rows[0]["baseline"] == case["baseline"]
    assert rows[0]["with_skills"] == case["with_skills"]


def test_disabled_review_rejects_before_database_access(client, db_session):
    entered = False

    def tracked_db():
        nonlocal entered
        entered = True
        yield db_session

    app.dependency_overrides[get_db] = tracked_db
    for route in ("assignments", "votes"):
        response = client.post(
            f"/api/ab-review/{route}", content="{", headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 503
    assert entered is False


@pytest.mark.parametrize("a_condition", ["baseline", "with_skills"])
def test_order_is_blind_stable_and_normalized(client, db_session, monkeypatch, a_condition):
    from app.db.models import ABAssignment, ABVote

    monkeypatch.setitem(settings.__dict__, "AB_REVIEW_ENABLED", True)
    monkeypatch.setattr("app.services.ab_reviews.secrets.choice", lambda _: a_condition)
    first = client.post("/api/ab-review/assignments", json={}).json()
    assignment = first["assignment"]
    resumed = client.post(
        "/api/ab-review/assignments", json={"session_id": first["session_id"]}
    ).json()
    assert resumed == first
    assert set(first["study"]) == {"id", "version", "title", "disclosure"}
    stored = db_session.get(ABAssignment, assignment["id"])
    assert stored.a_condition == a_condition
    response = client.post(
        "/api/ab-review/votes",
        json={
            "session_id": first["session_id"],
            "assignment_id": assignment["id"],
            "choice": "b",
            "reasons": ["restraint", "meaning"],
        },
    )
    assert response.status_code == 200
    expected_winner = "with_skills" if a_condition == "baseline" else "baseline"
    assert db_session.query(ABVote).one().winner == expected_winner
    assert "winner" not in response.json()


def test_completion_skip_counts_resume_and_receipts(client, monkeypatch):
    monkeypatch.setitem(settings.__dict__, "AB_REVIEW_ENABLED", True)
    current = client.post("/api/ab-review/assignments", json={}).json()
    first_body = first_receipt = None
    for index in range(6):
        assert current["completed"] == index
        assert current["skipped"] == min(index, 1)
        body = {
            "session_id": current["session_id"],
            "assignment_id": current["assignment"]["id"],
            "choice": "skip" if index == 0 else "tie",
            "reasons": [],
        }
        receipt = client.post("/api/ab-review/votes", json=body)
        assert receipt.status_code == 200
        assert receipt.json()["completed"] == index + 1
        assert receipt.json()["skipped"] == 1
        if index == 0:
            first_body, first_receipt = body, receipt.json()
        current = client.post(
            "/api/ab-review/assignments", json={"session_id": current["session_id"]}
        ).json()
    assert current["assignment"] is None
    assert current["completed"] == current["total"] == 6
    assert current["skipped"] == 1
    assert client.post("/api/ab-review/votes", json=first_body).json() == first_receipt


def test_ownership_conflicting_retry_and_closed_study(client, db_session, monkeypatch):
    from app.db.models import ABStudy

    monkeypatch.setitem(settings.__dict__, "AB_REVIEW_ENABLED", True)
    data = client.post("/api/ab-review/assignments", json={}).json()
    body = {
        "session_id": data["session_id"],
        "assignment_id": data["assignment"]["id"],
        "choice": "a",
        "reasons": [],
    }
    assert (
        client.post("/api/ab-review/votes", json={**body, "session_id": str(uuid4())}).status_code
        == 404
    )
    assert (
        client.post(
            "/api/ab-review/votes", json={**body, "assignment_id": str(uuid4())}
        ).status_code
        == 404
    )
    receipt = client.post("/api/ab-review/votes", json=body)
    assert receipt.status_code == 200
    assert client.post("/api/ab-review/votes", json={**body, "choice": "b"}).status_code == 409
    next_case = client.post(
        "/api/ab-review/assignments", json={"session_id": data["session_id"]}
    ).json()
    study = db_session.get(ABStudy, (data["study"]["id"], data["study"]["version"]))
    study.status = "closed"
    db_session.commit()
    assert client.post("/api/ab-review/assignments", json={}).status_code == 409
    assert (
        client.post(
            "/api/ab-review/votes", json={**body, "assignment_id": next_case["assignment"]["id"]}
        ).status_code
        == 409
    )
    assert client.post("/api/ab-review/votes", json=body).json() == receipt.json()


@pytest.mark.parametrize(
    "changes",
    [
        {"choice": "baseline"},
        {"choice": "with_skills"},
        {"winner": "baseline"},
        {"reasons": ["readability", "readability"]},
        {"reasons": ["unsupported"]},
        {"choice": "skip", "reasons": ["meaning"]},
        {"session_id": "bad"},
        {"assignment_id": "bad"},
        {"reasons": ["meaning"] * 5},
    ],
)
def test_invalid_votes_do_not_persist(client, db_session, monkeypatch, changes):
    from app.db.models import ABVote

    monkeypatch.setitem(settings.__dict__, "AB_REVIEW_ENABLED", True)
    data = client.post("/api/ab-review/assignments", json={}).json()
    body = {
        "session_id": data["session_id"],
        "assignment_id": data["assignment"]["id"],
        "choice": "a",
        "reasons": [],
    }
    assert client.post("/api/ab-review/votes", json={**body, **changes}).status_code == 422
    assert db_session.query(ABVote).count() == 0


@pytest.mark.parametrize("body", [{"session_id": "invalid"}, {"condition": "baseline"}])
def test_assignment_validates_opaque_session_and_extra_fields(client, monkeypatch, body):
    monkeypatch.setitem(settings.__dict__, "AB_REVIEW_ENABLED", True)
    assert client.post("/api/ab-review/assignments", json=body).status_code == 422


def test_seed_drift_rejected_without_overwriting_case(client, db_session, monkeypatch):
    from app.db.models import ABCase
    from app.services import ab_reviews

    monkeypatch.setitem(settings.__dict__, "AB_REVIEW_ENABLED", True)
    data = client.post("/api/ab-review/assignments", json={}).json()
    seed = ab_reviews.load_pilot()
    original = seed["cases"][0]["baseline"]
    seed["cases"][0]["baseline"] = "Changed frozen output"
    monkeypatch.setattr(ab_reviews, "load_pilot", lambda: seed)
    assert client.post("/api/ab-review/assignments", json={}).status_code == 409
    assert (
        db_session.get(ABCase, (data["study"]["id"], 1, seed["cases"][0]["id"])).baseline
        == original
    )


def test_private_summary_export_preserves_metadata_and_excludes_skips(
    client, db_session, monkeypatch, tmp_path, capsys
):
    from app import ab_review_cli

    monkeypatch.setitem(settings.__dict__, "AB_REVIEW_ENABLED", True)
    monkeypatch.setattr("app.services.ab_reviews.secrets.choice", lambda _: "with_skills")
    current = client.post("/api/ab-review/assignments", json={}).json()
    for choice, reasons in [("a", ["meaning"]), ("tie", []), ("skip", [])]:
        response = client.post(
            "/api/ab-review/votes",
            json={
                "session_id": current["session_id"],
                "assignment_id": current["assignment"]["id"],
                "choice": choice,
                "reasons": reasons,
            },
        )
        assert response.status_code == 200
        current = client.post(
            "/api/ab-review/assignments", json={"session_id": current["session_id"]}
        ).json()
    rows = list(ab_review_cli.query_rows(db_session))
    assert len(rows) == 3
    assert rows[0]["a_condition"] == "with_skills"
    assert rows[0]["b_condition"] == "baseline"
    assert rows[0]["winner"] == "with_skills"
    assert rows[0]["provenance"] == "anonymous_web"
    assert (
        rows[0]["source"]["modelVersion"]
        == "Exact provider version is not exposed by the subagent tool"
    )
    assert len(rows[0]["study_snapshot_hash"]) == len(rows[0]["case_hash"]) == 64
    summary = ab_review_cli.summarize(rows)
    assert summary["total"] == 3
    assert summary["skipped"] == summary["ties"] == 1
    assert summary["preference_denominator"] == 2
    assert summary["preference_rates"] == {"baseline": 0.0, "with_skills": 0.5, "tie": 0.5}
    assert summary["choices"] == {"a": 1, "b": 0, "tie": 1, "skip": 1}
    assert summary["reasons"] == {"meaning": 1}
    assert len(list(ab_review_cli.query_rows(db_session, profile="business"))) == 1
    assert not list(ab_review_cli.query_rows(db_session, model="unrecorded model"))
    assert not list(ab_review_cli.query_rows(db_session, since="2999-01-01T00:00:00Z"))
    monkeypatch.setattr(ab_review_cli, "SessionLocal", lambda: db_session)
    output = tmp_path / "votes.jsonl"
    assert ab_review_cli.main(["export", "--format", "jsonl", "--output", str(output)]) == 0
    exported = [json.loads(line) for line in output.read_text("utf-8").splitlines()]
    assert exported == rows
    csv_output = tmp_path / "votes.csv"
    assert ab_review_cli.main(["export", "--format", "csv", "--output", str(csv_output)]) == 0
    with csv_output.open(encoding="utf-8", newline="") as stream:
        csv_rows = list(csv.DictReader(stream))
    assert len(csv_rows) == 3
    assert csv_rows[0]["baseline"] == rows[0]["baseline"]
    assert json.loads(csv_rows[0]["source"]) == rows[0]["source"]
    assert ab_review_cli.main(["summary", "--profile", "business"]) == 0
    assert json.loads(capsys.readouterr().out)["total"] == 1
    assert (
        ab_review_cli.main(["close-study", "--study", current["study"]["id"], "--version", "1"])
        == 0
    )
    assert client.post("/api/ab-review/assignments", json={}).status_code == 409
    assert ab_review_cli.summarize([])["preference_rates"] == {
        "baseline": None,
        "with_skills": None,
        "tie": None,
    }


def test_no_public_admin_or_export_route(client, monkeypatch):
    monkeypatch.setitem(settings.__dict__, "AB_REVIEW_ENABLED", True)
    for path in ("export", "summary", "close-study"):
        assert client.get(f"/api/ab-review/{path}").status_code == 404


def test_real_sqlite_persistence_and_concurrent_retries(tmp_path):
    from concurrent.futures import ThreadPoolExecutor

    from app.db.models import ABAssignment, ABCase, ABVote
    from app.schemas import ABVoteRequest
    from app.services.ab_reviews import assign_case, submit_vote

    engine = create_engine(
        f"sqlite:///{tmp_path / 'reviews.db'}", connect_args={"check_same_thread": False}
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, record):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    session_id = str(uuid4())

    def assign(_):
        with sessions() as db:
            return assign_case(db, session_id)

    try:
        with ThreadPoolExecutor(max_workers=4) as executor:
            assignments = list(executor.map(assign, range(4)))
        ids = {item["assignment"]["id"] for item in assignments}
        assert len(ids) == 1
        body = ABVoteRequest(session_id=session_id, assignment_id=ids.pop(), choice="a")

        def vote(_):
            with sessions() as db:
                return submit_vote(db, body)

        with ThreadPoolExecutor(max_workers=4) as executor:
            receipts = list(executor.map(vote, range(4)))
        assert all(receipt == receipts[0] for receipt in receipts)
        with sessions() as db:
            assert db.query(ABAssignment).count() == db.query(ABVote).count() == 1
            assert db.query(ABCase).count() == 6
        engine.dispose()
        with sessions() as db:
            assert db.query(ABVote).one().id == receipts[0]["id"]
    finally:
        engine.dispose()


def test_study_closure_refreshes_an_already_loaded_snapshot(tmp_path):
    from fastapi import HTTPException

    from app.db.models import ABStudy
    from app.services.ab_reviews import assign_case, seed_pilot

    engine = create_engine(f"sqlite:///{tmp_path / 'closed.db'}")
    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    try:
        with sessions() as first:
            study = seed_pilot(first)
            key = (study.id, study.version)
            assert study.status == "open"
            with sessions() as second:
                second.get(ABStudy, key).status = "closed"
                second.commit()
            with pytest.raises(HTTPException) as error:
                assign_case(first, str(uuid4()))
            assert error.value.status_code == 409
    finally:
        engine.dispose()


@pytest.mark.parametrize("operation", ["vote", "assignment"])
def test_sqlite_close_waits_for_inflight_review_commit(tmp_path, monkeypatch, operation):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event, current_thread

    from app import ab_review_cli
    from app.db.models import ABAssignment, ABStudy, ABVote
    from app.schemas import ABVoteRequest
    from app.services import ab_reviews

    engine = create_engine(
        f"sqlite:///{tmp_path / 'overlapping-close.db'}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    session_id = str(uuid4())
    with sessions() as db:
        allocated = ab_reviews.assign_case(db, session_id)
    key = (allocated["study"]["id"], allocated["study"]["version"])
    body = ABVoteRequest(
        session_id=session_id, assignment_id=allocated["assignment"]["id"], choice="a"
    )
    checked_open = Event()
    finish_review = Event()
    close_attempted = Event()
    close_returned = Event()

    def pause_review():
        checked_open.set()
        assert finish_review.wait(timeout=10)

    if operation == "vote":
        original_progress = ab_reviews.progress

        def paused_progress(*args):
            if current_thread().name.startswith("inflight-review"):
                pause_review()
            return original_progress(*args)

        monkeypatch.setattr(ab_reviews, "progress", paused_progress)
    else:
        original_choice = ab_reviews.secrets.choice

        def paused_choice(options):
            pause_review()
            return original_choice(options)

        monkeypatch.setattr(ab_reviews.secrets, "choice", paused_choice)

    @event.listens_for(engine, "before_cursor_execute")
    def record_close_attempt(connection, cursor, statement, parameters, context, many):
        if current_thread().name.startswith("close-study") and statement.startswith("UPDATE"):
            close_attempted.set()

    monkeypatch.setattr(ab_review_cli, "SessionLocal", sessions)

    def review():
        with sessions() as db:
            if operation == "vote":
                return ab_reviews.submit_vote(db, body)
            return ab_reviews.assign_case(db, str(uuid4()))

    def close():
        result = ab_review_cli.main(["close-study", "--study", key[0], "--version", str(key[1])])
        close_returned.set()
        return result

    try:
        with (
            ThreadPoolExecutor(max_workers=1, thread_name_prefix="inflight-review") as reviews,
            ThreadPoolExecutor(max_workers=1, thread_name_prefix="close-study") as closes,
        ):
            pending_review = reviews.submit(review)
            assert checked_open.wait(timeout=10)
            pending_close = closes.submit(close)
            try:
                assert close_attempted.wait(timeout=10)
                assert not close_returned.wait(timeout=1), "Close returned before the review commit"
            finally:
                finish_review.set()
            result = pending_review.result(timeout=10)
            assert pending_close.result(timeout=10) == 0
        with sessions() as db:
            assert db.get(ABStudy, key).status == "closed"
            if operation == "vote":
                assert db.query(ABVote).count() == 1
                assert ab_reviews.submit_vote(db, body) == result
            else:
                assert db.query(ABAssignment).count() == 2
    finally:
        finish_review.set()
        engine.dispose()


def test_assignment_race_before_study_lock_keeps_one_active_case(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event, current_thread

    from app.db.models import ABAssignment
    from app.services import ab_reviews

    engine = create_engine(
        f"sqlite:///{tmp_path / 'allocation-race.db'}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    waiting_for_lock = Event()
    earlier_request_finished = Event()
    session_id = str(uuid4())
    with sessions() as db:
        ab_reviews.seed_pilot(db)

    original_locked_study = ab_reviews.locked_study

    def delay_study_lock(*args):
        if current_thread().name.startswith("late-request") and not waiting_for_lock.is_set():
            waiting_for_lock.set()
            assert earlier_request_finished.wait(timeout=10)
        return original_locked_study(*args)

    monkeypatch.setattr(ab_reviews, "locked_study", delay_study_lock)

    def late_request():
        with sessions() as db:
            return ab_reviews.assign_case(db, session_id)

    try:
        with ThreadPoolExecutor(max_workers=1, thread_name_prefix="late-request") as executor:
            late = executor.submit(late_request)
            assert waiting_for_lock.wait(timeout=10)
            try:
                with sessions() as db:
                    earlier = ab_reviews.assign_case(db, session_id)
            finally:
                earlier_request_finished.set()
            assert late.result()["assignment"] == earlier["assignment"]
        with sessions() as db:
            assert db.query(ABAssignment).count() == 1
    finally:
        earlier_request_finished.set()
        engine.dispose()


def test_review_routes_are_rate_limited(client, monkeypatch):
    from app.limiter import limiter

    monkeypatch.setitem(settings.__dict__, "AB_REVIEW_ENABLED", True)
    limiter.enabled = True
    for _ in range(30):
        assert client.post("/api/ab-review/assignments", json={}).status_code == 200
    assert client.post("/api/ab-review/assignments", json={}).status_code == 429
