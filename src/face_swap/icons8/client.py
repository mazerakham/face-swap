"""Icons8 API client implementation."""

from httpx import AsyncClient
from pydantic import HttpUrl
from .models import FaceSwapRequest, FaceSwapResponse, ImageId

def build_url(url: str) -> HttpUrl:
    """Build a valid HttpUrl from a string."""
    return HttpUrl(url)

class Icons8Client:
    """Client for interacting with Icons8 face swap API."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.icons8.com/api/v2") -> None:
        self.base_url = base_url
        self._client = AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"}
        )
    
    async def swap_faces(self, request: FaceSwapRequest) -> FaceSwapResponse:
        """Submit a face swap job to Icons8."""
        # Stub implementation - to be completed with actual API docs
        return FaceSwapResponse(
            result_image_url=build_url("https://example.com/result.jpg"),
            job_id=ImageId("test-job-id")
        )
    
    async def get_job_status(self, job_id: ImageId) -> FaceSwapResponse:
        """Get the status of a face swap job."""
        # Stub implementation - to be completed with actual API docs
        return FaceSwapResponse(
            result_image_url=build_url("https://example.com/result.jpg"),
            job_id=job_id
        )
