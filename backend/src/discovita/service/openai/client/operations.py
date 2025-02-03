"""OpenAI API operations."""

from typing import List, Dict, Any
from openai import AsyncOpenAI
from pydantic import AnyHttpUrl
from ..models import (
    ImageGenerationRequest,
    ImageResponse,
    GeneratedImage,
    OpenAIError,
    VisionRequest,
    CompletionRequest,
    ChatMessage,
    ChatResponse
)

async def describe_image_with_vision(
    client: AsyncOpenAI,
    image_url: AnyHttpUrl,
    prompt: str
) -> str:
    """Get a description of an image using GPT-4 Vision."""
    request = VisionRequest(
        messages=[ChatMessage(
            role="user",
            content=[
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {"url": str(image_url)}
                }
            ]
        )]
    )
    
    response = await client.chat.completions.create(**request.dict())
    return ChatResponse.from_openai_response(response).content

async def get_completion(
    client: AsyncOpenAI,
    prompt: str
) -> str:
    """Get a completion from GPT-4o."""
    request = CompletionRequest(
        messages=[ChatMessage(
            role="user",
            content=prompt
        )]
    )
    
    response = await client.chat.completions.create(**request.dict())
    return ChatResponse.from_openai_response(response).content

async def generate_image(
    client: AsyncOpenAI,
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
    
    response = await client.images.generate(**request.dict(exclude_none=True))
    # Extract revised_prompt from OpenAI's response
    return ImageResponse(
        created=int(response.created),
        data=[
            GeneratedImage(
                url=str(img.url),  # Ensure url is str
                revised_prompt=getattr(img, "revised_prompt", prompt)  # Fallback to original prompt
            )
            for img in response.data
        ]
    )
