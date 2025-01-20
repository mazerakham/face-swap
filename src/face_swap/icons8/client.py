"""Icons8 API client implementation."""

import logging
from typing import List, Optional
from httpx import AsyncClient, Response
from pydantic import HttpUrl
from .models import (
    FaceSwapRequest,
    FaceSwapResponse,
    ImageId,
    FaceTask,
)

logger = logging.getLogger(__name__)

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
        
        request_data = request.model_dump()
        logger.info("Submitting face swap request", extra={
            "source_url": source_url,
            "target_url": target_url,
            "request_body": request_data
        })
        logger.debug(f"Full request data: {request_data}")  # Debug print
        
        response = await self.client.post(
            "/process_image",
            params={"token": self.api_key},
            json=request.model_dump()
        )
        
        response_data = response.json()
        logger.debug(f"Face swap response data: {response_data}")  # Debug print
        self._log_response(response, "Face swap request")
        return FaceSwapResponse.model_validate(response_data)
    
    async def get_job_status(self, job_id: ImageId) -> FaceSwapResponse:
        """Get the status of a face swap job."""
        logger.info("Checking job status", extra={"job_id": job_id})
        
        response = await self.client.get(
            f"/process_image/{job_id}",
            params={"token": self.api_key}
        )
        
        response_data = response.json()
        logger.debug(f"Job status response data: {response_data}")  # Debug print
        self._log_response(response, "Job status check")
        return FaceSwapResponse.model_validate(response_data)
    
    async def list_jobs(self) -> List[FaceSwapResponse]:
        """Get list of face swap jobs."""
        logger.info("Listing face swap jobs")
        
        response = await self.client.get(
            "/process_images",
            params={"token": self.api_key}
        )
        
        self._log_response(response, "List jobs")
        data = response.json()
        return [FaceSwapResponse.model_validate(img) for img in data["images"]]
        
    def _log_response(self, response: Response, context: str) -> None:
        """Log API response details."""
        try:
            body = response.json()
        except Exception:
            body = response.text
            
        logger.info(
            f"{context} response",
            extra={
                "status_code": response.status_code,
                "response_body": body,
                "headers": dict(response.headers),
                "request_url": str(response.request.url),
                "request_method": response.request.method,
                "request_headers": dict(response.request.headers),
                "request_body": response.request.content.decode() if response.request.content else None
            }
        )
