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
        missing_vars = []

        icons8_api_key = os.getenv("FACESWAP_API_KEY")
        if not icons8_api_key:
            missing_vars.append("FACESWAP_API_KEY")

        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        if not aws_access_key_id:
            missing_vars.append("AWS_ACCESS_KEY_ID")

        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        if not aws_secret_access_key:
            missing_vars.append("AWS_SECRET_ACCESS_KEY")

        s3_bucket = os.getenv("S3_BUCKET")
        if not s3_bucket:
            missing_vars.append("S3_BUCKET")

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            missing_vars.append("OPENAI_API_KEY")

        if missing_vars:
            error_msg = cls._format_missing_env_error(missing_vars)
            raise ValueError(error_msg)

        return cls(
            icons8_api_key=icons8_api_key,
            icons8_base_url="https://api-faceswapper.icons8.com/api/v1",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_region="us-east-1",
            s3_bucket=s3_bucket,
            openai_api_key=openai_api_key
        )

    @staticmethod
    def _format_missing_env_error(missing_vars: list[str]) -> str:
        """Format a helpful error message for missing environment variables."""
        is_production = os.getenv("ENVIRONMENT") == "production"

        error_parts = [
            "\n" + "="*80,
            "CONFIGURATION ERROR: Missing Required Environment Variables",
            "="*80,
            "",
            f"The following environment variable(s) are required but not set:",
        ]

        for var in missing_vars:
            error_parts.append(f"  - {var}")

        error_parts.append("")

        if is_production:
            error_parts.extend([
                "PRODUCTION ENVIRONMENT DETECTED",
                "",
                "This indicates a misconfiguration in your production environment.",
                "Please ensure all required environment variables are properly configured",
                "in your deployment platform (e.g., Render, AWS, Heroku).",
                "",
                "Contact your DevOps team or check the deployment documentation."
            ])
        else:
            error_parts.extend([
                "DEVELOPMENT ENVIRONMENT",
                "",
                "To run this application locally, you need to:",
                "",
                "1. Create a .env file in the backend directory if it doesn't exist",
                "2. Add the required environment variables to the .env file",
                "",
                "To obtain API keys and credentials:",
                "  - Check your team's password manager (e.g., 1Password, LastPass)",
                "  - Refer to the project documentation in the repository",
                "  - Contact a team member or tech lead for assistance",
                "",
                "Example .env file format:",
                "  FACESWAP_API_KEY=your_icons8_api_key_here",
                "  AWS_ACCESS_KEY_ID=your_aws_access_key",
                "  AWS_SECRET_ACCESS_KEY=your_aws_secret_key",
                "  S3_BUCKET=your_s3_bucket_name",
                "  OPENAI_API_KEY=your_openai_api_key"
            ])

        error_parts.extend([
            "",
            "="*80,
            ""
        ])

        return "\n".join(error_parts)
