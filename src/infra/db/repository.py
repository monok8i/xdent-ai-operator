"""Database repository for law chunk storage and semantic search."""

from sqlalchemy.ext.asyncio import AsyncSession


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
