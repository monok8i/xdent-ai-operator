"""Transcripts API endpoints."""

from fastapi import APIRouter


router = APIRouter(prefix="/transcripts")


@router.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    """Health check endpoint for the transcript router.

    Returns:
        A simple JSON response indicating the service is healthy.
    """
    return {"status": "ok"}
