"""Semantic search service for transcript retrieval."""

from __future__ import annotations

import re
import unicodedata
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.infra.db.models import Transcript
    from src.infra.db.repository import TranscriptRepository
    from src.infra.embeddings.client import SentenceTransformerEmbeddingClient


class SearchService:
    """Orchestrate embedding generation and chunk retrieval."""

    _CANDIDATE_MULTIPLIER = 10
    _MIN_CANDIDATE_LIMIT = 50
    _LEXICAL_WEIGHT = 0.18

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

        requested_limit = limit or self._MIN_CANDIDATE_LIMIT
        candidate_limit = max(
            requested_limit * self._CANDIDATE_MULTIPLIER,
            self._MIN_CANDIDATE_LIMIT,
        )

        hits = await self._repository.search_by_theme_embedding(
            theme_id=theme_id,
            embedding=embedding[0],
            limit=candidate_limit,
            max_distance=max_distance,
        )

        if max_distance is not None:
            relaxed_hits = await self._repository.search_by_theme_embedding(
                theme_id=theme_id,
                embedding=embedding[0],
                limit=candidate_limit,
                max_distance=None,
            )
            hits = self._merge_hits(hits, relaxed_hits)

        ranked_hits = sorted(hits, key=lambda hit: self._ranking_key(prompt, hit))

        if limit is not None:
            return ranked_hits[:limit]

        return ranked_hits

    @classmethod
    def _normalize_text(cls, text: str) -> str:
        normalized = unicodedata.normalize("NFKD", text).casefold()
        stripped = "".join(
            character
            for character in normalized
            if not unicodedata.combining(character)
        )
        return stripped

    @classmethod
    def _tokenize(cls, text: str) -> set[str]:
        normalized = cls._normalize_text(text)
        return set(re.findall(r"[a-z0-9]+", normalized))

    @classmethod
    def _lexical_overlap(cls, prompt: str, transcript: str) -> float:
        prompt_tokens = cls._tokenize(prompt)
        if not prompt_tokens:
            return 0.0

        transcript_tokens = cls._tokenize(transcript)
        if not transcript_tokens:
            return 0.0

        return len(prompt_tokens & transcript_tokens) / len(prompt_tokens)

    @classmethod
    def _ranking_key(
        cls,
        prompt: str,
        hit: tuple[Transcript, float],
    ) -> tuple[float, float, int]:
        transcript, distance = hit
        lexical_overlap = cls._lexical_overlap(prompt, transcript.clear_transcript)
        adjusted_distance = distance - (lexical_overlap * cls._LEXICAL_WEIGHT)

        return (adjusted_distance, distance, transcript.id)

    @staticmethod
    def _merge_hits(
        primary_hits: list[tuple[Transcript, float]],
        relaxed_hits: list[tuple[Transcript, float]],
    ) -> list[tuple[Transcript, float]]:
        merged: dict[int, tuple[Transcript, float]] = {
            transcript.id: (transcript, distance)
            for transcript, distance in primary_hits
        }

        for transcript, distance in relaxed_hits:
            current = merged.get(transcript.id)
            if current is None or distance < current[1]:
                merged[transcript.id] = (transcript, distance)

        return list(merged.values())
