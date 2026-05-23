"""SQLAlchemy model for transcript theme."""

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.mixins import IdIntegerMixin
from src.infra.db.models.base import Base

if TYPE_CHECKING:
    from .transcript import Transcript


class TranscriptTheme(IdIntegerMixin, Base):
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    transcripts: Mapped[list["Transcript"]] = relationship(back_populates="theme")
