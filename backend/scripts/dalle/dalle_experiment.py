"""Script to demonstrate OpenAI DALL-E client functionality."""

import asyncio
import os
import httpx
from pathlib import Path
from face_swap.openai.client import OpenAIClient
from face_swap.openai.models import OpenAIMode

async def main() -> None:
    """Run the demonstration."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Mode from constructor (takes precedence)
    explicit_test_client = OpenAIClient(api_key=None, test_mode=True)
    print(f"Explicit test mode client mode: {explicit_test_client.mode}")
    
    # Mode from environment (if not specified in constructor)
    env_client = OpenAIClient(api_key)
    print(f"Environment-based client mode: {env_client.mode}")
    
    # Use the environment-based client for operations
    if env_client.mode == OpenAIMode.TEST:
        print("Running in TEST mode (using static test image)")
    else:
        print("Running in LIVE mode (using OpenAI API)")
    
    # Generate initial image
    gen_response = await env_client.generate_image(
        "A photorealistic portrait of a young woman with blonde hair"
    )
    image_url = gen_response.data[0].url
    revised_prompt = gen_response.data[0].revised_prompt
    print(f"Generated image URL: {image_url}")
    print(f"Revised prompt: {revised_prompt}")
    
    # Generate a variation using the revised prompt
    variation_response = await env_client.generate_image(
        f"{revised_prompt}, but with a crown of flowers"
    )
    print(f"Variation image URL: {variation_response.data[0].url}")
    print(f"Variation revised prompt: {variation_response.data[0].revised_prompt}")

if __name__ == "__main__":
    asyncio.run(main())
