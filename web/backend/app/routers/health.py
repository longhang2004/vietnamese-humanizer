from fastapi import APIRouter
from vietnamese_writing_skills import __version__

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health")
def get_health():
    return {"status": "ok", "version": __version__}
