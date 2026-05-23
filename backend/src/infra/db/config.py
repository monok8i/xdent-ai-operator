"""Database configuration and engine assembly.

The settings in this module read database environment variables and build the
async SQLAlchemy engine used by the application.
"""

from pydantic import AliasChoices, Field, PostgresDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.core.config.env import BaseEnvConfig


class Config(BaseEnvConfig):
    """Database-related environment settings and derived runtime objects.

    Attributes:
        POSTGRES_USER: Database username.
        POSTGRES_PASSWORD: Database password.
        POSTGRES_HOST: Database host name.
        POSTGRES_PORT: Database port.
        POSTGRES_DB: Database name.
        POSTGRES_DATABASE_URI: Full async connection URI.
        POSTGRES_ECHO: Whether SQLAlchemy should echo SQL statements.
        POSTGRES_ECHO_POOL: Whether SQLAlchemy should echo pool events.
        POSTGRES_POOL_MAX_OVERFLOW: Maximum overflow connections in the pool.
        POSTGRES_POOL_SIZE: Base size of the connection pool.
        POSTGRES_POOL_TIMEOUT: Pool wait timeout in seconds.
        POSTGRES_POOL_PRE_PING: Whether to validate connections before use.
        ENGINE: Lazily created async SQLAlchemy engine.
    """

    POSTGRES_USER: str | None = Field(
        default=None, validation_alias=AliasChoices("POSTGRES_USER", "PGUSER")
    )
    POSTGRES_PASSWORD: str | None = Field(
        default=None,
        validation_alias=AliasChoices("POSTGRES_PASSWORD", "PGPASSWORD"),
    )
    POSTGRES_HOST: str | None = Field(
        default=None, validation_alias=AliasChoices("POSTGRES_HOST", "PGHOST")
    )
    POSTGRES_PORT: int | None = Field(
        default=None, validation_alias=AliasChoices("POSTGRES_PORT", "PGPORT")
    )
    POSTGRES_DB: str | None = Field(
        default=None,
        validation_alias=AliasChoices("POSTGRES_DB", "PGDATABASE"),
    )

    POSTGRES_DATABASE_URI: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "POSTGRES_DATABASE_URI",
            "DATABASE_URL",
            "RAILWAY_DATABASE_URL",
            "POSTGRES_URL",
        ),
    )
    POSTGRES_ECHO: bool = True
    POSTGRES_ECHO_POOL: bool = False
    POSTGRES_POOL_MAX_OVERFLOW: int = 50
    POSTGRES_POOL_SIZE: int = 20
    POSTGRES_POOL_TIMEOUT: int = 0
    POSTGRES_POOL_PRE_PING: bool = True

    ENGINE: AsyncEngine | None = None

    @field_validator("POSTGRES_DATABASE_URI", mode="before")
    @classmethod
    def _assemble_db_connection(cls, v: str | None, info: FieldValidationInfo) -> str:
        """Build a PostgreSQL async DSN when a full URI is not provided.

        Args:
            v: Pre-existing database URI, if one was provided.
            info: Pydantic field validation context.

        Returns:
            Resolved async PostgreSQL connection string.
        """

        if isinstance(v, str):
            return v
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=info.data.get("POSTGRES_USER"),
                password=info.data.get("POSTGRES_PASSWORD"),
                host=info.data.get("POSTGRES_HOST"),
                port=info.data.get("POSTGRES_PORT"),
                path=f"{info.data.get('POSTGRES_DB') or ''}",
            )
        )

    @field_validator("ENGINE", mode="before")
    @classmethod
    def _assemble_db_engine(
        cls, v: AsyncEngine | None, info: FieldValidationInfo
    ) -> AsyncEngine:
        """Create the async SQLAlchemy engine from the resolved settings.

        Args:
            v: Pre-existing async engine, if one was provided.
            info: Pydantic field validation context.

        Returns:
            Configured async SQLAlchemy engine.
        """

        if isinstance(v, AsyncEngine):
            return v
        return create_async_engine(
            url=info.data.get("POSTGRES_DATABASE_URI"),  # type: ignore
            echo=info.data.get("POSTGRES_ECHO"),
            echo_pool=info.data.get("POSTGRES_ECHO_POOL"),
            max_overflow=info.data.get("POSTGRES_POOL_MAX_OVERFLOW"),
            pool_size=info.data.get("POSTGRES_POOL_SIZE"),
            pool_timeout=info.data.get("POSTGRES_POOL_TIMEOUT"),
            pool_pre_ping=info.data.get("POSTGRES_POOL_PRE_PING"),
        )
