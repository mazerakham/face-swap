"""OpenAI DALL-E API client implementation."""

from pathlib import Path
from typing import Optional
from httpx import AsyncClient
from ..models import ImageResponse
from . import operations
from .test import operations as test_operations

class DallEClient:
    """Client for interacting with OpenAI's DALL-E API."""
    
    def __init__(
        self,
        api_key: Optional[str],
        base_url: str = "https://api.openai.com/v1",
        test_mode: bool = False
    ) -> None:
        self.test_mode = test_mode
        if not test_mode and not api_key:
            raise ValueError("API key is required for live mode")
            
        self.base_url = base_url
        self.api_key = api_key
        self.client = AsyncClient(
            base_url=base_url,
            timeout=60.0
        )
        self.ops = test_operations if test_mode else operations
    
    async def generate_image(self, prompt: str) -> ImageResponse:
        """Generate an image from a text prompt."""
        return await self.ops.generate_image(self.client, self.api_key, prompt)

    async def edit_image(
        self,
        prompt: str,
        image: Path,
        mask: Optional[Path] = None
    ) -> ImageResponse:
        """Edit an image given the original image and a prompt."""
        return await self.ops.edit_image(self.client, self.api_key, prompt, image, mask)
