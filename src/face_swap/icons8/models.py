"""Data models for Icons8 API interactions."""

from enum import IntEnum
from typing import NewType, Optional, List
from pydantic import BaseModel, HttpUrl

ImageId = NewType("ImageId", str)

class ProcessStatus(IntEnum):
    """Status of a face swap processing job."""
    QUEUE = 0
    PROCESSING = 1
    READY = 2
    ERROR = 3

class BoundaryAdjustments(BaseModel):
    """Adjustments for face swapping."""
    emotion_fear: float = 0
    emotion_anger: float = 0
    emotion_disgust: float = 0
    emotion_surprise: float = 0
    emotion_contempt: float = 0
    emotion_happiness: float = 0
    age: float = 0
    gender: float = 0

class FaceTask(BaseModel):
    """Single face swap task configuration."""
    source_url: HttpUrl
    source_landmarks: List[int] = []
    target_landmarks: List[int] = []
    boundary_adjustments: BoundaryAdjustments = BoundaryAdjustments()

class FaceSwapRequest(BaseModel):
    """Request model for face swap operation."""
    target_url: HttpUrl
    face_tasks: List[FaceTask]

class ProcessedImage(BaseModel):
    """Details of a processed image."""
    width: int
    height: int
    type: str
    url: HttpUrl

class FaceSwapResponse(BaseModel):
    """Response model for face swap operation."""
    id: ImageId
    processed: Optional[ProcessedImage] = None
    status: ProcessStatus
    status_name: str
