"""Image description route handlers."""

from fastapi import APIRouter, Depends
from ...models import DescribeImageRequest, DescribeImageResponse
from ..dependencies import get_image_description_service
from ...service.openai.image_description import ImageDescriptionService

router = APIRouter()

@router.post("/describe", response_model=DescribeImageResponse)
async def describe_image(
    request: DescribeImageRequest,
    service: ImageDescriptionService = Depends(get_image_description_service)
) -> DescribeImageResponse:
    """Get a clean description of an image."""
    description = await service.get_clean_description(request.image_url)
    return DescribeImageResponse(description=description)
