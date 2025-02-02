"""OpenAI API client implementation."""

import os
from typing import Optional
from openai import AsyncOpenAI
from pydantic import AnyHttpUrl
from ..models import ImageResponse, OpenAIMode
from . import operations
from .test import operations as test_operations

def get_client_mode(mode: Optional[bool] = None) -> OpenAIMode:
    """Determine client mode based on constructor param and environment."""
    if mode is not None:
        return OpenAIMode.TEST if mode else OpenAIMode.LIVE
        
    env_mode = os.getenv("OPEN_AI_MODE")
    if env_mode:
        return OpenAIMode(env_mode)
        
    return OpenAIMode.LIVE

class OpenAIClient:
    """Client for interacting with OpenAI's APIs (DALL-E, Vision, Chat)."""
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openai.com/v1",
        test_mode: Optional[bool] = None
    ) -> None:
        self.mode = get_client_mode(test_mode)
        if self.mode == OpenAIMode.LIVE and not api_key:
            raise ValueError("API key is required for live mode")
            
        self.base_url = base_url
        self.api_key = api_key
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=60.0,
            max_retries=3
        )
        self.ops = test_operations if self.mode == OpenAIMode.TEST else operations
    
    async def generate_image(self, prompt: str) -> ImageResponse:
        """Generate an image from a text prompt using DALL-E."""
        return await self.ops.generate_image(self.client, self.api_key, prompt)
    
    async def describe_image_with_vision(self, image_url: AnyHttpUrl, prompt: str) -> str:
        """Get a description of an image using GPT-4 Vision."""
        return await self.ops.describe_image_with_vision(self.client, image_url, prompt)
    
    async def get_completion(self, prompt: str) -> str:
        """Get a completion from GPT-4o."""
        return await self.ops.get_completion(self.client, prompt)
