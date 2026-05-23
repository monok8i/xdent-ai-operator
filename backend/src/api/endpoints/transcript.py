"""Transcripts API endpoints."""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from src.api.schemas import (
    TranscriptImportResponse,
    TranscriptSearchRequest,
    TranscriptSearchResponse,
    TranscriptSearchHit,
)
from src.api.depends import (
    SearchServiceDependency,
    TranscriptImportServiceDependency,
)


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


@router.post("/", response_model=TranscriptImportResponse)
async def import_transcripts(
    transcript_import_service: TranscriptImportServiceDependency,
    theme_name: str = Form(..., min_length=1),
    file: UploadFile = File(...),
) -> TranscriptImportResponse:
    """Import transcript JSON into the database for the requested theme."""

    try:
        json_text = (await file.read()).decode("utf-8")
        created, skipped = await transcript_import_service.import_from_json_text(
            theme_name=theme_name,
            json_text=json_text,
        )

    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must contain UTF-8 encoded JSON.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return TranscriptImportResponse(
        theme_name=theme_name.strip(),
        created=created,
        skipped=skipped,
    )
