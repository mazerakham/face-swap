"""API route handlers."""

from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from .dependencies import get_settings
from .icons8.client import Icons8Client
from .icons8.models import Icons8Error, ImageId
from .config import Settings
from .s3 import S3Service, FileUploadRequest
from .models import SwapFaceRequest, SwapFaceResult
from .openai.client.operations import generate_image
from httpx import AsyncClient
from pydantic import BaseModel

router = APIRouter()

class GenerateImageRequest(BaseModel):
    setting: str
    outfit: str
    emotion: str
    userFeedback: str | None = None
    previousAugmentedPrompt: str | None = None

class GenerateImageResponse(BaseModel):
    imageUrl: str
    augmentedPrompt: str

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

@router.post("/generate", response_model=GenerateImageResponse)
async def generate_scene(
    request: GenerateImageRequest,
    settings: Settings = Depends(get_settings)
) -> GenerateImageResponse:
    """Generate an image based on the user's vision."""
    base_prompt = f"A photo of a person in {request.setting}, wearing {request.outfit}, expressing {request.emotion}"
    
    if request.userFeedback and request.previousAugmentedPrompt:
        # If we have feedback and a previous prompt, use those for refinement
        prompt = f"{request.previousAugmentedPrompt}\n\nUser Feedback: {request.userFeedback}"
    else:
        prompt = base_prompt

    async with AsyncClient(base_url="https://api.openai.com/v1") as client:
        response = await generate_image(client, settings.openai_api_key, prompt)
        # Get the first generated image
        image = response.data[0]
        return GenerateImageResponse(
            imageUrl=image.url,
            augmentedPrompt=image.revised_prompt
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
