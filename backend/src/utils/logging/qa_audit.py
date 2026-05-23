"""Question-answer audit logging helpers."""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models.question_answer_log import QuestionAnswerLog

_LOGGER = logging.getLogger(__name__)


async def record_qa_pair(*, session: AsyncSession, prompt: str, answer: str) -> None:
    """Persist one prompt/answer pair in the database.

    The request still succeeds even if audit storage fails; the exception is
    logged and then swallowed so the main answer path stays stable.
    """

    try:
        session.add(
            QuestionAnswerLog(
                prompt=prompt,
                answer=answer,
                created_at=datetime.now(tz=UTC),
            )
        )
        await session.flush()
    except Exception:
        _LOGGER.exception("Failed to write QA audit log to the database")
