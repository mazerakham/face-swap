"""Image generation route handlers."""

from fastapi import APIRouter, Depends
from httpx import AsyncClient
from ...config import Settings
from ...dependencies import get_settings
from ...models import GenerateImageRequest, GenerateImageResponse
from ...service.openai.client.operations import generate_image
from ..dependencies import get_openai_client

router = APIRouter()

@router.post("/generate", response_model=GenerateImageResponse)
async def generate_scene(
    request: GenerateImageRequest,
    settings: Settings = Depends(get_settings),
    client: AsyncClient = Depends(get_openai_client)
) -> GenerateImageResponse:
    """Generate an image based on the user's vision."""
    base_prompt = f"A photo of a person in {request.setting}, wearing {request.outfit}, expressing {request.emotion}"
    
    if request.userFeedback and request.previousAugmentedPrompt:
        # If we have feedback and a previous prompt, use those for refinement
        prompt = f"{request.previousAugmentedPrompt}\n\nUser Feedback: {request.userFeedback}"
    else:
        prompt = base_prompt

    response = await generate_image(client, settings.openai_api_key, prompt)
    # Get the first generated image
    image = response.data[0]
    return GenerateImageResponse(
        imageUrl=image.url,
        augmentedPrompt=image.revised_prompt
    )
