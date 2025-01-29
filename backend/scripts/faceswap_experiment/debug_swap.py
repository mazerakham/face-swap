"""Debug script for face swap API."""

import asyncio
import logging
import sys
from datetime import datetime
import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test URLs
SOURCE_URL = "https://jake-public-01.s3.us-east-1.amazonaws.com/uploads/base_face_darth.png"
TARGET_URL = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-OqfnbUaLOOzFNJuvjw0vLyqa/user-t7MEMNrMjJHzF1XFnZ6aWO0K/img-19FvB0Azl1BjMUH5uzCsQP6z.png?st=2025-01-29T17%3A58%3A16Z&se=2025-01-29T19%3A58%3A16Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-01-29T00%3A46%3A32Z&ske=2025-01-30T00%3A46%3A32Z&sks=b&skv=2024-08-04&sig=XzmW33NTSPs17OT1TOw3LPZQvG3aNcZxTjEMx1ISFaM%3D"

async def debug_face_swap() -> None:
    """Test the face swap API endpoint with polling."""
    logger.info("Starting face swap test")
    start_time = datetime.now()
    
    async with httpx.AsyncClient() as client:
        try:
            # Make request to our local API
            logger.info("Submitting face swap request...")
            response = await client.post(
                "http://localhost:8000/api/v1/swap",
                json={
                    "source_url": SOURCE_URL,
                    "target_url": TARGET_URL
                },
                timeout=120.0  # 2 minute timeout for the entire operation
            )
            
            if response.status_code != 200:
                logger.error(f"Request failed with status {response.status_code}")
                logger.error(f"Error: {response.text}")
                sys.exit(1)
                
            result = response.json()
            logger.info(f"Final response after {(datetime.now() - start_time).total_seconds():.1f} seconds:")
            logger.info(f"Status: {result['status']}")
            
            if result['status'] == 'complete':
                logger.info(f"Success! Face swap image URL: {result['url']}")
            else:
                logger.error(f"Face swap failed with status: {result['status']}")
                sys.exit(1)
            
        except Exception as e:
            logger.error(f"Error in face swap request: {e}")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(debug_face_swap())
