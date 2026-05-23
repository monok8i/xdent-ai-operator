"""SQLAlchemy model for question-answer audit logs."""

from datetime import datetime

from sqlalchemy import DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.db.models.base import Base
from src.infra.db.mixins import IdIntegerMixin


class QuestionAnswerLog(IdIntegerMixin, Base):
    """Persist a prompt and its generated answer for auditability."""

    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
