"""Pytest configuration and fixtures."""

from typing import AsyncGenerator, Generator
import pytest
from httpx import AsyncClient
from face_swap.app import create_app
from face_swap.config import Settings

@pytest.fixture
def settings() -> Generator[Settings, None, None]:
    """Test settings with dummy values."""
    yield Settings(
        icons8_api_key="test-api-key",
        icons8_base_url="https://test.icons8.com"
    )

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Test client for FastAPI application."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
