"""API route handlers."""

from fastapi import APIRouter, Depends
from .icons8.client import Icons8Client
from .icons8.models import FaceSwapRequest, FaceSwapResponse, ImageId
from .config import Settings

router = APIRouter()

def get_icons8_client(settings: Settings = Depends()) -> Icons8Client:
    """Dependency for Icons8 client instance."""
    return Icons8Client(
        api_key=settings.icons8_api_key,
        base_url=settings.icons8_base_url
    )

@router.post("/swap", response_model=FaceSwapResponse)
async def swap_faces(
    request: FaceSwapRequest,
    client: Icons8Client = Depends(get_icons8_client)
) -> FaceSwapResponse:
    """Submit a face swap request."""
    return await client.swap_faces(request)

@router.get("/status/{job_id}", response_model=FaceSwapResponse)
async def get_swap_status(
    job_id: str,
    client: Icons8Client = Depends(get_icons8_client)
) -> FaceSwapResponse:
    """Get status of a face swap job."""
    return await client.get_job_status(ImageId(job_id))
