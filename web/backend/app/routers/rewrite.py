from fastapi import APIRouter, HTTPException, Request

from app.limiter import limiter
from app.schemas import VALID_SKILLS, RewriteRequest, RewriteResponse
from app.services.rewriter import GeminiKeyMissingError, generate_rewrite

router = APIRouter(prefix="/api", tags=["Rewrite"])


@router.post("/rewrite", response_model=RewriteResponse)
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý Gemini: {e!s}")
