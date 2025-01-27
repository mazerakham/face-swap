"""Logging utilities for Icons8 API client."""

import logging
from httpx import Response

logger = logging.getLogger(__name__)

def log_response(response: Response, context: str) -> None:
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
