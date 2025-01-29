"""File upload route handlers."""

from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from ...config import Settings
from ...dependencies import get_settings
from ...s3 import S3Service, FileUploadRequest

router = APIRouter()

def get_s3_service(settings: Settings = Depends(get_settings)) -> S3Service:
    """Dependency for S3 service instance."""
    return S3Service(settings)

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
