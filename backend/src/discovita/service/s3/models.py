"""Models for S3 operations."""

from pydantic import BaseModel

class FileUploadRequest(BaseModel):
    """Request model for file uploads."""
    filename: str
    content_type: str
    content: bytes
