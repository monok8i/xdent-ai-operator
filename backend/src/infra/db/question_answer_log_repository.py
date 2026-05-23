"""Repository for question-answer audit logs."""

from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models import QuestionAnswerLog


class QuestionAnswerLogRepository:
    """Encapsulate persistence queries for QA audit logs."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_for_export(
        self,
        *,
        limit: int,
        offset: int,
    ) -> list[QuestionAnswerLog]:
        """Return QA audit logs ordered from newest to oldest."""

        statement = (
            select(QuestionAnswerLog)
            .order_by(desc(QuestionAnswerLog.created_at), desc(QuestionAnswerLog.id))
            .offset(offset)
            .limit(limit)
        )
        rows = await self.session.execute(statement)
        return list(rows.scalars().all())
