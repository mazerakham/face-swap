"""Face swap route handlers."""

from fastapi import APIRouter, Depends, HTTPException, status
from ...config import Settings
from ...dependencies import get_settings
from ...models import SwapFaceRequest, SwapFaceResult
from ...icons8.client import Icons8Client
from ...icons8.models import Icons8Error, ImageId

router = APIRouter()

def get_icons8_client(settings: Settings = Depends(get_settings)) -> Icons8Client:
    """Dependency for Icons8 client instance."""
    return Icons8Client(
        api_key=settings.icons8_api_key,
        base_url=settings.icons8_base_url
    )

@router.post("/swap", response_model=SwapFaceResult, status_code=status.HTTP_201_CREATED)
async def swap_faces(
    request: SwapFaceRequest,
    client: Icons8Client = Depends(get_icons8_client)
) -> SwapFaceResult:
    """Submit a face swap request."""
    try:
        response = await client.swap_faces(
            source_url=str(request.source_url), 
            target_url=str(request.target_url)
        )
        return SwapFaceResult.from_icons8_response(response)
    except Icons8Error as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/swap/{job_id}", response_model=SwapFaceResult)
async def get_swap_status(
    job_id: str,
    client: Icons8Client = Depends(get_icons8_client)
) -> SwapFaceResult:
    """Get status of a face swap job."""
    try:
        response = await client.get_job_status(ImageId(job_id))
        return SwapFaceResult.from_icons8_response(response)
    except Icons8Error as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
