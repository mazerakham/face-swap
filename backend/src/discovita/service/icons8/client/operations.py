"""Icons8 API operations."""

from typing import List
from urllib.parse import quote
from httpx import AsyncClient
from pydantic import AnyHttpUrl, HttpUrl, parse_obj_as
from ..models import (
    FaceSwapRequest,
    FaceSwapResponse,
    ImageId,
    FaceTask,
    Icons8Error,
    GetBboxRequest,
    GetBboxResponse,
)
from .logging import log_response

async def get_landmarks(client: AsyncClient, api_key: str, urls: List[str]) -> GetBboxResponse:
    """Get face landmarks for the given image URLs."""
    # Let pydantic handle URL parsing and encoding
    request = GetBboxRequest(urls=parse_obj_as(List[AnyHttpUrl], urls))
    
    response = await client.post(
        "/get_bbox",
        params={"token": api_key},
        json=request.dict()
    )
    
    response_data = response.json()
    log_response(response, "Get landmarks")
    
    if response.status_code >= 400:
        raise Icons8Error(
            status_code=response.status_code,
            detail=response_data.get('error', 'Unknown error')
        )
        
    return GetBboxResponse.parse_obj(response_data)

async def swap_faces(client: AsyncClient, api_key: str, source_url: str, target_url: str) -> FaceSwapResponse:
    """Submit a face swap job to Icons8."""
    # Let pydantic handle URL parsing and encoding
    target_http_url = parse_obj_as(AnyHttpUrl, target_url)
    source_http_url = parse_obj_as(AnyHttpUrl, source_url)
    
    landmarks_response = await get_landmarks(client, api_key, [source_url, target_url])
    source_faces = next(img for img in landmarks_response.__root__ if img.img_url == source_http_url)
    target_faces = next(img for img in landmarks_response.__root__ if img.img_url == target_http_url)
    
    request = FaceSwapRequest(
        target_url=target_http_url,
        face_tasks=[FaceTask(
            source_url=source_http_url,
            source_landmarks=source_faces.faces[0].landmarks,
            target_landmarks=target_faces.faces[0].landmarks
        )]
    )
    
    response = await client.post(
        "/process_image",
        params={"token": api_key},
        json=request.dict()
    )
    
    response_data = response.json()
    log_response(response, "Face swap request")
    
    if response.status_code >= 400:
        raise Icons8Error(
            status_code=response.status_code,
            detail=response_data.get('error', 'Unknown error')
        )
        
    return FaceSwapResponse.parse_obj(response_data)

async def get_job_status(client: AsyncClient, api_key: str, job_id: ImageId) -> FaceSwapResponse:
    """Get the status of a face swap job."""
    response = await client.get(
        f"/process_image/{job_id}",
        params={"token": api_key}
    )
    
    response_data = response.json()
    log_response(response, "Job status check")
    
    if response.status_code >= 400:
        raise Icons8Error(
            status_code=response.status_code,
            detail=response_data.get('error', 'Unknown error')
        )
        
    return FaceSwapResponse.parse_obj(response_data)

async def list_jobs(client: AsyncClient, api_key: str) -> List[FaceSwapResponse]:
    """Get list of face swap jobs."""
    response = await client.get(
        "/process_images",
        params={"token": api_key}
    )
    
    log_response(response, "List jobs")
    data = response.json()
    return [FaceSwapResponse.parse_obj(img) for img in data["images"]]
