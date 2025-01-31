"""Test operations that return static responses."""

from pathlib import Path
from httpx import AsyncClient
from pydantic import AnyHttpUrl
from ...models import ImageResponse, GeneratedImage

DUMMY_IMAGE_PATH = Path("src/face_swap/icons8/client/example_images/base_face_darth.png")

async def describe_image_with_vision(
    client: AsyncClient,
    image_url: AnyHttpUrl,
    prompt: str
) -> str:
    """Return dummy image description."""
    return "A person with dark brown hair, hazel eyes, and a warm smile. They have defined cheekbones and a strong jawline."

async def get_completion(
    client: AsyncClient,
    prompt: str
) -> str:
    """Return dummy completion."""
    return "Dark brown hair, hazel eyes, defined cheekbones, strong jawline."

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
