"""Logging utilities for Icons8 API client."""

from httpx import Response

def log_response(response: Response, context: str) -> None:
    """Log API request and response details using print statements."""
    print(f"\n=== Icons8 API {context} ===")
    
    # Request details
    print("\nRequest:")
    print(f"URL: {response.request.url}")
    print(f"Method: {response.request.method}")
    print("Body:", response.request.content.decode() if response.request.content else "None")
    
    # Response details
    print("\nResponse:")
    print(f"Status: {response.status_code}")
    print("Body:", response.text)
    print("=" * 50)
