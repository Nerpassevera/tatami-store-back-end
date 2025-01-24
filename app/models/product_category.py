"""Module for managing product-category relationships in the database.

This module defines the association table between products and categories,
implementing a many-to-many relationship between these entities.
"""

from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.db import db

if TYPE_CHECKING:
    from .product import Product
    from .category import Category


class ProductCategory(db.Model):
    """Association model representing the many-to-many relationship between products and categories.
    
    This model serves as a junction table that connects products with their categories
    and vice versa, allowing products to have multiple categories and categories to
    contain multiple products.
    """

    __tablename__ = "product_categories"

    # Fields
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), primary_key=True)

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="categories")
    category: Mapped["Category"] = relationship("Category", back_populates="products")

    def __repr__(self) -> str:
        return f"<ProductCategory(product_id={self.product_id}, category_id={self.category_id})>"
