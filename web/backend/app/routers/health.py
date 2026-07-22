from fastapi import APIRouter
from vietnamese_writing_skills import __version__

from app.capabilities import public_capabilities

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health")
def get_health():
    return {
        "status": "ok",
        "version": __version__,
        "capabilities": public_capabilities(),
    }
