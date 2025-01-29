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
    request = ImageGenerationRequest(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1792x1024",
        quality="standard"
    )
    
    response = await client.post(
        "/images/generations",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=request.dict(exclude_none=True),
        timeout=60.0  # DALL-E 3 can take longer to generate
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
