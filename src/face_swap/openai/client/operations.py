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
    request_json = request.dict(exclude_none=True)
    print("\nSending to OpenAI API:")
    print(f"URL: {client.base_url}/images/generations")
    print(f"JSON payload: {request_json}")
    
    response = await client.post(
        "/images/generations",
        headers={"Authorization": f"Bearer {api_key}"},
        json=request_json,
    )
    
    if response.status_code != 200:
        raise OpenAIError(response.status_code, response.text)
    
    print(f"\nAPI Response: {response.text}")
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
    
    # Always use the transparent mask from resources
    transparent_mask = Path(__file__).parent / "transparent_mask.png"
    if not transparent_mask.exists():
        raise FileNotFoundError(
            "Transparent mask not found. Ensure the client resources are properly initialized."
        )
    
    files = {
        "image": ("image.png", image.read_bytes(), "image/png"),
        "mask": ("mask.png", transparent_mask.read_bytes(), "image/png"),
        "prompt": (None, request.prompt),
        "n": (None, str(request.n)),
        "size": (None, request.size),
    }
    
    print("\nSending to OpenAI API:")
    print(f"URL: {client.base_url}/images/edits")
    print(f"Files:")
    print(f"  - image: {image}")
    print(f"  - mask: {transparent_mask}")
    print(f"  - prompt: {request.prompt}")
    print(f"  - n: {request.n}")
    print(f"  - size: {request.size}")
    
    response = await client.post(
        "/images/edits",
        headers={"Authorization": f"Bearer {api_key}"},
        files=files,
    )
    
    if response.status_code != 200:
        raise OpenAIError(response.status_code, response.text)
    
    print(f"\nAPI Response: {response.text}")
    return ImageResponse.parse_obj(response.json())
