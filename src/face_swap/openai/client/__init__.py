"""OpenAI DALL-E client package."""

from . import resources  # Create transparent mask
from .client import DallEClient

__all__ = ["DallEClient"]
