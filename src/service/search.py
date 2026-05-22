"""Semantic search service for transcript retrieval."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.infra.db.models import Transcript
    from src.infra.db.repository import TranscriptRepository
    from src.infra.embeddings.client import SentenceTransformerEmbeddingClient


class SearchService:
    """Orchestrate embedding generation and chunk retrieval."""

    def __init__(
        self,
        embedding_client: "SentenceTransformerEmbeddingClient",
        repository: "TranscriptRepository",
    ) -> None:
        self._embedding_client = embedding_client
        self._repository = repository

    async def search(
        self,
        *,
        theme_id: int,
        prompt: str,
        limit: int | None = None,
        max_distance: float | None = None,
    ) -> list[tuple[Transcript, float]]:
        """Return ranked transcript hits for the supplied prompt."""

        embedding = await self._embedding_client.generate_embeddings([prompt])
        if not embedding:
            return []

        hits = await self._repository.search_by_theme_embedding(
            theme_id=theme_id,
            embedding=embedding[0],
            limit=limit,
            max_distance=max_distance,
        )

        return hits
