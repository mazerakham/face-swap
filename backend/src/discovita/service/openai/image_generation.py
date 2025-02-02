"""Service for generating images using OpenAI."""

from pydantic import AnyHttpUrl
from .client.client import OpenAIClient
from .models import ImageResponse

class ImageGenerationService:
    """Service for generating images using OpenAI."""
    
    def __init__(self, client: OpenAIClient):
        self.client = client
    
    async def generate_scene(
        self,
        setting: str,
        outfit: str,
        emotion: str,
        user_description: str | None = None,
        user_feedback: str | None = None,
        previous_augmented_prompt: str | None = None
    ) -> ImageResponse:
        """Generate a scene based on user input."""
        # Build base prompt including user description if available
        person_desc = f"a person with {user_description}" if user_description else "a person"
        base_prompt = f"A photo of {person_desc} in {setting}, wearing {outfit}, expressing {emotion}. Make sure the scene prominently features a person with these physical characteristics."
        
        if user_feedback and previous_augmented_prompt:
            # If we have feedback and a previous prompt, use those for refinement
            prompt = f"{previous_augmented_prompt}\n\nUser Feedback: {user_feedback}"
        else:
            prompt = base_prompt

        return await self.client.generate_image(prompt)
