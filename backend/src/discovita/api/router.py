"""API router configuration."""

from fastapi import APIRouter
from .routes import image_generation, face_swap, upload

router = APIRouter()

@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}

# Include route modules
router.include_router(image_generation.router, tags=["image-generation"])
router.include_router(face_swap.router, tags=["face-swap"])
router.include_router(upload.router, tags=["upload"])
