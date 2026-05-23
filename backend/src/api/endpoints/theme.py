"""Themes API endpoints."""

from fastapi import APIRouter

from src.api.schemas import Theme, ThemeResponse
from src.api.depends import TranscriptRepositoryDependency


router = APIRouter(prefix="/themes", tags=["themes"])


@router.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    """Health check endpoint for the transcript router.

    Returns:
        A simple JSON response indicating the service is healthy.
    """
    return {"status": "ok"}


@router.get("/", response_model=ThemeResponse)
async def get_themes(
    repository: TranscriptRepositoryDependency,
) -> ThemeResponse:
    """Return all available transcript themes."""

    themes = await repository.get_themes()
    count = len(themes)

    return ThemeResponse(
        count=count, themes=[Theme(id=theme.id, name=theme.name) for theme in themes]
    )
