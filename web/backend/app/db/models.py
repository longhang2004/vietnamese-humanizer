import uuid
from datetime import UTC, datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class Contribution(Base):
    __tablename__ = "contributions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    input_text: Mapped[str] = mapped_column(Text, nullable=False)
    context: Mapped[str | None] = mapped_column(Text, nullable=True)
    suggestion: Mapped[str] = mapped_column(Text, nullable=False)
    skill: Mapped[str] = mapped_column(String(100), nullable=False)
    pattern_ids: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON string
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    consent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    review_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ABStudy(Base):
    __tablename__ = "ab_studies"
    __table_args__ = (CheckConstraint("status IN ('open', 'closed')"),)

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    version: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    disclosure: Mapped[str] = mapped_column(Text)
    provenance: Mapped[str] = mapped_column(String(100))
    source: Mapped[str] = mapped_column(Text)  # frozen JSON source metadata
    snapshot_hash: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(20), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ABCase(Base):
    __tablename__ = "ab_cases"
    __table_args__ = (
        ForeignKeyConstraint(
            ["study_id", "study_version"], ["ab_studies.id", "ab_studies.version"]
        ),
    )

    study_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    study_version: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    position: Mapped[int] = mapped_column(Integer)
    topic: Mapped[str] = mapped_column(Text)
    profile: Mapped[str] = mapped_column(String(100))
    instruction: Mapped[str] = mapped_column(Text)
    input_text: Mapped[str] = mapped_column(Text)
    baseline: Mapped[str] = mapped_column(Text)
    with_skills: Mapped[str] = mapped_column(Text)
    case_metadata: Mapped[str] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(String(64))


class ABAssignment(Base):
    __tablename__ = "ab_assignments"
    __table_args__ = (
        ForeignKeyConstraint(
            ["study_id", "study_version", "case_id"],
            ["ab_cases.study_id", "ab_cases.study_version", "ab_cases.id"],
        ),
        UniqueConstraint("session_id", "study_id", "study_version", "case_id"),
        UniqueConstraint("session_id", "study_id", "study_version", "active_slot"),
        CheckConstraint("a_condition IN ('baseline', 'with_skills')"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(String(36), index=True)
    study_id: Mapped[str] = mapped_column(String(100))
    study_version: Mapped[int] = mapped_column(Integer)
    case_id: Mapped[str] = mapped_column(String(100))
    a_condition: Mapped[str] = mapped_column(String(20))
    # One true slot per session/version; completed assignments use SQL NULL.
    active_slot: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ABVote(Base):
    __tablename__ = "ab_votes"
    __table_args__ = (
        CheckConstraint("choice IN ('a', 'b', 'tie', 'skip')"),
        CheckConstraint("winner IN ('baseline', 'with_skills', 'tie', 'skip')"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    assignment_id: Mapped[str] = mapped_column(ForeignKey("ab_assignments.id"), unique=True)
    choice: Mapped[str] = mapped_column(String(10))
    winner: Mapped[str] = mapped_column(String(20))
    reasons: Mapped[str] = mapped_column(Text)
    provenance: Mapped[str] = mapped_column(String(100), default="anonymous_web")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    receipt_completed: Mapped[int] = mapped_column(Integer)
    receipt_total: Mapped[int] = mapped_column(Integer)
    receipt_skipped: Mapped[int] = mapped_column(Integer)
