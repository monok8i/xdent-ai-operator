"""SQLAlchemy model for transcripts and their embeddings."""

from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector  # type: ignore

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.mixins import IdIntegerMixin
from src.infra.db.models.base import Base

if TYPE_CHECKING:
    from .theme import TranscriptTheme


class Transcript(IdIntegerMixin, Base):
    transcript_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    call_entity_id: Mapped[int] = mapped_column(nullable=False)
    theme_id: Mapped[int | None] = mapped_column(
        ForeignKey("transcripttheme.id"), nullable=True
    )
    clear_transcript: Mapped[str] = mapped_column(nullable=False)
    embedding: Mapped[Vector] = mapped_column(Vector(768), nullable=False)

    theme: Mapped["TranscriptTheme | None"] = relationship(back_populates="transcripts")
