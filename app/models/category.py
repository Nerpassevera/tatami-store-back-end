"""Module for managing product categories in the database.

This module defines the Category model which represents product categories
and their relationships with products through the ProductCategory association.
"""

from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import db

if TYPE_CHECKING:
    from .product_category import ProductCategory


class Category(db.Model):
    """Category model representing product classifications in the system.
    
    Attributes:
        id: Unique identifier for the category
        name: Category name (unique)
        description: Optional category description
        products: List of associated products through ProductCategory
    """
    __tablename__ = "categories"

    # Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    products: Mapped[list["ProductCategory"]] = relationship(
        "ProductCategory",
        back_populates="category",
    )

    def __repr__(self) -> str:
        """Return string representation of the Category."""
        return f"<Category(name={self.name})>"

    def to_dict(self) -> dict:
        """Convert the category instance to a dictionary.
        
        Returns:
            dict: Category data in dictionary format
        """
        return {
            # "id": str(self.id),
            "name": self.name,
            "description": self.description
        }
