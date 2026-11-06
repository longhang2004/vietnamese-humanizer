import hashlib
import json
import secrets
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import ABAssignment, ABCase, ABStudy, ABVote
from app.schemas import ABVoteRequest

PILOT_PATH = Path(__file__).resolve().parents[1] / "data/ab_review_pilot.json"
VOTE_MESSAGE = "Đã lưu lựa chọn của bạn."


def json_text(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def snapshot_hash(value) -> str:
    return hashlib.sha256(json_text(value).encode("utf-8")).hexdigest()


def load_pilot() -> dict:
    return json.loads(PILOT_PATH.read_text(encoding="utf-8"))


def seed_pilot(db: Session) -> ABStudy:
    """Freeze a version once; never update its cases from a changed source file."""
    payload = load_pilot()
    source = payload["study"]
    key = (source["id"], source["version"])
    digest = snapshot_hash(payload)
    study = db.get(ABStudy, key)
    if study is None:
        study = ABStudy(
            id=source["id"],
            version=source["version"],
            title=source["title"],
            disclosure=source["disclosure"],
            provenance=source["provenance"],
            source=json_text(source["source"]),
            snapshot_hash=digest,
        )
        db.add(study)
        try:
            # Persist the parent first: these snapshot models have no ORM relationships.
            db.flush()
            for index, case in enumerate(payload["cases"]):
                db.add(
                    ABCase(
                        study_id=source["id"],
                        study_version=source["version"],
                        id=case["id"],
                        position=index,
                        topic=case["topic"],
                        profile=case["profile"],
                        instruction=case["instruction"],
                        input_text=case["input_text"],
                        baseline=case["baseline"],
                        with_skills=case["with_skills"],
                        case_metadata=json_text(case["metadata"]),
                        content_hash=snapshot_hash(case),
                    )
                )
            db.commit()
        except IntegrityError:
            # Another worker may have committed this exact study while we seeded it.
            db.rollback()
        study = db.get(ABStudy, key)
    if study is None or study.snapshot_hash != digest:
        raise HTTPException(409, "Nội dung đợt chấm đã thay đổi; cần tạo phiên bản mới.")
    return study


def study_cases(db: Session, study: ABStudy):
    return db.query(ABCase).filter_by(study_id=study.id, study_version=study.version)


def session_votes(db: Session, study: ABStudy, session_id: str):
    return (
        db.query(ABVote)
        .join(ABAssignment)
        .filter(
            ABAssignment.study_id == study.id,
            ABAssignment.study_version == study.version,
            ABAssignment.session_id == session_id,
        )
    )


def progress(db: Session, study: ABStudy, session_id: str) -> dict:
    votes = session_votes(db, study, session_id)
    return {
        "completed": votes.count(),
        "total": study_cases(db, study).count(),
        "skipped": votes.filter(ABVote.choice == "skip").count(),
    }


def require_open(study: ABStudy) -> None:
    if study.status != "open":
        raise HTTPException(409, "Đợt chấm này đã đóng.")


def locked_study(db: Session, study_id: str, version: int) -> ABStudy:
    query = db.query(ABStudy).filter_by(id=study_id, version=version)
    if db.get_bind().dialect.name == "sqlite":
        # SQLite ignores FOR UPDATE. A no-op write holds its transaction's write
        # lock until commit/rollback, serializing close with the final review write.
        query.update({ABStudy.status: ABStudy.status}, synchronize_session=False)
    return query.populate_existing().with_for_update().one()


def assign_case(db: Session, session_id: str | None) -> dict:
    study = seed_pilot(db)
    study = locked_study(db, study.id, study.version)
    require_open(study)
    session_id = session_id or str(uuid4())
    assignments = db.query(ABAssignment).filter_by(
        study_id=study.id, study_version=study.version, session_id=session_id
    )
    assignment = assignments.outerjoin(ABVote).filter(ABVote.id.is_(None)).first()
    if assignment is None:
        assigned = assignments.with_entities(ABAssignment.case_id)
        case = (
            study_cases(db, study)
            .filter(ABCase.id.not_in(assigned))
            .order_by(ABCase.position)
            .first()
        )
        if case is not None:
            assignment = ABAssignment(
                session_id=session_id,
                study_id=study.id,
                study_version=study.version,
                case_id=case.id,
                a_condition=secrets.choice(["baseline", "with_skills"]),
            )
            db.add(assignment)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                # A competing request may have chosen this or the next case after
                # our first read. Re-read its unique active slot after rollback.
                return assign_case(db, session_id)
    public_assignment = None
    if assignment is not None:
        case = db.get(ABCase, (study.id, study.version, assignment.case_id))
        b_condition = "with_skills" if assignment.a_condition == "baseline" else "baseline"
        public_assignment = {
            "id": assignment.id,
            "case_id": case.id,
            "topic": case.topic,
            "profile": case.profile,
            "instruction": case.instruction,
            "input_text": case.input_text,
            "a": getattr(case, assignment.a_condition),
            "b": getattr(case, b_condition),
        }
    return {
        "session_id": session_id,
        "study": {
            "id": study.id,
            "version": study.version,
            "title": study.title,
            "disclosure": study.disclosure,
        },
        "assignment": public_assignment,
        **progress(db, study, session_id),
    }


def vote_receipt(vote: ABVote) -> dict:
    return {
        "id": vote.id,
        "message": VOTE_MESSAGE,
        "completed": vote.receipt_completed,
        "total": vote.receipt_total,
        "skipped": vote.receipt_skipped,
    }


def check_retry(vote: ABVote, body: ABVoteRequest, reasons: str) -> dict:
    if vote.choice != body.choice or vote.reasons != reasons:
        raise HTTPException(409, "Lượt chấm này đã có một lựa chọn khác.")
    return vote_receipt(vote)


def submit_vote(db: Session, body: ABVoteRequest) -> dict:
    assignment = db.get(ABAssignment, str(body.assignment_id))
    if assignment is None or assignment.session_id != str(body.session_id):
        raise HTTPException(404, "Không tìm thấy lượt chấm trong phiên này.")
    reasons = json_text(sorted(body.reasons))
    study = locked_study(db, assignment.study_id, assignment.study_version)
    existing = db.query(ABVote).filter_by(assignment_id=assignment.id).first()
    if existing is not None:
        return check_retry(existing, body, reasons)
    require_open(study)
    counts = progress(db, study, assignment.session_id)
    winner = body.choice
    if body.choice == "a":
        winner = assignment.a_condition
    elif body.choice == "b":
        winner = "with_skills" if assignment.a_condition == "baseline" else "baseline"
    vote = ABVote(
        assignment_id=assignment.id,
        choice=body.choice,
        winner=winner,
        reasons=reasons,
        provenance="anonymous_web",
        receipt_completed=counts["completed"] + 1,
        receipt_total=counts["total"],
        receipt_skipped=counts["skipped"] + (body.choice == "skip"),
    )
    db.add(vote)
    assignment.active_slot = None
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.query(ABVote).filter_by(assignment_id=assignment.id).one()
        return check_retry(existing, body, reasons)
    db.refresh(vote)
    return vote_receipt(vote)
