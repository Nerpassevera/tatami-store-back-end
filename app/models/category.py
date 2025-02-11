from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import db

if TYPE_CHECKING:
    from .product_category import ProductCategory


class Category(db.Model):
    """
    Represents a category in the tatami store.
    Attributes:
        id (int): The unique identifier for the category.
        name (str): The name of the category.
        description (Optional[str]): A brief description of the category.
        products (list[ProductCategory]): The list of product categories associated with this category.
    """
    __tablename__ = "categories"

    # Fields
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    products: Mapped[list["ProductCategory"]] = relationship(
        "ProductCategory",
        back_populates="category",
    )
