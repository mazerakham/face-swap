"""Face selection logic for Icons8 face swap operations."""

from dataclasses import dataclass

@dataclass(frozen=True)
class BoundingBox:
    """Represents a face bounding box with min/max coordinates and confidence."""
    x_min: int
    y_min: int
    x_max: int
    y_max: int
    confidence: float

    @property
    def width(self) -> int:
        """Calculate width from x coordinates."""
        return self.x_max - self.x_min

    @property
    def height(self) -> int:
        """Calculate height from y coordinates."""
        return self.y_max - self.y_min

    @property
    def relevance(self) -> float:
        """Calculate the relevance score (area * confidence) of the bounding box."""
        return float(self.width * self.height) * self.confidence

    @classmethod
    def from_bbox_list(cls, bbox: list[float]) -> "BoundingBox":
        """Convert Icons8 bbox format [x_min, y_min, x_max, y_max, confidence] to BoundingBox."""
        x_min, y_min, x_max, y_max, confidence, *_ = bbox  # Ignore any additional values
        return cls(
            x_min=int(x_min),
            y_min=int(y_min),
            x_max=int(x_max),
            y_max=int(y_max),
            confidence=float(confidence)
        )

def select_primary_face(faces: list[BoundingBox]) -> BoundingBox:
    """Select the most relevant face based on bounding box area and confidence.
    
    Args:
        faces: List of face bounding boxes
        
    Returns:
        BoundingBox of the face with highest relevance (area * confidence)
        
    Raises:
        AssertionError: If faces list is empty
    """
    assert faces, "No faces detected in image"
    return max(faces, key=lambda box: box.relevance)
