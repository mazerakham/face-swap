"""FastAPI application factory."""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .minimal_routes import router
from .dependencies import get_settings

def setup_logging() -> None:
    """Configure logging for the application."""
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    
    # File handler
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(logs_dir / "face_swap.log")
    file_handler.setFormatter(log_format)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Set Icons8 client logger to DEBUG for detailed API logging
    icons8_logger = logging.getLogger("face_swap.icons8.client")
    icons8_logger.setLevel(logging.DEBUG)

# Load environment variables
load_dotenv()

# Configure logging
setup_logging()

# Log environment variables on startup
logger = logging.getLogger(__name__)
logger.info("Environment variables loaded", extra={
    "FACESWAP_API_KEY": bool(os.getenv("FACESWAP_API_KEY")),
    "AWS_ACCESS_KEY_ID": bool(os.getenv("AWS_ACCESS_KEY_ID")),
    "AWS_SECRET_ACCESS_KEY": bool(os.getenv("AWS_SECRET_ACCESS_KEY")),
    "S3_BUCKET": os.getenv("S3_BUCKET")
})

app = FastAPI(title="Face Swap API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1", dependencies=[Depends(get_settings)])
