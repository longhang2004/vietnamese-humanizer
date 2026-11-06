"""Private, database-authorized A/B review queries. No HTTP administration surface."""

import argparse
import csv
import json
import sys
from collections import Counter
from contextlib import nullcontext
from datetime import UTC, datetime

from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.db.database import Base, SessionLocal, engine
from app.db.models import ABAssignment, ABCase, ABStudy, ABVote, utc_now
from app.services.ab_reviews import json_text, locked_study, seed_pilot

EXPORT_FIELDS = (
    "vote_id",
    "voted_at",
    "provenance",
    "study_id",
    "study_version",
    "study_title",
    "study_status",
    "study_provenance",
    "study_snapshot_hash",
    "source",
    "case_id",
    "case_hash",
    "topic",
    "profile",
    "instruction",
    "input_text",
    "baseline",
    "with_skills",
    "case_metadata",
    "session_id",
    "assignment_id",
    "assigned_at",
    "a_condition",
    "b_condition",
    "choice",
    "winner",
    "reasons",
)


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    # SQLAlchemy's existing DateTime convention stores UTC without a timezone.
    return parsed.astimezone(UTC).replace(tzinfo=None)


def iso_utc(value: datetime) -> str:
    return value.replace(tzinfo=UTC).isoformat()


def query_rows(
    db: Session,
    *,
    study_id: str | None = None,
    version: int | None = None,
    topic: str | None = None,
    profile: str | None = None,
    model: str | None = None,
    skill_commit: str | None = None,
    since: str | None = None,
    until: str | None = None,
):
    query = (
        db.query(ABVote, ABAssignment, ABCase, ABStudy)
        .join(ABAssignment, ABVote.assignment_id == ABAssignment.id)
        .join(
            ABCase,
            and_(
                ABAssignment.study_id == ABCase.study_id,
                ABAssignment.study_version == ABCase.study_version,
                ABAssignment.case_id == ABCase.id,
            ),
        )
        .join(
            ABStudy,
            and_(
                ABCase.study_id == ABStudy.id,
                ABCase.study_version == ABStudy.version,
            ),
        )
    )
    for value, column in (
        (study_id, ABStudy.id),
        (version, ABStudy.version),
        (topic, ABCase.topic),
        (profile, ABCase.profile),
    ):
        if value is not None:
            query = query.filter(column == value)
    if since:
        query = query.filter(ABVote.created_at >= parse_time(since))
    if until:
        query = query.filter(ABVote.created_at < parse_time(until))
    for vote, assignment, case, study in query.order_by(ABVote.created_at, ABVote.id):
        source = json.loads(study.source)
        if model is not None and source.get("modelVersion") != model:
            continue
        if skill_commit is not None and source.get("skillCommit") != skill_commit:
            continue
        yield {
            "vote_id": vote.id,
            "voted_at": iso_utc(vote.created_at),
            "provenance": vote.provenance,
            "study_id": study.id,
            "study_version": study.version,
            "study_title": study.title,
            "study_status": study.status,
            "study_provenance": study.provenance,
            "study_snapshot_hash": study.snapshot_hash,
            "source": source,
            "case_id": case.id,
            "case_hash": case.content_hash,
            "topic": case.topic,
            "profile": case.profile,
            "instruction": case.instruction,
            "input_text": case.input_text,
            "baseline": case.baseline,
            "with_skills": case.with_skills,
            "case_metadata": json.loads(case.case_metadata),
            "session_id": assignment.session_id,
            "assignment_id": assignment.id,
            "assigned_at": iso_utc(assignment.created_at),
            "a_condition": assignment.a_condition,
            "b_condition": "with_skills" if assignment.a_condition == "baseline" else "baseline",
            "choice": vote.choice,
            "winner": vote.winner,
            "reasons": json.loads(vote.reasons),
        }


def summarize(rows) -> dict:
    rows = list(rows)
    choices = Counter(row["choice"] for row in rows)
    winners = Counter(row["winner"] for row in rows)
    denominator = len(rows) - choices["skip"]
    positions = {}
    for condition in ("baseline", "with_skills"):
        first = [row for row in rows if row["a_condition"] == condition]
        counts = Counter(row["choice"] for row in first)
        positions[condition] = {
            "total": len(first),
            **{choice: counts[choice] for choice in ("a", "b", "tie", "skip")},
        }
    return {
        "total": len(rows),
        "anonymous_sessions": len({row["session_id"] for row in rows}),
        "skipped": choices["skip"],
        "ties": choices["tie"],
        "preference_denominator": denominator,
        "choices": {choice: choices[choice] for choice in ("a", "b", "tie", "skip")},
        "winners": {
            winner: winners[winner] for winner in ("baseline", "with_skills", "tie", "skip")
        },
        "preference_rates": {
            winner: winners[winner] / denominator if denominator else None
            for winner in ("baseline", "with_skills", "tie")
        },
        "reasons": dict(Counter(reason for row in rows for reason in row["reasons"])),
        "a_position": positions,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("seed", help="Create tables and freeze the bundled pilot idempotently")
    close = commands.add_parser("close-study", help="Stop new assignments and ballots")
    close.add_argument("--study", required=True)
    close.add_argument("--version", required=True, type=int)
    export = commands.add_parser("export", help="Export private ballots with frozen snapshots")
    export.add_argument("--format", choices=("csv", "jsonl"), default="jsonl")
    export.add_argument("--output", default="-", help="Output path; defaults to stdout")
    summary = commands.add_parser(
        "summary", help="Count choices, ties, skips and presentation order"
    )
    for command in (export, summary):
        command.add_argument("--study", dest="study_id")
        command.add_argument("--version", type=int)
        command.add_argument("--topic")
        command.add_argument("--profile")
        command.add_argument(
            "--model", help="Exact recorded modelVersion, including unknown wording"
        )
        command.add_argument("--skill-commit")
        command.add_argument("--since", help="Inclusive ISO UTC ballot time")
        command.add_argument("--until", help="Exclusive ISO UTC ballot time")
    args = parser.parse_args(argv)
    with SessionLocal() as db:
        if args.command == "seed":
            Base.metadata.create_all(engine)
            seed_pilot(db)
            return 0
        if args.command == "close-study":
            try:
                study = locked_study(db, args.study, args.version)
            except NoResultFound:
                parser.error("Study/version not found.")
            study.status = "closed"
            study.closed_at = study.closed_at or utc_now()
            db.commit()
            return 0
        filters = {
            key: getattr(args, key)
            for key in (
                "study_id",
                "version",
                "topic",
                "profile",
                "model",
                "skill_commit",
                "since",
                "until",
            )
        }
        try:
            rows = list(query_rows(db, **filters))
        except ValueError as exc:
            parser.error(str(exc))
        if args.command == "summary":
            print(json.dumps(summarize(rows), ensure_ascii=False, indent=2))
            return 0
        with (
            nullcontext(sys.stdout)
            if args.output == "-"
            else open(args.output, "w", encoding="utf-8", newline="")
        ) as output:
            if args.format == "jsonl":
                for row in rows:
                    output.write(json_text(row) + "\n")
            else:
                writer = csv.DictWriter(output, fieldnames=EXPORT_FIELDS)
                writer.writeheader()
                for row in rows:
                    writer.writerow(
                        {
                            key: json_text(value) if isinstance(value, (dict, list)) else value
                            for key, value in row.items()
                        }
                    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
