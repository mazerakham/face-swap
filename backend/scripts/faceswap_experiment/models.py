from dataclasses import dataclass, field
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
    boundary_adjustments: BoundaryAdjustments = field(default_factory=BoundaryAdjustments)
    source_landmarks: List[float] = field(default_factory=lambda: [
        392.36614990234375, 373.7126159667969, 548.9041748046875,
        370.4452209472656, 479.63702392578125, 481.96380615234375,
        406.66619873046875, 554.4490356445312, 539.323974609375,
        551.4761352539062
    ])
    target_landmarks: List[float] = field(default_factory=lambda: [
        529.2066650390625, 131.077392578125, 560.5444946289062,
        135.17361450195312, 551.2858276367188, 141.26443481445312,
        533.3395385742188, 160.43634033203125, 559.767578125,
        163.57125854492188
    ])


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
    statusName: str
    error: Optional[str] = None
