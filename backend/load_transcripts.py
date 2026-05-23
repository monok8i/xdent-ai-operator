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
from pathlib import Path

from src.core.config._global import config
from src.infra.db.session import get_async_session
from src.infra.embeddings.client import SentenceTransformerEmbeddingClient
from src.service.transcript import TranscriptImportService


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
        import_service = TranscriptImportService(
            session=session,
            embedding_client=embedding_client,
        )

        for theme_name, transcripts_path in transcript_files:
            created, skipped = await import_service.import_from_path(
                theme_name=theme_name,
                file_path=transcripts_path,
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
