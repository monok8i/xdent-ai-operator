"""Database session management helpers.

This module provides the async session dependency used by the API layer.
"""

import logging
import time

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

logger = logging.getLogger(__name__)


async def get_async_session(database_engine: AsyncEngine):
    """Yield a transactional async SQLAlchemy session.

    Args:
        database_engine: Async SQLAlchemy engine used to create the session.

    Yields:
        Active async SQLAlchemy session.

    Raises:
        Exception: Re-raises any error after rolling back the transaction.

    The session is committed after successful work and rolled back on any
    exception. The session is also explicitly closed when the dependency exits.
    """

    _local_session = async_sessionmaker(
        database_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with _local_session() as session:
        try:
            start_time = time.perf_counter()
            logger.info("[Database] Session started.")

            yield session

            await session.commit()
            elapsed = time.perf_counter() - start_time
            logger.info(
                f"[Database] Session committed successfully in {elapsed:.7f} seconds."
            )

        except Exception as e:
            await session.rollback()
            raise e

        finally:
            await session.close()
