from fastapi import Depends

from src.api.depends import SearchServiceDependency
from src.api.schemas import (
    TranscriptSearchHit,
    TranscriptSearchRequest,
    TranscriptSearchResponse,
)
from src.mcp.server import mcp


@mcp.tool()
async def search_transcripts(
    search_service: SearchServiceDependency,
    payload: TranscriptSearchRequest = Depends(),
) -> dict[str, object]:
    """Search transcripts by theme and prompt."""

    hits = await search_service.search(
        theme_id=payload.theme_id,
        prompt=payload.prompt,
        limit=payload.limit,
        max_distance=payload.max_distance,
    )

    response = TranscriptSearchResponse(
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

    return response.model_dump()
