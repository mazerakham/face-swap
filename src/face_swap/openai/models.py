"""Data models for OpenAI DALL-E API interactions."""

from enum import Enum
from typing import List
from pydantic import BaseModel, AnyHttpUrl, Field

class OpenAIMode(str, Enum):
    """Operating mode for OpenAI client."""
    LIVE = "LIVE"
    TEST = "TEST"

class ImageGenerationRequest(BaseModel):
    """Request model for image generation."""
    model: str = "dall-e-3"
    prompt: str = Field(..., description="Text description of the desired image")
    n: int = 1
    size: str = "1792x1024"  # 16:9 aspect ratio, should be under 1MB
    quality: str = "standard"

class ImageEditRequest(BaseModel):
    """Request model for image editing."""
    prompt: str = Field(..., description="Text description of the desired image")
    n: int = 1
    size: str = "1792x1024"  # 16:9 aspect ratio, should be under 1MB

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
