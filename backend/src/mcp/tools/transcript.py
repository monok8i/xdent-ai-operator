from src.api.schemas import (
    TranscriptSearchHit,
    TranscriptSearchRequest,
    TranscriptSearchResponse,
)
from src.mcp.server import mcp
from src.mcp.depends import embedding_client, get_repository


@mcp.tool()
async def search_transcripts(
    theme_id: int,
    prompt: str,
    limit: int | None = 10,
    max_distance: float | None = None,
) -> dict[str, object]:
    """Search transcripts by theme and prompt."""

    payload = TranscriptSearchRequest(
        theme_id=theme_id,
        prompt=prompt,
        limit=limit,
        max_distance=max_distance,
    )

    embeddings = await embedding_client.generate_embeddings([payload.prompt])
    if not embeddings:
        response = TranscriptSearchResponse(count=0, results=[])
        return response.model_dump()

    async with get_repository() as repository:
        hits = await repository.search_by_theme_embedding(
            theme_id=payload.theme_id,
            embedding=embeddings[0],
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
