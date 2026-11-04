from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.capabilities import capability_route_class, require_contributions_enabled
from app.db.database import get_db
from app.limiter import limiter
from app.schemas import VALID_SKILLS, ContributionCreate, ContributionResponse
from app.services.contributions import create_contribution

router = APIRouter(
    prefix="/api",
    tags=["Contributions"],
    route_class=capability_route_class(require_contributions_enabled),
)


@router.post(
    "/contributions",
    response_model=ContributionResponse,
)
@limiter.limit("3/minute")
def submit_contribution(request: Request, body: ContributionCreate, db: Session = Depends(get_db)):
    if not body.consent:
        raise HTTPException(
            status_code=400,
            detail="Bạn cần xác nhận quyền chia sẻ văn bản trước khi gửi ví dụ.",
        )

    if body.skill not in VALID_SKILLS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Kỹ năng không hợp lệ: {body.skill}. "
                f"Các kỹ năng hợp lệ: {', '.join(sorted(VALID_SKILLS))}"
            ),
        )

    contrib = create_contribution(db, body)
    return ContributionResponse(
        id=contrib.id,
        status=contrib.status,
        message="Đã nhận ví dụ của bạn. Nhóm duy trì sẽ xem xét trước khi thêm vào bộ dữ liệu.",
    )
