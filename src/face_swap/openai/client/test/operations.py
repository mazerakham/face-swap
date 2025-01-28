"""Test operations that return a static image."""

from pathlib import Path
from httpx import AsyncClient
from ...models import ImageResponse, GeneratedImage

DUMMY_IMAGE_PATH = Path("src/face_swap/icons8/client/example_images/base_face_darth.png")

async def generate_image(
    client: AsyncClient,
    api_key: str,
    prompt: str,
) -> ImageResponse:
    """Return dummy image URL."""
    return ImageResponse(
        created=1234567890,
        data=[GeneratedImage(url=f"file://{DUMMY_IMAGE_PATH.absolute()}")]
    )

async def edit_image(
    client: AsyncClient,
    api_key: str,
    prompt: str,
    image: Path,
    mask: Path | None = None,
) -> ImageResponse:
    """Return dummy image URL."""
    return ImageResponse(
        created=1234567890,
        data=[GeneratedImage(url=f"file://{DUMMY_IMAGE_PATH.absolute()}")]
    )
