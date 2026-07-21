from fastapi import APIRouter, HTTPException, Request

from app.limiter import limiter
from app.schemas import VALID_SKILLS, LintRequest, LintResponse
from app.services.linter import run_linter

router = APIRouter(prefix="/api", tags=["Lint"])


@router.post("/lint", response_model=LintResponse)
@limiter.limit("30/minute")
def lint_text_endpoint(request: Request, body: LintRequest):
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Văn bản không được để trống.")

    if body.skills:
        invalid = [s for s in body.skills if s not in VALID_SKILLS]
        if invalid:
            raise HTTPException(
                status_code=400,
                detail=f"Kỹ năng không hợp lệ: {', '.join(invalid)}. Các kỹ năng hợp lệ: {', '.join(sorted(VALID_SKILLS))}",
            )

    return run_linter(text=body.text, skills=body.skills)
