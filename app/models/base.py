"""
This module defines the base class for SQLAlchemy models.

Classes:
    Base: A declarative base class for all SQLAlchemy models.
"""

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy declarative models.

    This class serves as the base class for all SQLAlchemy declarative models in the application.
    It inherits from `DeclarativeBase` and provides common functionality for all models.

    Attributes:
        None
    """
    pass
