"""Base SQLAlchemy model with async support and automatic table naming."""

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(AsyncAttrs, DeclarativeBase):
    """Shared declarative base for async ORM models.

    Model classes that inherit from this base automatically get async ORM
    support and a table name derived from the lowercase class name.
    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        """Derive the table name from the class name.

        Returns:
            Lowercase class name used as the database table name.
        """

        return f"{self.__name__.lower()}"
