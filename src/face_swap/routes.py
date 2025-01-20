"""API route handlers."""

from fastapi import APIRouter, Depends, UploadFile, File
import boto3
from botocore.config import Config
from .icons8.client import Icons8Client
from .icons8.models import Icons8Error, ImageId
from .config import Settings
from .models import SwapFaceRequest, SwapFaceResult

router = APIRouter()

def get_icons8_client(settings: Settings = Depends()) -> Icons8Client:
    """Dependency for Icons8 client instance."""
    return Icons8Client(
        api_key=settings.icons8_api_key,
        base_url=settings.icons8_base_url
    )

def get_s3_client(settings: Settings = Depends()):
    """Dependency for S3 client instance."""
    return boto3.client(
        's3',
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        config=Config(region_name=settings.aws_region)
    )

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    s3_client = Depends(get_s3_client),
    settings: Settings = Depends()
) -> dict[str, str]:
    """Upload an image to S3 and return its public URL."""
    content = await file.read()
    key = f"uploads/{file.filename}"
    
    s3_client.put_object(
        Bucket=settings.s3_bucket,
        Key=key,
        Body=content,
        ContentType=file.content_type
    )
    
    url = f"https://{settings.s3_bucket}.s3.{settings.aws_region}.amazonaws.com/{key}"
    return {"url": url}

@router.post("/swap", response_model=SwapFaceResult, status_code=status.HTTP_201_CREATED)
async def swap_faces(
    source_url: str,
    target_url: str,
    client: Icons8Client = Depends(get_icons8_client)
) -> SwapFaceResult:
    """Submit a face swap request."""
    try:
        response = await client.swap_faces(source_url=source_url, target_url=target_url)
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
