"""Tests for Icons8 API client."""

import pytest
from face_swap.icons8.client import Icons8Client, build_url
from face_swap.icons8.models import FaceSwapRequest, ImageId

pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_swap_faces() -> None:
    """Test face swap request returns expected response."""
    client = Icons8Client(api_key="test-key")
    request = FaceSwapRequest(
        source_image_url=build_url("https://example.com/source.jpg"),
        target_image_url=build_url("https://example.com/target.jpg")
    )
    
    response = await client.swap_faces(request)
    assert response.job_id == ImageId("test-job-id")
    assert str(response.result_image_url) == "https://example.com/result.jpg/"

@pytest.mark.asyncio
async def test_get_job_status() -> None:
    """Test job status request returns expected response."""
    client = Icons8Client(api_key="test-key")
    job_id = ImageId("test-job-id")
    
    response = await client.get_job_status(job_id)
    assert response.job_id == job_id
    assert str(response.result_image_url) == "https://example.com/result.jpg/"
