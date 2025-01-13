from dataclasses import asdict
import os
from typing import Optional
import httpx
from dotenv import load_dotenv

from .models import ProcessImageRequest, ProcessImageResponse


class FaceSwapClient:
    BASE_URL = "https://api-faceswapper.icons8.com/api/v1"

    def __init__(self) -> None:
        load_dotenv()
        api_key = os.getenv("FACESWAP_API_KEY")
        assert api_key, "FACESWAP_API_KEY must be set in .env file"
        self.api_key = api_key
        
    def _get_auth_params(self) -> dict[str, str]:
        return {"token": self.api_key}

    async def process_image(self, request: ProcessImageRequest) -> ProcessImageResponse:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/process_image",
                params=self._get_auth_params(),
                json=asdict(request)
            )
            response.raise_for_status()
            data = response.json()
            return ProcessImageResponse(**data)

    async def get_result(self, image_id: str) -> ProcessImageResponse:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/process_image/{image_id}",
                params=self._get_auth_params()
            )
            response.raise_for_status()
            data = response.json()
            return ProcessImageResponse(**data)
