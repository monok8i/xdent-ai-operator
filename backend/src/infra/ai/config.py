"""Environment settings for the AI answer client."""

from pydantic import AliasChoices, Field

from src.core.config.env import BaseEnvConfig


class Config(BaseEnvConfig):
    """Model and runtime settings for AI answer generation.

    Attributes:
        AI_API_KEY: API key for the chat completion provider.
        AI_BASE_URL: Base URL for the OpenAI-compatible API.
        AI_MODEL: Chat model identifier.
        AI_TIMEOUT_SECONDS: Request timeout for AI calls.
        AI_TEMPERATURE: Default temperature for generation.
        AI_MAX_TOKENS: Default token budget for generated answers.
    """

    AI_API_KEY: str | None = Field(
        default=None,
        validation_alias=AliasChoices("AI_API_KEY", "OPENAI_API_KEY"),
    )
    AI_BASE_URL: str = Field(
        default="https://api.openai.com/v1",
        validation_alias=AliasChoices("AI_BASE_URL", "OPENAI_BASE_URL"),
    )
    AI_MODEL: str = Field(
        default="gpt-4.1-mini",
        validation_alias=AliasChoices("AI_MODEL", "OPENAI_MODEL"),
    )
    AI_TIMEOUT_SECONDS: int = 60
    AI_TEMPERATURE: float = 0.2
    AI_MAX_TOKENS: int = 256
