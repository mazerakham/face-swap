"""OpenAI DALL-E API operations."""

from httpx import AsyncClient
from ..models import (
    ImageGenerationRequest,
    ImageResponse,
    GeneratedImage,
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
    
    data = response.json()
    # Extract revised_prompt from OpenAI's response
    images = [
        GeneratedImage(
            url=img["url"],
            revised_prompt=img.get("revised_prompt", prompt)  # Fallback to original prompt
        )
        for img in data["data"]
    ]
    
    return ImageResponse(
        created=data["created"],
        data=images
    )
