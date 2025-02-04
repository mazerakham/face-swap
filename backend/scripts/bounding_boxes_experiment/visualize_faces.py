"""Visualize face bounding boxes on an image."""

import json
from io import BytesIO
import requests
from PIL import Image, ImageDraw

# Colors for bounding boxes (RGBA with alpha=128 for translucency)
COLORS = [
    (255, 0, 0, 128),    # Red
    (255, 165, 0, 128),  # Orange
    (255, 255, 0, 128),  # Yellow
    (0, 255, 0, 128),    # Green
    (0, 0, 255, 128)     # Blue
]

def load_image_from_url(url: str) -> Image.Image:
    """Load an image from a URL."""
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def draw_bounding_boxes(image: Image.Image, faces: list) -> Image.Image:
    """Draw translucent bounding boxes on the image."""
    # Create a copy of the image to draw on
    img_with_boxes = image.copy()
    draw = ImageDraw.Draw(img_with_boxes, 'RGBA')
    
    # Draw each face's bounding box
    for face, color in zip(faces, COLORS):
        bbox = face["bbox"]
        x_min, y_min, x_max, y_max, _ = bbox  # Ignore confidence score
        
        # Draw rectangle
        draw.rectangle(
            [x_min, y_min, x_max, y_max],
            fill=color,
            outline=color[:3] + (255,)  # Solid outline
        )
    
    return img_with_boxes

def main():
    """Load image, draw bounding boxes, and display result."""
    # Load face data
    with open("example_response.json") as f:
        data = json.load(f)
    
    # Load and process image
    image = load_image_from_url(data["img_url"])
    result = draw_bounding_boxes(image, data["faces"])
    
    # Display result
    result.show()
    
    # Save result
    result.save("faces_with_boxes.png")

if __name__ == "__main__":
    main()
