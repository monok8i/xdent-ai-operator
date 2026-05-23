"""Import transcript JSON files into the database.

The script scans ``src/utils/data`` for theme folders, reads the
``Transcripts.json`` file in each folder, generates embeddings for every
transcript, and stores the result in the ``TranscriptTheme`` and
``Transcript`` tables.

Usage:
    uv run python scripts/load_transcripts.py
    uv run python scripts/load_transcripts.py --data-dir src/utils/data
    uv run python scripts/load_transcripts.py --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from typing import Any, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config._global import config
from src.infra.db.models import Transcript, TranscriptTheme
from src.infra.db.session import get_async_session
from src.infra.embeddings.client import SentenceTransformerEmbeddingClient


def resolve_default_data_dir() -> Path:
    """Return the repository's bundled transcript data directory."""

    script_path = Path(__file__).resolve()
    for parent in (script_path.parent, *script_path.parents):
        candidate = parent / "src" / "utils" / "data"
        if candidate.exists():
            return candidate

    return script_path.parent / "src" / "utils" / "data"


DEFAULT_DATA_DIR = resolve_default_data_dir()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the import job."""

    parser = argparse.ArgumentParser(
        description="Import transcripts from theme folders into the database."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help="Root folder that contains the theme subfolders.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Read files and build embeddings, but do not write to the database.",
    )
    return parser.parse_args()


def iter_transcript_files(data_dir: Path) -> list[tuple[str, Path]]:
    """Return theme names and their matching transcript files."""

    transcript_files: list[tuple[str, Path]] = []

    for transcripts_path in sorted(data_dir.rglob("Transcripts.json")):
        if not transcripts_path.is_file():
            continue

        theme_name = transcripts_path.parent.name
        if theme_name.startswith("_"):
            continue

        transcript_files.append((theme_name, transcripts_path))

    return transcript_files


def load_transcripts(file_path: Path) -> list[dict[str, Any]]:
    """Load a transcript JSON document from disk."""

    raw_data = json.loads(file_path.read_text(encoding="utf-8"))

    if isinstance(raw_data, list):
        raw_transcripts = cast(list[Any], raw_data)
        transcripts: list[dict[str, Any]] = []
        for item in raw_transcripts:
            if isinstance(item, dict):
                transcripts.append(cast(dict[str, Any], item))
        return transcripts

    if isinstance(raw_data, dict):
        return [raw_data]

    raise ValueError(f"Unsupported JSON structure in {file_path}")


def normalize_text(text: str) -> str:
    """Return transcript text in a stable, embed-friendly format."""

    return " ".join(text.replace("\r", " ").replace("\n", " ").split())


async def get_or_create_theme(
    session: AsyncSession, theme_name: str
) -> TranscriptTheme:
    """Return the database theme row for ``theme_name``, creating it if needed."""

    theme = await session.scalar(
        select(TranscriptTheme).where(TranscriptTheme.name == theme_name)
    )
    if theme is not None:
        return theme

    theme = TranscriptTheme(name=theme_name)
    session.add(theme)
    await session.flush()
    return theme


async def get_existing_transcript_ids(
    session: AsyncSession, transcript_ids: list[int]
) -> set[int]:
    """Fetch transcript IDs that already exist in the database."""

    if not transcript_ids:
        return set()

    rows = await session.scalars(
        select(Transcript.transcript_id).where(
            Transcript.transcript_id.in_(transcript_ids)
        )
    )
    return set(rows.all())


async def import_theme_file(
    *,
    session: AsyncSession,
    embedding_client: SentenceTransformerEmbeddingClient,
    theme_name: str,
    transcripts_path: Path,
    dry_run: bool,
) -> tuple[int, int]:
    """Import a single theme file and return ``(created, skipped)`` counts."""

    payloads = load_transcripts(transcripts_path)

    candidate_rows: list[dict[str, Any]] = []
    seen_transcript_ids: set[int] = set()
    for payload in payloads:
        transcript_id = payload.get("Id")
        call_entity_id = payload.get("CallEntityId")
        transcript_text = payload.get("TranscriptText")

        if transcript_id is None or call_entity_id is None or transcript_text is None:
            continue

        transcript_id_int = int(transcript_id)
        if transcript_id_int in seen_transcript_ids:
            continue

        transcript_text = normalize_text(str(transcript_text))
        if not transcript_text:
            continue

        candidate_rows.append(
            {
                "transcript_id": transcript_id_int,
                "call_entity_id": int(call_entity_id),
                "clear_transcript": transcript_text,
            }
        )
        seen_transcript_ids.add(transcript_id_int)

    if not candidate_rows:
        return 0, 0

    existing_ids = await get_existing_transcript_ids(
        session, [row["transcript_id"] for row in candidate_rows]
    )
    rows_to_insert = [
        row for row in candidate_rows if row["transcript_id"] not in existing_ids
    ]

    if not rows_to_insert:
        return 0, len(candidate_rows)

    embeddings = await embedding_client.generate_embeddings(
        [row["clear_transcript"] for row in rows_to_insert]
    )

    if len(embeddings) != len(rows_to_insert):
        raise RuntimeError(
            f"Embedding count mismatch for {transcripts_path}: "
            f"expected {len(rows_to_insert)}, got {len(embeddings)}"
        )

    if dry_run:
        return len(rows_to_insert), len(candidate_rows) - len(rows_to_insert)

    theme = await get_or_create_theme(session, theme_name)

    session.add_all(
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
    await session.flush()
    return len(rows_to_insert), len(candidate_rows) - len(rows_to_insert)


async def run_import(data_dir: Path, dry_run: bool) -> None:
    """Import every transcript file found under ``data_dir``."""

    transcript_files = iter_transcript_files(data_dir)
    if not transcript_files:
        print(f"No Transcripts.json files found under {data_dir}")
        return

    embedding_client = SentenceTransformerEmbeddingClient(
        model_name=config.embeddings.EMBEDDING_MODEL_NAME,
        device=config.embeddings.EMBEDDING_DEVICE,
        normalize_embeddings=config.embeddings.EMBEDDING_NORMALIZE,
        batch_size=config.embeddings.EMBEDDING_BATCH_SIZE,
    )

    engine = config.db.ENGINE
    if engine is None:
        raise RuntimeError("Database engine is not configured")

    total_created = 0
    total_skipped = 0

    async for session in get_async_session(engine):
        for theme_name, transcripts_path in transcript_files:
            created, skipped = await import_theme_file(
                session=session,
                embedding_client=embedding_client,
                theme_name=theme_name,
                transcripts_path=transcripts_path,
                dry_run=dry_run,
            )
            total_created += created
            total_skipped += skipped
            print(
                f"{theme_name}: created={created}, skipped={skipped}, file={transcripts_path}"
            )

    print(
        f"Finished import: created={total_created}, skipped={total_skipped}, dry_run={dry_run}"
    )


def main() -> int:
    """CLI entrypoint."""

    args = parse_args()
    asyncio.run(run_import(data_dir=args.data_dir, dry_run=args.dry_run))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
