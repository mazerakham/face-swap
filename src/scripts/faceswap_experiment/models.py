from dataclasses import dataclass
from typing import List, Optional


@dataclass
class BoundaryAdjustments:
    emotion_fear: float = 0
    emotion_anger: float = 0
    emotion_disgust: float = 0
    emotion_surprise: float = 0
    emotion_contempt: float = 0
    emotion_happiness: float = 0
    age: float = 0
    gender: float = 0


@dataclass
class FaceTask:
    source_url: str
    source_landmarks: List[int]
    target_landmarks: List[int]
    boundary_adjustments: BoundaryAdjustments


@dataclass
class ProcessImageRequest:
    target_url: str
    face_tasks: List[FaceTask]


@dataclass
class ProcessedImage:
    width: int
    height: int
    type: str
    url: str


@dataclass
class ProcessImageResponse:
    id: str
    processed: Optional[ProcessedImage]
    status: int
    status_name: str
