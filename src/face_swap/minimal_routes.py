"""API route handlers."""

from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from .dependencies import get_settings
from .icons8.client import Icons8Client
from .icons8.models import FaceSwapResponse
from .config import Settings
from .s3 import S3Service, FileUploadRequest

router = APIRouter()

def get_icons8_client(settings: Settings = Depends(get_settings)) -> Icons8Client:
    """Dependency for Icons8 client instance."""
    return Icons8Client(
        api_key=settings.icons8_api_key,
        base_url=settings.icons8_base_url
    )

def get_s3_service(settings: Settings = Depends(get_settings)) -> S3Service:
    """Dependency for S3 service instance."""
    return S3Service(settings)

@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}

@router.post("/upload")
async def upload_image(
    file: UploadFile,
    s3_service: S3Service = Depends(get_s3_service)
) -> dict[str, str]:
    """Upload an image to S3 and return its public URL."""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required"
        )
    
    if not file.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content type is required"
        )
    
    content = await file.read()
    request = FileUploadRequest(
        filename=file.filename,
        content_type=file.content_type,
        content=content
    )
    url = s3_service.upload(request)
    return {"url": url}

@router.post("/swap", response_model=FaceSwapResponse)
async def swap_faces(
    source_url: str,
    target_url: str,
    client: Icons8Client = Depends(get_icons8_client)
) -> FaceSwapResponse:
    """Submit a face swap request."""
    return await client.swap_faces(source_url=source_url, target_url=target_url)
