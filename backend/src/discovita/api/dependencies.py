"""API dependencies."""

from typing import AsyncGenerator
from httpx import AsyncClient, Limits, Timeout

async def get_openai_client() -> AsyncGenerator[AsyncClient, None]:
    """Dependency for OpenAI client instance."""
    timeout = Timeout(60.0, connect=10.0)
    limits = Limits(max_keepalive_connections=5, max_connections=10)
    
    async with AsyncClient(
        base_url="https://api.openai.com/v1",
        timeout=timeout,
        limits=limits,
        http2=True
    ) as client:
        yield client
