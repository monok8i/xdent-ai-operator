"""Pydantic schemas for the API."""

from pydantic import BaseModel, Field


class TranscriptSearchRequest(BaseModel):
    """Search request payload for transcript retrieval."""

    theme_id: int = Field(..., ge=1)
    prompt: str = Field(..., min_length=1)
    limit: int | None = Field(default=10, ge=1, le=100)
    max_distance: float | None = Field(default=None, ge=0)


class TranscriptSearchHit(BaseModel):
    """A single ranked transcript search result."""

    id: int
    transcript_id: int
    call_entity_id: int
    theme_id: int | None
    clear_transcript: str
    distance: float


class TranscriptSearchResponse(BaseModel):
    """Response payload for transcript search requests."""

    count: int
    results: list[TranscriptSearchHit]


class TranscriptImportResponse(BaseModel):
    """Response payload for transcript import requests."""

    theme_name: str
    created: int
    skipped: int


class AnswerRequest(BaseModel):
    """Request payload for AI answer generation."""

    prompt: str = Field(..., min_length=1)


class AnswerResponse(BaseModel):
    """Response payload for AI answer generation."""

    message: str


class Theme(BaseModel):
    """A single transcript theme."""

    id: int
    name: str


class ThemeResponse(BaseModel):
    """A single transcript theme."""

    count: int
    themes: list[Theme]
