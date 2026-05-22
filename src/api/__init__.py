"""Top-level API router composition for the backend."""

from fastapi import APIRouter

from .endpoints.transcript import router as transcript_router

router = APIRouter(prefix="/api/v1")
router.include_router(transcript_router)

__all__ = ("router",)
