"""Data models for Icons8 API interactions."""

from enum import IntEnum
from typing import NewType, Optional, List
from pydantic import BaseModel, AnyHttpUrl, Field

ImageId = NewType("ImageId", str)

class ProcessStatus(IntEnum):
    """Status of a face swap processing job."""
    QUEUE = 0
    PROCESSING = 1
    READY = 2
    ERROR = 3
    FAILED = 4

class Icons8Error(Exception):
    """Icons8 API error."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Icons8 API error: {detail}")

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
    source_url: AnyHttpUrl = Field(..., description="URL of the source image")
    source_landmarks: List[float] = [
        392.36614990234375, 373.7126159667969, 548.9041748046875,
        370.4452209472656, 479.63702392578125, 481.96380615234375,
        406.66619873046875, 554.4490356445312, 539.323974609375,
        551.4761352539062
    ]
    target_landmarks: List[float] = [
        529.2066650390625, 131.077392578125, 560.5444946289062,
        135.17361450195312, 551.2858276367188, 141.26443481445312,
        533.3395385742188, 160.43634033203125, 559.767578125,
        163.57125854492188
    ]
    boundary_adjustments: BoundaryAdjustments = BoundaryAdjustments()

class FaceSwapRequest(BaseModel):
    """Request model for face swap operation."""
    target_url: AnyHttpUrl = Field(..., description="URL of the target image")
    face_tasks: List[FaceTask]

class ProcessedImage(BaseModel):
    """Details of a processed image."""
    width: int
    height: int
    type: str
    url: AnyHttpUrl = Field(..., description="URL of the processed image")

class FaceSwapResponse(BaseModel):
    """Response model for face swap operation."""
    id: ImageId
    processed: Optional[ProcessedImage] = None
    status: ProcessStatus
    status_name: str = Field(alias="statusName")
