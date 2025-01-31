"""Mock response and request classes for testing Icons8 client."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class MockRequest:
    """Mock implementation of httpx.Request."""
    url: str
    method: str = "POST"
    content: Optional[bytes] = None

    def decode(self) -> str:
        """Decode content to string."""
        return self.content.decode() if self.content else ""

class MockResponse:
    """Mock implementation of httpx.Response."""
    
    def __init__(self, data: dict, status_code: int = 200, url: str = "https://api.icons8.com"):
        self._data = data
        self.status_code = status_code
        # Add required Response attributes
        self.http_version = "1.1"
        self.headers = {}
        self.is_closed = True
        self.is_stream_consumed = True
        self.next_request = None
        # Add request attribute required for logging
        self.request = MockRequest(url=url)
        self.text = str(data)

    def json(self) -> dict:
        """Return mock response data."""
        return self._data

    def read(self) -> bytes:
        """Mock read method."""
        return b""

    async def aread(self) -> bytes:
        """Mock async read method."""
        return b""

    def close(self) -> None:
        """Mock close method."""
        pass

    async def aclose(self) -> None:
        """Mock async close method."""
        pass
