import asyncio
from .client import FaceSwapClient
from .models import BoundaryAdjustments, FaceTask, ProcessImageRequest


# Example URLs - replace these with your own images
SOURCE_IMAGE_URL = "https://jake-public-01.s3.us-east-1.amazonaws.com/base_image.png"
TARGET_IMAGE_URL = "https://jake-public-01.s3.us-east-1.amazonaws.com/headshot.png"


async def main() -> None:
    client = FaceSwapClient()
    
    # Create face swap request
    request = ProcessImageRequest(
        target_url=TARGET_IMAGE_URL,
        face_tasks=[
            FaceTask(
                source_url=SOURCE_IMAGE_URL,
                source_landmarks=[0],  # Use first detected face
                target_landmarks=[0],  # Replace first detected face
                boundary_adjustments=BoundaryAdjustments()
            )
        ]
    )
    
    # Submit face swap request
    response = await client.process_image(request)
    print(f"Request submitted. Image ID: {response.id}")
    
    # Poll for results
    while True:
        result = await client.get_result(response.id)
        if result.status == 2 and result.processed:  # Ready
            print(f"Face swap complete! Result URL: {result.processed.url}")
            break
        elif result.status == 2:  # Ready but no result
            print("Face swap failed: No processed result available")
            break
        elif result.status == 0 or result.statusName == "processing":  # Queue or Processing
            print("Processing... waiting 2 seconds")
            await asyncio.sleep(2)
        else:
            error_msg = f": {result.error}" if result.error else ""
            print(f"Face swap failed - {result.statusName}{error_msg}")
            break


if __name__ == "__main__":
    asyncio.run(main())
