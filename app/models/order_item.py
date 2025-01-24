"""
Attributes:
    __tablename__ (str): The name of the table in the database.
    order_id (Mapped[int]): The ID of the order this item belongs to.
    product_id (Mapped[int]): The ID of the product in this order item.
    quantity (Mapped[int]): The quantity of the product in this order item.
    unit_price (Mapped[float]): The unit price of the product in this order item.
    order (Mapped["Order"]): The relationship to the Order model.
    product (Mapped["Product"]): The relationship to the Product model.
Methods:
    calculate_subtotal() -> float:
    to_dict() -> dict:
    from_dict(cls, data: dict) -> "OrderItem":
    update_quantity(new_quantity: int):
    delete():
    __repr__() -> str:
        Return a string representation of the OrderItem instance.
"""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, Float

from app.db import db

if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderItem(db.Model):
    """
    Represents an item in an order, including the product, quantity, and unit price.
    """
    __tablename__ = "order_items"

    # Composite Primary Key
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey(
        "products.id", ondelete="RESTRICT"), primary_key=True)

    # Other Fields
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    order: Mapped["Order"] = relationship(
        "Order", back_populates="order_items")
    product: Mapped["Product"] = relationship("Product")

    # Methods

    def calculate_subtotal(self) -> float:
        """
        Calculate the subtotal for this order item (quantity * unit price).

        Returns:
            float: The subtotal for this item.
        """
        return self.quantity * self.unit_price

    def to_dict(self) -> dict:
        """
        Convert the order item to a dictionary representation.

        Returns:
            dict: A dictionary containing the order item details.
        """
        return {
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "subtotal": self.calculate_subtotal(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OrderItem":
        """
        Create an OrderItem instance from a dictionary.

        Args:
            data (dict): A dictionary containing order item details.

        Returns:
            OrderItem: An instance of OrderItem.
        """
        return cls(
            order_id=UUID(data["order_id"]),
            product_id=UUID(data["product_id"]),
            quantity=data["quantity"],
            unit_price=data["unit_price"],
        )

    # ?
    def update_quantity(self, new_quantity: int):
        """
        Update the quantity of the order item.

        Args:
            new_quantity (int): The new quantity to set.
        """
        self.quantity = new_quantity
        db.session.commit()

    def delete(self):
        """
        Delete the order item from the database.
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f"""<OrderItem(order_id={self.order_id},
                    product_id={self.product_id},
                    quantity={self.quantity},
                    unit_price={self.unit_price})>"""
