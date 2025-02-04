"""Tests for face selection logic."""

import pytest
from discovita.service.icons8.face_selection import BoundingBox, select_primary_face

def test_bounding_box_area():
    """Test area calculation for bounding box."""
    box = BoundingBox(x_min=10, y_min=20, x_max=110, y_max=220, confidence=0.9)
    assert box.width * box.height == 20000

def test_bounding_box_from_list():
    """Test creation of BoundingBox from list of coordinates."""
    bbox_list = [10.5, 20.5, 110.5, 220.5, 0.9]
    box = BoundingBox.from_bbox_list(bbox_list)
    assert box == BoundingBox(x_min=10, y_min=20, x_max=110, y_max=220, confidence=0.9)

def test_bounding_box_from_invalid_list():
    """Test error when creating BoundingBox from invalid list."""
    with pytest.raises(ValueError, match="not enough values to unpack"):
        BoundingBox.from_bbox_list([1, 2, 3])

def test_select_primary_face_largest():
    """Test selection of largest face from multiple faces."""
    faces = [
        BoundingBox(x_min=0, y_min=0, x_max=50, y_max=50, confidence=0.9),     # Area: 2500
        BoundingBox(x_min=0, y_min=0, x_max=100, y_max=100, confidence=0.9),   # Area: 10000 (largest)
        BoundingBox(x_min=0, y_min=0, x_max=30, y_max=30, confidence=0.9),     # Area: 900
    ]
    primary = select_primary_face(faces)
    assert primary.width == 100 and primary.height == 100

def test_select_primary_face_no_faces():
    """Test error when no faces are provided."""
    with pytest.raises(AssertionError, match="No faces detected in image"):
        select_primary_face([])

def test_select_primary_face_single():
    """Test selection with single face."""
    face = BoundingBox(x_min=0, y_min=0, x_max=50, y_max=50, confidence=0.9)
    assert select_primary_face([face]) == face

def test_select_primary_face_equal_size():
    """Test selection when faces have equal size."""
    faces = [
        BoundingBox(x_min=0, y_min=0, x_max=50, y_max=50, confidence=0.9),
        BoundingBox(x_min=100, y_min=100, x_max=150, y_max=150, confidence=0.9)
    ]
    # Should return first face when sizes are equal
    assert select_primary_face(faces) == faces[0]
