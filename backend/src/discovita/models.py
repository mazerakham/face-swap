"""API-specific data models."""

from pydantic import BaseModel, HttpUrl
from enum import IntEnum
from typing import Optional

class GenerateImageRequest(BaseModel):
    setting: str
    outfit: str
    emotion: str
    userFeedback: str | None = None
    previousAugmentedPrompt: str | None = None

class GenerateImageResponse(BaseModel):
    imageUrl: str
    augmentedPrompt: str
    
class SwapFaceRequest(BaseModel):
    """Request model for face swap operation."""
    source_url: HttpUrl
    target_url: HttpUrl

class ProcessingStatus(IntEnum):
    """Status of a face swap processing job."""
    QUEUE = 0
    PROCESSING = 1
    READY = 2
    ERROR = 3
    FAILED = 4

class ProcessedImageResult(BaseModel):
    """Details of a processed image."""
    width: int
    height: int
    type: str
    url: HttpUrl

class SwapFaceResult(BaseModel):
    """Response model for face swap operation."""
    job_id: str
    processed: Optional[ProcessedImageResult] = None
    status: ProcessingStatus
    status_name: str

    @classmethod
    def from_icons8_response(cls, response):
        """Convert Icons8 response to our API response model."""
        return cls(
            job_id=response.id,
            processed=ProcessedImageResult(
                width=response.processed.width,
                height=response.processed.height,
                type=response.processed.type,
                url=response.processed.url
            ) if response.processed else None,
            status=ProcessingStatus(response.status),
            status_name=response.status_name
        )
