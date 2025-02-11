from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.db import db

if TYPE_CHECKING:
    from .product import Product
    from .category import Category


class ProductCategory(db.Model):
    """
    Represents the association between products and categories in the database.
    Attributes:
        __tablename__ (str): The name of the table in the database.
        product_id (UUID): The ID of the product, which is a foreign key referencing the products table.
        category_id (int): The ID of the category, which is a foreign key referencing the categories table.
        product (Product): The relationship to the Product model.
        category (Category): The relationship to the Category model.
    Methods:
        __repr__(): Returns a string representation of the ProductCategory instance.
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
