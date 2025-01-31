"""Tests for face selection logic."""

import pytest
from discovita.service.icons8.face_selection import BoundingBox, select_primary_face

def test_bounding_box_area():
    """Test area calculation for bounding box."""
    box = BoundingBox(x=10, y=20, width=100, height=200)
    assert box.area == 20000

def test_bounding_box_from_list():
    """Test creation of BoundingBox from list of coordinates."""
    bbox_list = [10.5, 20.5, 100.7, 200.3]
    box = BoundingBox.from_bbox_list(bbox_list)
    assert box == BoundingBox(x=10, y=20, width=100, height=200)

def test_bounding_box_from_invalid_list():
    """Test error when creating BoundingBox from invalid list."""
    with pytest.raises(AssertionError, match="Bounding box must contain exactly 4 values"):
        BoundingBox.from_bbox_list([1, 2, 3])

def test_select_primary_face_largest():
    """Test selection of largest face from multiple faces."""
    faces = [
        BoundingBox(x=0, y=0, width=50, height=50),    # Area: 2500
        BoundingBox(x=0, y=0, width=100, height=100),  # Area: 10000 (largest)
        BoundingBox(x=0, y=0, width=30, height=30),    # Area: 900
    ]
    primary = select_primary_face(faces)
    assert primary.width == 100 and primary.height == 100

def test_select_primary_face_no_faces():
    """Test error when no faces are provided."""
    with pytest.raises(AssertionError, match="No faces detected in image"):
        select_primary_face([])

def test_select_primary_face_single():
    """Test selection with single face."""
    face = BoundingBox(x=0, y=0, width=50, height=50)
    assert select_primary_face([face]) == face

def test_select_primary_face_equal_size():
    """Test selection when faces have equal size."""
    faces = [
        BoundingBox(x=0, y=0, width=50, height=50),
        BoundingBox(x=100, y=100, width=50, height=50)
    ]
    # Should return first face when sizes are equal
    assert select_primary_face(faces) == faces[0]
