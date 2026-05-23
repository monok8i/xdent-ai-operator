"""Transcript import service."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from sqlalchemy import select

from src.infra.db.models import Transcript, TranscriptTheme

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.infra.embeddings.client import SentenceTransformerEmbeddingClient


class TranscriptImportService:
    """Import transcript JSON payloads into the database."""

    def __init__(
        self,
        *,
        session: "AsyncSession",
        embedding_client: "SentenceTransformerEmbeddingClient",
    ) -> None:
        self._session = session
        self._embedding_client = embedding_client

    async def import_from_json_text(
        self,
        *,
        theme_name: str,
        json_text: str,
        dry_run: bool = False,
    ) -> tuple[int, int]:
        """Import a JSON document for a theme and return ``(created, skipped)``."""

        normalized_theme_name = theme_name.strip()
        if not normalized_theme_name:
            raise ValueError("theme_name must not be empty")

        payloads = self._load_transcript_payloads(json_text)
        return await self._import_payloads(
            theme_name=normalized_theme_name,
            payloads=payloads,
            dry_run=dry_run,
        )

    async def import_from_path(
        self,
        *,
        theme_name: str,
        file_path: Path,
        dry_run: bool = False,
    ) -> tuple[int, int]:
        """Import transcript JSON from a file path."""

        return await self.import_from_json_text(
            theme_name=theme_name,
            json_text=file_path.read_text(encoding="utf-8"),
            dry_run=dry_run,
        )

    @staticmethod
    def _normalize_text(text: str) -> str:
        return " ".join(text.replace("\r", " ").replace("\n", " ").split())

    @staticmethod
    def _load_transcript_payloads(json_text: str) -> list[dict[str, Any]]:
        raw_data = json.loads(json_text)

        if isinstance(raw_data, list):
            raw_transcripts = cast(list[Any], raw_data)
            transcripts: list[dict[str, Any]] = []
            for item in raw_transcripts:
                if isinstance(item, dict):
                    transcripts.append(cast(dict[str, Any], item))
            return transcripts

        if isinstance(raw_data, dict):
            return [raw_data]

        raise ValueError("Unsupported JSON structure for transcript import")

    async def _get_or_create_theme(self, theme_name: str):
        theme = await self._session.scalar(
            select(TranscriptTheme).where(TranscriptTheme.name == theme_name)
        )
        if theme is not None:
            return theme

        theme = TranscriptTheme(name=theme_name)
        self._session.add(theme)
        await self._session.flush()
        return theme

    async def _get_existing_transcript_ids(self, transcript_ids: list[int]) -> set[int]:
        if not transcript_ids:
            return set()

        rows = await self._session.scalars(
            select(Transcript.transcript_id).where(
                Transcript.transcript_id.in_(transcript_ids)
            )
        )
        return set(rows.all())

    async def _import_payloads(
        self,
        *,
        theme_name: str,
        payloads: list[dict[str, Any]],
        dry_run: bool,
    ) -> tuple[int, int]:
        candidate_rows: list[dict[str, Any]] = []
        seen_transcript_ids: set[int] = set()

        for payload in payloads:
            transcript_id = payload.get("Id")
            call_entity_id = payload.get("CallEntityId")
            transcript_text = payload.get("TranscriptText")

            if (
                transcript_id is None
                or call_entity_id is None
                or transcript_text is None
            ):
                continue

            transcript_id_int = int(transcript_id)
            if transcript_id_int in seen_transcript_ids:
                continue

            normalized_text = self._normalize_text(str(transcript_text))
            if not normalized_text:
                continue

            candidate_rows.append(
                {
                    "transcript_id": transcript_id_int,
                    "call_entity_id": int(call_entity_id),
                    "clear_transcript": normalized_text,
                }
            )
            seen_transcript_ids.add(transcript_id_int)

        if not candidate_rows:
            return 0, 0

        existing_ids = await self._get_existing_transcript_ids(
            [row["transcript_id"] for row in candidate_rows]
        )
        rows_to_insert = [
            row for row in candidate_rows if row["transcript_id"] not in existing_ids
        ]

        if not rows_to_insert:
            return 0, len(candidate_rows)

        embeddings = await self._embedding_client.generate_embeddings(
            [row["clear_transcript"] for row in rows_to_insert]
        )

        if len(embeddings) != len(rows_to_insert):
            raise RuntimeError(
                f"Embedding count mismatch for theme '{theme_name}': "
                f"expected {len(rows_to_insert)}, got {len(embeddings)}"
            )

        if dry_run:
            return len(rows_to_insert), len(candidate_rows) - len(rows_to_insert)

        theme = await self._get_or_create_theme(theme_name)

        self._session.add_all(
            [
                Transcript(
                    transcript_id=row["transcript_id"],
                    call_entity_id=row["call_entity_id"],
                    theme_id=theme.id,
                    clear_transcript=row["clear_transcript"],
                    embedding=embedding,
                )
                for row, embedding in zip(rows_to_insert, embeddings, strict=True)
            ]
        )
        await self._session.flush()
        return len(rows_to_insert), len(candidate_rows) - len(rows_to_insert)
