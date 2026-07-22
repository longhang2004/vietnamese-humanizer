from fastapi import APIRouter, Depends, HTTPException, Request

from app.capabilities import capability_route_class, require_rewrite_enabled
from app.limiter import limiter
from app.schemas import VALID_SKILLS, RewriteRequest, RewriteResponse
from app.services.rewriter import GeminiKeyMissingError, generate_rewrite

router = APIRouter(
    prefix="/api",
    tags=["Rewrite"],
    route_class=capability_route_class(require_rewrite_enabled),
)


@router.post(
    "/rewrite",
    response_model=RewriteResponse,
    dependencies=[Depends(require_rewrite_enabled)],
)
@limiter.limit("5/minute")
def rewrite_endpoint(request: Request, body: RewriteRequest):
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Văn bản không được để trống.")

    if body.skill not in VALID_SKILLS:
        raise HTTPException(
            status_code=400,
            detail=f"Kỹ năng không hợp lệ: {body.skill}. Các kỹ năng hợp lệ: {', '.join(sorted(VALID_SKILLS))}",
        )

    try:
        return generate_rewrite(text=body.text, skill=body.skill, issue_ids=body.issue_ids)
    except GeminiKeyMissingError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Không thể xử lý yêu cầu viết lại.",
        ) from None
