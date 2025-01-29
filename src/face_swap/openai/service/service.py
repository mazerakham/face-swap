"""Service for OpenAI image operations with aspect ratio handling."""

from pathlib import Path
from typing import Optional
from ..client import DallEClient
from .models import ServiceResponse, ImagePaths
from . import operations

class OpenAIService:
    """Service for OpenAI image operations."""
    
    def __init__(
        self,
        api_key: Optional[str],
        temp_dir: Path,
        test_mode: Optional[bool] = None
    ) -> None:
        """Initialize service with client and working directory."""
        self.client = DallEClient(api_key, test_mode=test_mode)
        self.temp_dir = temp_dir
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    async def generate_image(self, prompt: str) -> ServiceResponse:
        """Generate both square and 16:9 images from prompt."""
        return await operations.generate_image(
            self.client,
            prompt,
            self.temp_dir
        )
    
    async def edit_image(
        self,
        prompt: str,
        image_paths: ImagePaths,
    ) -> ServiceResponse:
        """Edit image and return both square and 16:9 versions."""
        return await operations.edit_image(
            self.client,
            prompt,
            image_paths,
            self.temp_dir
        )
