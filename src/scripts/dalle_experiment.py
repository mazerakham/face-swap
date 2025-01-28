"""Script to demonstrate OpenAI DALL-E client functionality."""

import asyncio
import os
import httpx
from pathlib import Path
from face_swap.openai.client import DallEClient
from face_swap.openai.models import OpenAIMode

async def main() -> None:
    """Run the demonstration."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Mode from constructor (takes precedence)
    explicit_test_client = DallEClient(api_key=None, test_mode=True)
    print(f"Explicit test mode client mode: {explicit_test_client.mode}")
    
    # Mode from environment (if not specified in constructor)
    env_client = DallEClient(api_key)
    print(f"Environment-based client mode: {env_client.mode}")
    
    # Use the environment-based client for operations
    if env_client.mode == OpenAIMode.TEST:
        print("Running in TEST mode (using static test image)")
    else:
        print("Running in LIVE mode (using OpenAI API)")
    
    # Generate an image
    gen_response = await env_client.generate_image(
        "A photorealistic portrait of a young woman with blonde hair"
    )
    image_url = gen_response.data[0].url
    print(f"Generated image URL: {image_url}")
    
    # Download the generated image
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(image_url)
        temp_image = Path("temp_image.png")
        temp_image.write_bytes(response.content)
    
    # Edit the downloaded image
    edit_response = await env_client.edit_image(
        "Add a crown of flowers",
        temp_image
    )
    print(f"Edited image URL: {edit_response.data[0].url}")
    
    # Clean up
    temp_image.unlink()

if __name__ == "__main__":
    asyncio.run(main())
