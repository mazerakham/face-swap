"""Icons8 API client implementation."""

from typing import List, Optional
from httpx import AsyncClient
from ..models import FaceSwapResponse, ImageId, GetBboxResponse
from . import operations

class Icons8Client:
    """Client for interacting with Icons8 face swap API."""
    
    def __init__(self, api_key: Optional[str], base_url: str) -> None:
        if not api_key:
            raise ValueError("API key is required")
            
        self.base_url = base_url
        self.api_key = api_key
        self.client = AsyncClient(
            base_url=base_url,
            timeout=90.0
        )
    
    async def get_landmarks(self, urls: List[str]) -> GetBboxResponse:
        """Get face landmarks for the given image URLs."""
        return await operations.get_landmarks(self.client, self.api_key, urls)
    
    async def swap_faces(self, source_url: str, target_url: str) -> FaceSwapResponse:
        """Submit a face swap job to Icons8."""
        return await operations.swap_faces(self.client, self.api_key, source_url, target_url)
    
    async def get_job_status(self, job_id: ImageId) -> FaceSwapResponse:
        """Get the status of a face swap job."""
        return await operations.get_job_status(self.client, self.api_key, job_id)
    
    async def list_jobs(self) -> List[FaceSwapResponse]:
        """Get list of face swap jobs."""
        return await operations.list_jobs(self.client, self.api_key)
