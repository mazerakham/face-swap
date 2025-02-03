"""Script demonstrating image generation with augmented prompt reuse."""

import asyncio
import os
from face_swap.openai.client import OpenAIClient

async def main() -> None:
    """Generate Darth Vader images using augmented prompts."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    client = OpenAIClient(api_key, test_mode=False)  # Explicitly set live mode
    
    # Generate initial Darth Vader image
    initial_response = await client.generate_image(
        "A cinematic portrait of Darth Vader in dramatic lighting"
    )
    initial_url = initial_response.data[0].url
    augmented_prompt = initial_response.data[0].revised_prompt
    
    print("Initial Darth Vader image:")
    print(f"URL: {initial_url}")
    print(f"Augmented prompt: {augmented_prompt}")
    
    # Generate variation with red eyes using the augmented prompt
    variation_response = await client.generate_image(
        f"{augmented_prompt}, but with glowing red eyes"
    )
    variation_url = variation_response.data[0].url
    variation_prompt = variation_response.data[0].revised_prompt
    
    print("\nDarth Vader with red eyes:")
    print(f"URL: {variation_url}")
    print(f"Final prompt: {variation_prompt}")

if __name__ == "__main__":
    asyncio.run(main())
