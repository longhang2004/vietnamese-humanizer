from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.capabilities import capability_route_class, require_ab_review_enabled
from app.db.database import get_db
from app.limiter import limiter
from app.schemas import (
    ABAssignmentRequest,
    ABAssignmentResponse,
    ABVoteRequest,
    ABVoteResponse,
)
from app.services.ab_reviews import assign_case, submit_vote

router = APIRouter(
    prefix="/api/ab-review",
    tags=["A/B review"],
    route_class=capability_route_class(require_ab_review_enabled),
)


@router.post("/assignments", response_model=ABAssignmentResponse)
@limiter.limit("30/minute")
def assignment(request: Request, body: ABAssignmentRequest, db: Session = Depends(get_db)):
    return assign_case(db, str(body.session_id) if body.session_id else None)


@router.post("/votes", response_model=ABVoteResponse)
@limiter.limit("20/minute")
def vote(request: Request, body: ABVoteRequest, db: Session = Depends(get_db)):
    return submit_vote(db, body)
