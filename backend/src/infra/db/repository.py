"""Database repository for law chunk storage and semantic search."""

from typing import Sequence, cast

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.models import Transcript, TranscriptTheme


class TranscriptRepository:
    """Encapsulate persistence and vector-search queries for law chunks.

    Attributes:
        session: Active async SQLAlchemy session used for all database work.
    """

    def __init__(self, session: AsyncSession):
        """Store the active async database session used by the repository.

        Args:
            session: Async SQLAlchemy session bound to the current request.
        """

        self.session = session

    async def get_themes(self) -> list[TranscriptTheme]:
        """Return all transcript themes."""

        statement = select(TranscriptTheme)
        rows = await self.session.execute(statement)

        return cast(list[TranscriptTheme], rows.scalars().all())

    async def search_by_theme_embedding(
        self,
        *,
        theme_id: int,
        embedding: Sequence[float],
        limit: int | None = None,
        max_distance: float | None = None,
    ) -> list[tuple[Transcript, float]]:
        """Return transcripts for a theme ordered by embedding distance."""

        distance_expression = Transcript.embedding.cosine_distance(list(embedding))
        distance = distance_expression.label("distance")

        statement: Select[tuple[Transcript, float]] = select(
            Transcript, distance
        ).where(Transcript.theme_id == theme_id)

        if max_distance is not None:
            statement = statement.where(distance_expression <= max_distance)

        statement = statement.order_by(distance)

        if limit is not None:
            statement = statement.limit(limit)

        rows = await self.session.execute(statement)
        return [(row[0], float(row[1])) for row in rows.all()]
