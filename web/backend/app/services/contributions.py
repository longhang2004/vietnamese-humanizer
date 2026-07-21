import json

from sqlalchemy.orm import Session

from app.db.models import Contribution, utc_now
from app.schemas import ContributionCreate


def create_contribution(db: Session, data: ContributionCreate) -> Contribution:
    pattern_ids_json = json.dumps(data.pattern_ids) if data.pattern_ids else None
    contrib = Contribution(
        input_text=data.input_text,
        context=data.context,
        suggestion=data.suggestion,
        skill=data.skill,
        pattern_ids=pattern_ids_json,
        note=data.note,
        consent=data.consent,
        status="pending",
    )
    db.add(contrib)
    db.commit()
    db.refresh(contrib)
    return contrib


def get_contributions_by_status(db: Session, status: str = "pending") -> list[Contribution]:
    return db.query(Contribution).filter(Contribution.status == status).order_by(Contribution.created_at.desc()).all()


def update_contribution_status(
    db: Session, contrib_id: str, status: str, review_note: str | None = None
) -> Contribution | None:
    contrib = db.query(Contribution).filter(Contribution.id == contrib_id).first()
    if not contrib:
        return None
    contrib.status = status
    contrib.review_note = review_note
    contrib.reviewed_at = utc_now()
    db.commit()
    db.refresh(contrib)
    return contrib


def export_approved_contributions(db: Session) -> list[dict]:
    approved = db.query(Contribution).filter(Contribution.status == "approved").all()
    results = []
    for c in approved:
        pids = json.loads(c.pattern_ids) if c.pattern_ids else []
        results.append({
            "id": c.id,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "input_text": c.input_text,
            "context": c.context,
            "suggestion": c.suggestion,
            "skill": c.skill,
            "pattern_ids": pids,
            "note": c.note,
            "status": c.status,
            "review_note": c.review_note,
            "reviewed_at": c.reviewed_at.isoformat() if c.reviewed_at else None,
        })
    return results
