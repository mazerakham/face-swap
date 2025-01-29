"""Resource initialization for OpenAI client."""

from pathlib import Path
from PIL import Image

def create_transparent_mask() -> None:
    """Create a 1024x1024 transparent PNG to use as mask for edits."""
    mask_path = Path(__file__).parent / "transparent_mask.png"
    if not mask_path.exists():
        # Create a fully transparent RGBA image
        img = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
        img.save(mask_path, 'PNG')

# Create resources when module is imported
create_transparent_mask()
