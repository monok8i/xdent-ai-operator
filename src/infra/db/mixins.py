"""Reusable mixins for SQLAlchemy models."""

from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column


@declarative_mixin
class IdIntegerMixin:
    """Add an auto-incrementing integer primary key named ``id``.

    Models can inherit from this mixin to get a standard integer identifier
    without repeating the column definition.
    """

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
