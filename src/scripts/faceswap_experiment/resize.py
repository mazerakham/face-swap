from PIL import Image
import os

# Define the paths
IMAGE_PATH = "/Users/jakemirra/Downloads/base_image.png"
NEW_IMAGE_PATH = "/Users/jakemirra/Downloads/target_image_small.png"

def downscale_image(image_path, new_image_path, size_reduction_factor=2):
    """
    Downscale the image to ensure its file size is no more than half of the original size.

    Args:
        image_path (str): Path to the original image.
        new_image_path (str): Path to save the downscaled image.
        size_reduction_factor (int): Factor by which to reduce dimensions.
    """
    # Open the image
    with Image.open(image_path) as img:
        # Calculate new dimensions
        original_width, original_height = img.size
        new_width = max(1, original_width // size_reduction_factor)
        new_height = max(1, original_height // size_reduction_factor)

        # Downscale the image
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)

        # Save the image with high-efficiency compression
        img_resized.save(new_image_path, optimize=True, quality=85)

        # Ensure the new image size is less than half the original
        original_size = os.path.getsize(image_path)
        new_size = os.path.getsize(new_image_path)

        # If the new file is still too large, reduce quality further
        while new_size > original_size / 2:
            with Image.open(new_image_path) as img:
                img.save(new_image_path, optimize=True, quality=75)
            new_size = os.path.getsize(new_image_path)

        print(f"Original size: {original_size / 1024:.2f} KB")
        print(f"New size: {new_size / 1024:.2f} KB")
        print(f"Image saved to {new_image_path}")

# Run the function
downscale_image(IMAGE_PATH, NEW_IMAGE_PATH)
