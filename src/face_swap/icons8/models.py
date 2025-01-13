"""Data models for Icons8 API interactions."""

from pydantic import BaseModel, HttpUrl
from typing import NewType

ImageId = NewType("ImageId", str)

class FaceSwapRequest(BaseModel):
    """Request model for face swap operation."""
    source_image_url: HttpUrl
    target_image_url: HttpUrl

class FaceSwapResponse(BaseModel):
    """Response model for face swap operation."""
    result_image_url: HttpUrl
    job_id: ImageId
