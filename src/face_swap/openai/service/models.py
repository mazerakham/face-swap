"""Service layer models for OpenAI operations."""

from dataclasses import dataclass
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field, validator

class ImageUrls(BaseModel):
    """URLs for both square and 16:9 versions of an image."""
    square_url: str = Field(..., description="URL or file path of the square image")
    wide_url: str = Field(..., description="URL or file path of the 16:9 aspect ratio image")
    
    @validator('square_url', 'wide_url')
    def validate_url(cls, v: str) -> str:
        """Validate URL is either http(s):// or file://."""
        if not (v.startswith(('http://', 'https://', 'file://'))):
            raise ValueError('URL must start with http://, https://, or file://')
        return v

class ServiceResponse(BaseModel):
    """Response model for service operations."""
    created: int = Field(..., description="Unix timestamp of when the request was created")
    data: List[ImageUrls]

@dataclass
class ImagePaths:
    """Paths for both square and 16:9 versions of an image."""
    square: Path
    wide: Path
