"""Logging configuration for OpenAI client."""

import logging
import json
from pathlib import Path
from typing import Any, Dict

import os

# Get project root directory (backend folder)
project_root = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)

# Configure logger
logger = logging.getLogger("openai_client")
logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler(log_dir / "openai.log")
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(file_handler)

def log_request(operation: str, **kwargs: Any) -> None:
    """Log OpenAI API request details."""
    request_data = {
        "operation": operation,
        **{k: v for k, v in kwargs.items() if k != "api_key"}  # Exclude sensitive data
    }
    logger.info(f"OpenAI Request: {json.dumps(request_data, indent=2)}")

def log_response(operation: str, response: Any) -> None:
    """Log OpenAI API response details."""
    # Convert response to dict, handling OpenAI response objects
    if hasattr(response, "model_dump"):
        response_data = response.model_dump()
    elif hasattr(response, "__dict__"):
        response_data = response.__dict__
    else:
        response_data = str(response)
    
    logger.info(f"OpenAI Response: {json.dumps(response_data, indent=2)}")
