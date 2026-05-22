"""Transcripts API endpoints."""

from fastapi import APIRouter, Depends

from src.api.schemas import (
    TranscriptSearchRequest,
    TranscriptSearchResponse,
    TranscriptSearchHit,
)
from src.api.depends import SearchServiceDependency


router = APIRouter(prefix="/transcripts", tags=["transcripts"])


@router.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    """Health check endpoint for the transcript router.

    Returns:
        A simple JSON response indicating the service is healthy.
    """
    return {"status": "ok"}


@router.get("/", response_model=TranscriptSearchResponse)
async def search_transcripts(
    search_service: SearchServiceDependency,
    payload: TranscriptSearchRequest = Depends(),
) -> TranscriptSearchResponse:
    """Search transcripts by theme and prompt."""

    hits = await search_service.search(
        theme_id=payload.theme_id,
        prompt=payload.prompt,
        limit=payload.limit,
        max_distance=payload.max_distance,
    )

    return TranscriptSearchResponse(
        count=len(hits),
        results=[
            TranscriptSearchHit(
                id=transcript.id,
                transcript_id=transcript.transcript_id,
                call_entity_id=transcript.call_entity_id,
                theme_id=transcript.theme_id,
                clear_transcript=transcript.clear_transcript,
                distance=distance,
            )
            for transcript, distance in hits
        ],
    )
