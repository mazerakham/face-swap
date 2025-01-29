"""Application configuration."""

import os
from dataclasses import dataclass

@dataclass
class Settings:
    """Application settings loaded from environment variables."""
    icons8_api_key: str
    icons8_base_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
    s3_bucket: str
    openai_api_key: str

    @classmethod
    def from_env(cls) -> "Settings":
        """Create settings from environment variables."""
        icons8_api_key = os.getenv("FACESWAP_API_KEY")
        if not icons8_api_key:
            raise ValueError("FACESWAP_API_KEY is required")

        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        if not aws_access_key_id:
            raise ValueError("AWS_ACCESS_KEY_ID is required")

        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        if not aws_secret_access_key:
            raise ValueError("AWS_SECRET_ACCESS_KEY is required")

        s3_bucket = os.getenv("S3_BUCKET")
        if not s3_bucket:
            raise ValueError("S3_BUCKET is required")

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")

        return cls(
            icons8_api_key=icons8_api_key,
            icons8_base_url="https://api-faceswapper.icons8.com/api/v1",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_region="us-east-1",
            s3_bucket=s3_bucket,
            openai_api_key=openai_api_key
        )
