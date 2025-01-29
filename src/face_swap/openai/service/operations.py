"""Service operations for OpenAI image generation and editing."""

import os
from io import BytesIO
from pathlib import Path
import httpx
from PIL import Image
from ..client import DallEClient
from .models import ServiceResponse, ImageUrls, ImagePaths

async def download_image(url: str, path: Path) -> None:
    """Download image from URL to path."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        path.write_bytes(response.content)

def create_wide_image(square_path: Path, wide_path: Path) -> None:
    """Create 16:9 image by clipping square image."""
    with Image.open(square_path) as img:
        # Convert to RGBA
        img = img.convert('RGBA')
        width = img.width
        height = int(width * 9/16)
        top = (img.height - height) // 2
        
        wide = img.crop((0, top, width, top + height))
        wide.save(wide_path, 'PNG')
        
def save_rgba_image(img_data: bytes, path: Path) -> None:
    """Save image data as RGBA PNG."""
    with Image.open(BytesIO(img_data)) as img:
        img = img.convert('RGBA')
        img.save(path, 'PNG')

async def generate_image(
    client: DallEClient,
    prompt: str,
    temp_dir: Path,
) -> ServiceResponse:
    """Generate both square and 16:9 images from prompt."""
    # Generate square image
    response = await client.generate_image(prompt)
    square_url = response.data[0].url
    
    # Download square image
    async with httpx.AsyncClient() as http_client:
        img_response = await http_client.get(square_url)
        square_path = temp_dir / "square.png"
        save_rgba_image(img_response.content, square_path)
    
    # Create 16:9 version
    wide_path = temp_dir / "wide.png"
    create_wide_image(square_path, wide_path)
    
    # Convert local paths to file URLs
    return ServiceResponse(
        created=response.created,
        data=[ImageUrls(
            square_url=f"file://{square_path.absolute()}",
            wide_url=f"file://{wide_path.absolute()}"
        )]
    )

async def edit_image(
    client: DallEClient,
    prompt: str,
    image_paths: ImagePaths,
    temp_dir: Path,
) -> ServiceResponse:
    """Edit image and return both square and 16:9 versions."""
    # Edit square image
    response = await client.edit_image(prompt, image_paths.square)
    edited_square_url = response.data[0].url
    
    # Download edited square image
    async with httpx.AsyncClient() as http_client:
        img_response = await http_client.get(edited_square_url)
        edited_square_path = temp_dir / "edited_square.png"
        save_rgba_image(img_response.content, edited_square_path)
    
    # Create 16:9 version
    edited_wide_path = temp_dir / "edited_wide.png"
    create_wide_image(edited_square_path, edited_wide_path)
    
    # Convert local paths to file URLs
    return ServiceResponse(
        created=response.created,
        data=[ImageUrls(
            square_url=f"file://{edited_square_path.absolute()}",
            wide_url=f"file://{edited_wide_path.absolute()}"
        )]
    )
