"""Shared runtime helpers for MCP tools."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from src.core.config._global import config
from src.infra.db.repository import TranscriptRepository
from src.infra.db.session import get_async_session
from src.infra.embeddings.client import SentenceTransformerEmbeddingClient


embedding_client = SentenceTransformerEmbeddingClient(
    model_name=config.embeddings.EMBEDDING_MODEL_NAME,
    device=config.embeddings.EMBEDDING_DEVICE,
    normalize_embeddings=config.embeddings.EMBEDDING_NORMALIZE,
    batch_size=config.embeddings.EMBEDDING_BATCH_SIZE,
)


@asynccontextmanager
async def get_repository() -> AsyncIterator[TranscriptRepository]:
    """Yield a repository backed by the configured database engine."""

    engine = config.db.ENGINE
    if engine is None:
        raise RuntimeError("Database engine is not configured")

    async for session in get_async_session(engine):
        yield TranscriptRepository(session=session)
