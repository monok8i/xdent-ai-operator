"""Semantic search service for law chunks."""

from typing import TYPE_CHECKING


if TYPE_CHECKING:
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
        prompt: str,
        limit: int | None = None,
        max_distance: float | None = None,
    ) -> ...:
        """Return ranked chunk hits for the supplied prompt."""
        ...
