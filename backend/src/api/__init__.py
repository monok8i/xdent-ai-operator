"""Top-level API router composition for the backend."""

from fastapi import APIRouter

from .endpoints.answer import router as answer_router
from .endpoints.theme import router as theme_router
from .endpoints.qa_logs import router as qa_logs_router
from .endpoints.transcript import router as transcript_router

router = APIRouter(prefix="/api/v1")
router.include_router(answer_router)
router.include_router(qa_logs_router)
router.include_router(theme_router)
router.include_router(transcript_router)

__all__ = ("router",)
