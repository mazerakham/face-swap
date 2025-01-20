"""Application configuration."""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    icons8_api_key: Optional[str] = Field(None, alias="FACESWAP_API_KEY")
    icons8_base_url: str = "https://api-faceswapper.icons8.com/api/v1"
    aws_access_key_id: Optional[str] = Field(None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(None, alias="AWS_SECRET_ACCESS_KEY")
    aws_region: str = "us-east-1"
    s3_bucket: Optional[str] = Field(None, alias="S3_BUCKET")

    class Config:
        env_file = ".env"
        ignore_extra = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.icons8_api_key:
            raise ValueError("FACESWAP_API_KEY is required")
        if not self.aws_access_key_id:
            raise ValueError("AWS_ACCESS_KEY_ID is required")
        if not self.aws_secret_access_key:
            raise ValueError("AWS_SECRET_ACCESS_KEY is required")
        if not self.s3_bucket:
            raise ValueError("S3_BUCKET is required")
