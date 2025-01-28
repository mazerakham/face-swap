"""OpenAI DALL-E API operations."""

from pathlib import Path
from httpx import AsyncClient
from ..models import (
    ImageGenerationRequest,
    ImageEditRequest,
    ImageResponse,
    OpenAIError,
)

async def generate_image(
    client: AsyncClient,
    api_key: str,
    prompt: str,
) -> ImageResponse:
    """Generate an image from a text prompt."""
    request = ImageGenerationRequest(prompt=prompt)
    response = await client.post(
        "/images/generations",
        headers={"Authorization": f"Bearer {api_key}"},
        json=request.dict(exclude_none=True),
    )
    
    if response.status_code != 200:
        raise OpenAIError(response.status_code, response.text)
        
    return ImageResponse.parse_obj(response.json())

async def edit_image(
    client: AsyncClient,
    api_key: str,
    prompt: str,
    image: Path,
    mask: Path | None = None,
) -> ImageResponse:
    """Edit an image given the original image and a prompt."""
    request = ImageEditRequest(prompt=prompt)
    files = {
        "image": ("image.png", image.read_bytes(), "image/png"),
        "prompt": (None, request.prompt),
        "n": (None, str(request.n)),
        "size": (None, request.size),
    }
    
    if mask:
        files["mask"] = ("mask.png", mask.read_bytes(), "image/png")
    
    response = await client.post(
        "/images/edits",
        headers={"Authorization": f"Bearer {api_key}"},
        files=files,
    )
    
    if response.status_code != 200:
        raise OpenAIError(response.status_code, response.text)
        
    return ImageResponse.parse_obj(response.json())
