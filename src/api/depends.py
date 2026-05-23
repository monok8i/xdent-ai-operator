"""FastAPI dependency providers for application services and resources."""

from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from starlette.requests import HTTPConnection

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.core.config._global import Config as ProjectConfig
    from src.infra.ai.client import AIClient
    from src.infra.embeddings.client import SentenceTransformerEmbeddingClient

from src.infra.ai.client import AIClient
from src.infra.db.repository import TranscriptRepository
from src.infra.db.session import get_async_session

from src.service.answer import AnswerService
from src.service.search import SearchService


def get_config(connection: HTTPConnection) -> "ProjectConfig":
    """Return the shared application configuration stored on app state.

    Args:
        connection: Current HTTP or WebSocket connection object.

    Returns:
        The shared project configuration object stored on ``app.state``.
    """

    return connection.app.state.project_config


def get_embedding_client(
    connection: HTTPConnection,
) -> "SentenceTransformerEmbeddingClient":
    """Return the shared embedding client stored on app state.

    Args:
        connection: Current HTTP or WebSocket connection object.

    Returns:
        A sentence embedding client initialized during application startup.
    """

    return connection.app.state.embedding_client


def get_ai_client(connection: HTTPConnection) -> "AIClient":
    """Return the shared AI client stored on app state."""

    return connection.app.state.ai_client


async def get_db(config: "ProjectConfig" = Depends(get_config)):
    """Yield an async database session bound to the current engine.

    Args:
        config: Resolved project configuration.

    Yields:
        An active SQLAlchemy async session.
    """
    engine = config.db.ENGINE
    if engine is None:
        raise RuntimeError("Database engine is not configured")

    async for session in get_async_session(engine):
        yield session


def get_transcript_repository(
    session: "AsyncSession" = Depends(get_db),
) -> TranscriptRepository:
    """Create the repository used for browsing transcripts."""

    return TranscriptRepository(session=session)


def search_service(
    embedding_client: "SentenceTransformerEmbeddingClient" = Depends(
        get_embedding_client
    ),
    repository: TranscriptRepository = Depends(get_transcript_repository),
):
    """Create the search service used by law search endpoints."""

    return SearchService(embedding_client=embedding_client, repository=repository)


def answer_service(
    ai_client: "AIClient" = Depends(get_ai_client),
    repository: TranscriptRepository = Depends(get_transcript_repository),
    search_service: SearchService = Depends(search_service),
) -> AnswerService:
    """Create the service that generates AI answers from transcripts."""

    return AnswerService(
        ai_client=ai_client,
        repository=repository,
        search_service=search_service,
    )


EmbeddingClientDependency = Annotated[
    "SentenceTransformerEmbeddingClient", Depends(get_embedding_client)
]


SearchServiceDependency = Annotated[SearchService, Depends(search_service)]


AnswerServiceDependency = Annotated[AnswerService, Depends(answer_service)]


TranscriptRepositoryDependency = Annotated[
    TranscriptRepository, Depends(get_transcript_repository)
]
