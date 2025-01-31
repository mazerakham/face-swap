"""Face selection logic for Icons8 face swap operations."""

from dataclasses import dataclass

@dataclass(frozen=True)
class BoundingBox:
    """Represents a face bounding box with x, y coordinates, dimensions, and confidence."""
    x: int
    y: int
    width: int
    height: int
    confidence: float

    @property
    def relevance(self) -> float:
        """Calculate the relevance score (area * confidence) of the bounding box."""
        return float(self.width * self.height) * self.confidence

    @classmethod
    def from_bbox_list(cls, bbox: list[float]) -> "BoundingBox":
        """Convert Icons8 bbox format [x, y, width, height, confidence] to BoundingBox."""
        x, y, width, height, confidence, *_ = bbox  # Ignore any additional values
        return cls(
            x=int(x),
            y=int(y),
            width=int(width),
            height=int(height),
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
