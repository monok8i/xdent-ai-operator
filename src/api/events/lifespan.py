"""Application lifespan hook for startup and shutdown orchestration."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from src.infra.ai.client import AIClient
from src.infra.embeddings.client import SentenceTransformerEmbeddingClient

if TYPE_CHECKING:
    from fastapi import FastAPI
    from src.core.config._global import Config as ProjectConfig


@asynccontextmanager
async def lifespan(app: "FastAPI") -> AsyncGenerator[None]:
    """Wrap application startup and shutdown phases.

    Args:
        app: FastAPI application instance.

    Yields:
        Nothing. The context manager exists so startup and shutdown hooks can
        be added in a single place when needed.
    """

    config: "ProjectConfig" = app.state.project_config

    app.state.ai_client = AIClient(
        api_key=config.ai.AI_API_KEY,
        base_url=config.ai.AI_BASE_URL,
        model=config.ai.AI_MODEL,
        timeout_seconds=config.ai.AI_TIMEOUT_SECONDS,
        default_temperature=config.ai.AI_TEMPERATURE,
        default_max_tokens=config.ai.AI_MAX_TOKENS,
    )

    app.state.embedding_client = SentenceTransformerEmbeddingClient(
        model_name=config.embeddings.EMBEDDING_MODEL_NAME,
        device=config.embeddings.EMBEDDING_DEVICE,
        normalize_embeddings=config.embeddings.EMBEDDING_NORMALIZE,
        batch_size=config.embeddings.EMBEDDING_BATCH_SIZE,
    )

    yield

    await app.state.ai_client.close()
