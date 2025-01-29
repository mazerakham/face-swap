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
        data=[
            GeneratedImage(
                url="https://api.openai.com/test/image.png",  # Use https URL for test
                revised_prompt=f"A highly detailed digital art {prompt}, 8k resolution, cinematic lighting"
            )
        ]
    )
