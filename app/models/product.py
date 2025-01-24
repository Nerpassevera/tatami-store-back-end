"""
Product Model

This module defines the Product model for the tatami-store-back-end application.
It includes fields for product details such as name, description, price, stock quantity,
and image URL.
It also defines relationships with OrderItem, CartItem, and ProductCategory models.

Classes:
    Product: Represents a product in the store.

Fields:
    id (UUID): The unique identifier for the product.
    name (str): The name of the product.
    description (str): A description of the product.
    price (float): The price of the product.
    stock_quantity (int): The quantity of the product in stock.
    image_url (str): The URL of the product's image.

Relationships:
    order_items (list[OrderItem]): The order items associated with the product.
    cart_items (list[CartItem]): The cart items associated with the product.
    categories (list[ProductCategory]): The categories associated with the product.

Methods:
    to_dict() -> dict: Convert the product to a dictionary representation.
    update_stock(quantity: int) -> None: Update the stock quantity by a specified amount.
    __repr__() -> str: Return a string representation of the product.
"""

from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, Float, Integer

from app.db import db

if TYPE_CHECKING:
    from .order_item import OrderItem
    from .cart_item import CartItem
    from .product_category import ProductCategory


class Product(db.Model):
    """
    Represents a product in the store.

        Attributes:
            id (UUID): The unique identifier for the product.
            name (str): The name of the product.
            description (str, optional): A description of the product.
            price (float): The price of the product.
            stock_quantity (int): The quantity of the product in stock.
            image_url (str, optional): The URL of the product's image.
            order_items (list[OrderItem]): The order items associated with the product.
            cart_items (list[CartItem]): The cart items associated with the product.
            categories (list[ProductCategory]): The categories associated with the product.

        Methods:
            to_dict() -> dict:
                Convert the product to a dictionary representation.
            update_stock(quantity: int) -> None:
                Update the stock quantity by a specified amount.
            __repr__() -> str:
                Return a string representation of the product."""
    __tablename__ = "products"

    # Fields
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=True)

    # Relationships
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="product", lazy="dynamic", cascade=None
    )
    cart_items: Mapped[list["CartItem"]] = relationship(
        "CartItem", back_populates="product", lazy="dynamic", cascade="all, delete"
    )
    categories: Mapped[list["ProductCategory"]] = relationship(
        "ProductCategory", back_populates="product", lazy="select", cascade="all, delete"
    )

    @validates("stock_quantity")
    def validate_stock_quantity(self, key, value):
        """
        Validate that stock_quantity is not negative.
        
        Args:
            key (str): The name of the field being validated.
            value (int): The value to validate.

        Returns:
            int: The validated value.

        Raises:
            ValueError: If the stock_quantity is negative.
        """
        if value < 0:
            raise ValueError("Stock quantity cannot be negative")
        return value

    def to_dict(self) -> dict:
        """Convert the product to a dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock_quantity": self.stock_quantity,
        }

    def update_stock(self, quantity: int) -> None:
        """Update the stock quantity by a specified amount.

        Args:
            quantity (int): The amount to adjust the stock by (positive or negative).

        Raises:
            ValueError: If the resulting stock quantity would be negative.
        """
        if self.stock_quantity + quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.stock_quantity += quantity

    def __repr__(self) -> str:
        return (
            f"<Product(name={self.name}, price={self.price}, "
            f"stock_quantity={self.stock_quantity})>"
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """Create an instance of the class from a dictionary of data."""
        return cls(
            name=data["name"],
            description=data.get("description"),
            price=data["price"],
            stock_quantity=data["stock_quantity"] or 0,
            image_url=data.get("image_url"),
        )
