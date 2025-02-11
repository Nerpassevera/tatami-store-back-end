from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer

from app.db import db

if TYPE_CHECKING:
    from .cart import Cart
    from .product import Product


class CartItem(db.Model):
    """
    Represents an item in a shopping cart.
    Attributes:
        __tablename__ (str): The name of the table in the database.
        cart_id (UUID): The ID of the cart to which this item belongs.
        product_id (UUID): The ID of the product.
        quantity (int): The quantity of the product in the cart.
        cart (Cart): The cart to which this item belongs.
        product (Product): The product associated with this item.
    Methods:
        from_dict(data):
    """
    __tablename__ = "cart_items"

    # Composite primary key
    cart_id: Mapped[UUID] = mapped_column(ForeignKey(
        "carts.id", ondelete="CASCADE"), primary_key=True)
    product_id: Mapped[UUID] = mapped_column(ForeignKey(
        "products.id", ondelete="CASCADE"), primary_key=True)

    # Other fields
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    product: Mapped["Product"] = relationship("Product")

    @classmethod
    def from_dict(cls, data):
        """
        Create an instance of the class from a dictionary.
        Args:
            data (dict): A dictionary containing the keys 'cart_id', 'product_id', and 'quantity'.
        Returns:
            An instance of the class.
        Raises:
            ValueError: If any of the required fields ('cart_id', 'product_id', 'quantity') 
            are missing from the dictionary.
        """
        try:
            return cls(
                cart_id=data["cart_id"],
                product_id=data["product_id"],
                quantity=data["quantity"],
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}") from e
