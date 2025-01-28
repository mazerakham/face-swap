"""Script to demonstrate OpenAI DALL-E client functionality."""

import asyncio
import os
import httpx
from pathlib import Path
from face_swap.openai.client import DallEClient

async def main() -> None:
    """Run the demonstration."""
    # Test mode (no API key needed)
    test_client = DallEClient(api_key=None, test_mode=True)
    test_response = await test_client.generate_image("This will return a static test image")
    print(f"Test mode image URL: {test_response.data[0].url}")
    
    # Live mode (requires API key)
    api_key = os.getenv("OPENAI_API_KEY")
    live_client = DallEClient(api_key)  # Will raise error if API key not found
    
    # Generate an image from a prompt
    gen_response = await live_client.generate_image(
        "A photorealistic portrait of a young woman with blonde hair"
    )
    image_url = gen_response.data[0].url
    print(f"Live mode generated image URL: {image_url}")
    
    # Download the generated image
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(image_url)
        temp_image = Path("temp_image.png")
        temp_image.write_bytes(response.content)
    
    # Edit the downloaded image
    edit_response = await live_client.edit_image(
        "Add a crown of flowers",
        temp_image
    )
    print(f"Live mode edited image URL: {edit_response.data[0].url}")
    
    # Clean up
    temp_image.unlink()

if __name__ == "__main__":
    asyncio.run(main())
