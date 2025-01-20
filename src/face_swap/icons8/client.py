"""Icons8 API client implementation."""

from typing import List, Optional
from httpx import AsyncClient
from pydantic import HttpUrl
from .models import (
    FaceSwapRequest,
    FaceSwapResponse,
    ImageId,
    FaceTask,
)

class Icons8Client:
    """Client for interacting with Icons8 face swap API."""
    
    def __init__(self, api_key: Optional[str], base_url: str) -> None:
        if not api_key:
            raise ValueError("API key is required")
            
        self.base_url = base_url
        self.api_key = api_key
        self.client = AsyncClient(base_url=base_url)
    
    async def swap_faces(self, source_url: str, target_url: str) -> FaceSwapResponse:
        """Submit a face swap job to Icons8."""
        request = FaceSwapRequest(
            target_url=HttpUrl(target_url),
            face_tasks=[FaceTask(source_url=HttpUrl(source_url))]
        )
        
        response = await self.client.post(
            "/process_image",
            params={"token": self.api_key},
            json=request.model_dump()
        )
        return FaceSwapResponse.model_validate(response.json())
    
    async def get_job_status(self, job_id: ImageId) -> FaceSwapResponse:
        """Get the status of a face swap job."""
        response = await self.client.get(
            f"/process_image/{job_id}",
            params={"token": self.api_key}
        )
        return FaceSwapResponse.model_validate(response.json())
    
    async def list_jobs(self) -> List[FaceSwapResponse]:
        """Get list of face swap jobs."""
        response = await self.client.get(
            "/process_images",
            params={"token": self.api_key}
        )
        data = response.json()
        return [FaceSwapResponse.model_validate(img) for img in data["images"]]
