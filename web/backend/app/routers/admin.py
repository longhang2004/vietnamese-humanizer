import json
import secrets

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from app.capabilities import require_admin_enabled
from app.config import settings
from app.db.database import get_db
from app.schemas import AdminContributionItem, AdminContributionPatch
from app.services.contributions import (
    export_approved_contributions,
    get_contributions_by_status,
    update_contribution_status,
)

router = APIRouter(prefix="/api/admin", tags=["Admin"])


def verify_admin_key(x_admin_key: str | None = Header(None, alias="X-Admin-Key")):
    admin_key = settings.ADMIN_API_KEY
    if not x_admin_key or not admin_key or not secrets.compare_digest(x_admin_key, admin_key):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: X-Admin-Key header missing or invalid.",
        )


@router.get(
    "/contributions",
    response_model=list[AdminContributionItem],
    dependencies=[Depends(require_admin_enabled), Depends(verify_admin_key)],
)
def list_contributions_admin(
    status: str = Query("pending"),
    db: Session = Depends(get_db),
):
    contributions = get_contributions_by_status(db, status=status)
    items = []
    for c in contributions:
        pids = json.loads(c.pattern_ids) if c.pattern_ids else None
        items.append(
            AdminContributionItem(
                id=c.id,
                created_at=c.created_at.isoformat() if c.created_at else "",
                input_text=c.input_text,
                context=c.context,
                suggestion=c.suggestion,
                skill=c.skill,
                pattern_ids=pids,
                note=c.note,
                consent=c.consent,
                status=c.status,
                review_note=c.review_note,
                reviewed_at=c.reviewed_at.isoformat() if c.reviewed_at else None,
            )
        )
    return items


@router.patch(
    "/contributions/{contrib_id}",
    response_model=AdminContributionItem,
    dependencies=[Depends(require_admin_enabled), Depends(verify_admin_key)],
)
def patch_contribution_admin(
    contrib_id: str,
    body: AdminContributionPatch,
    db: Session = Depends(get_db),
):
    if body.status not in ("approved", "rejected", "pending"):
        raise HTTPException(status_code=400, detail="Trạng thái không hợp lệ.")

    updated = update_contribution_status(
        db, contrib_id=contrib_id, status=body.status, review_note=body.review_note
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Không tìm thấy đóng góp.")

    pids = json.loads(updated.pattern_ids) if updated.pattern_ids else None
    return AdminContributionItem(
        id=updated.id,
        created_at=updated.created_at.isoformat() if updated.created_at else "",
        input_text=updated.input_text,
        context=updated.context,
        suggestion=updated.suggestion,
        skill=updated.skill,
        pattern_ids=pids,
        note=updated.note,
        consent=updated.consent,
        status=updated.status,
        review_note=updated.review_note,
        reviewed_at=updated.reviewed_at.isoformat() if updated.reviewed_at else None,
    )


@router.get(
    "/contributions/export",
    dependencies=[Depends(require_admin_enabled), Depends(verify_admin_key)],
)
def export_contributions_admin(
    status: str = Query("approved"),
    db: Session = Depends(get_db),
):
    if status != "approved":
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ export status='approved'.")
    return export_approved_contributions(db)
