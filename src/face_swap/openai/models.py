"""Data models for OpenAI DALL-E API interactions."""

from enum import Enum
from typing import List
from pydantic import BaseModel, AnyHttpUrl, Field

class OpenAIMode(str, Enum):
    """Operating mode for OpenAI client."""
    LIVE = "LIVE"
    TEST = "TEST"

class ImageSize(str, Enum):
    """Available image sizes for DALL-E."""
    SIZE_1024 = "1024x1024"

class ImageGenerationRequest(BaseModel):
    """Request model for image generation."""
    model: str = "dall-e-3"
    prompt: str = Field(..., description="Text description of the desired image")
    n: int = 1
    size: str = ImageSize.SIZE_1024
    quality: str = "standard"

class ImageEditRequest(BaseModel):
    """Request model for image editing."""
    prompt: str = Field(..., description="Text description of the desired image")
    n: int = 1
    size: str = ImageSize.SIZE_1024

class GeneratedImage(BaseModel):
    """Single generated image result."""
    url: AnyHttpUrl = Field(..., description="URL of the generated image")

class ImageResponse(BaseModel):
    """Response model for image operations."""
    created: int = Field(..., description="Unix timestamp of when the request was created")
    data: List[GeneratedImage]

class OpenAIError(Exception):
    """OpenAI API error."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"OpenAI API error: {detail}")
