"""Icons8 service for face swap operations."""

import asyncio
from typing import Dict
from pydantic import HttpUrl
from .client import Icons8Client
from .models import ImageId, Icons8Error, ProcessStatus
from ...models import SwapFaceResult

class Icons8Service:
    """Service for Icons8 face swap operations."""
    
    def __init__(self, client: Icons8Client):
        self.client = client
        self.max_polling_time = 60  # Maximum time to wait in seconds
        self.polling_interval = 2   # Time between checks in seconds
        
    async def _poll_until_complete(self, job_id: ImageId) -> SwapFaceResult:
        """Poll job status until completion or timeout."""
        start_time = asyncio.get_event_loop().time()
        
        while True:
            if asyncio.get_event_loop().time() - start_time > self.max_polling_time:
                raise Icons8Error(
                    status_code=504,
                    detail="Face swap operation timed out"
                )
                
            response = await self.client.get_job_status(job_id)
            result = SwapFaceResult.from_icons8_response(response)
            
            if result.status == ProcessStatus.READY:
                return result
                
            if result.status in (ProcessStatus.ERROR, ProcessStatus.FAILED):
                raise Icons8Error(
                    status_code=500,
                    detail=f"Face swap failed: {result.status_name}"
                )
                
            await asyncio.sleep(self.polling_interval)
    
    async def swap_faces(self, source_url: HttpUrl, target_url: HttpUrl) -> Dict[str, str]:
        """
        Perform face swap operation and wait for completion.
        
        Returns:
            Dict with url and status keys formatted for frontend consumption.
        """
        # Initiate face swap
        response = await self.client.swap_faces(
            source_url=str(source_url),
            target_url=str(target_url)
        )
        initial_result = SwapFaceResult.from_icons8_response(response)
        
        # Poll until complete
        final_result = await self._poll_until_complete(ImageId(initial_result.job_id))
        
        # Convert to frontend format
        return final_result.to_frontend_response()
