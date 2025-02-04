"""Data models for OpenAI API interactions."""

from enum import Enum
from typing import List, Union, Dict, Any
from pydantic import BaseModel, Field

class OpenAIMode(str, Enum):
    """Operating mode for OpenAI client."""
    LIVE = "LIVE"
    TEST = "TEST"

class ImageGenerationRequest(BaseModel):
    """Request model for image generation."""
    model: str = "dall-e-3"
    prompt: str = Field(..., description="Text description of the desired image")
    n: int = 1
    size: str = "1792x1024"  # 16:9 aspect ratio, should be under 1MB
    quality: str = "standard"

class GeneratedImage(BaseModel):
    """Single generated image result."""
    url: str = Field(..., description="URL of the generated image")
    revised_prompt: str = Field(..., description="OpenAI's augmented version of the input prompt")

class ImageResponse(BaseModel):
    """Response model for image operations."""
    created: int = Field(..., description="Unix timestamp of when the request was created")
    data: List[GeneratedImage]

class OpenAIError(Exception):
    """OpenAI API error."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"OpenAI API error: {detail}")

class ChatMessage(BaseModel):
    """Chat message model."""
    role: str
    content: Union[str, List[Dict[str, Any]]]

class ChatRequest(BaseModel):
    """Base model for chat completion requests."""
    model: str
    messages: List[ChatMessage]
    max_tokens: int = 300

class ChatResponse(BaseModel):
    """Base model for chat completion responses."""
    content: str

    @classmethod
    def from_openai_response(cls, response: Any) -> "ChatResponse":
        """Create ChatResponse from OpenAI API response."""
        return cls(content=response.choices[0].message.content)

class VisionRequest(ChatRequest):
    """Request model for GPT-4 Vision."""
    model: str = "gpt-4o-mini"

class CompletionRequest(ChatRequest):
    """Request model for GPT-4 text completion."""
    model: str = "gpt-4o"
