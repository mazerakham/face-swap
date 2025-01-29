"""Face swap route handlers."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ...config import Settings
from ...dependencies import get_settings
from ...models import SwapFaceRequest
from ...service.icons8.icons8_service import Icons8Service
from ...service.icons8.client import Icons8Client
from ...service.icons8.models import Icons8Error

router = APIRouter()

def get_icons8_service(settings: Settings = Depends(get_settings)) -> Icons8Service:
    """Dependency for Icons8 service instance."""
    client = Icons8Client(
        api_key=settings.icons8_api_key,
        base_url=settings.icons8_base_url
    )
    return Icons8Service(client)

@router.post("/swap", status_code=status.HTTP_200_OK)
async def swap_faces(
    request: SwapFaceRequest,
    service: Icons8Service = Depends(get_icons8_service)
) -> JSONResponse:
    """Submit face swap request and wait for completion."""
    try:
        result = await service.swap_faces(
            source_url=request.source_url,
            target_url=request.target_url
        )
        return JSONResponse(content=result)
    except Icons8Error as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
