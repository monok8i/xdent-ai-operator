"""Application lifespan hook for startup and shutdown orchestration."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

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

    app.state.embedding_client = SentenceTransformerEmbeddingClient(
        model_name=config.embeddings.EMBEDDING_MODEL_NAME,
        device=config.embeddings.EMBEDDING_DEVICE,
        normalize_embeddings=config.embeddings.EMBEDDING_NORMALIZE,
        batch_size=config.embeddings.EMBEDDING_BATCH_SIZE,
    )

    yield
