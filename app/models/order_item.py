from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, Float

from app.db import db

if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderItem(db.Model):
    """
    Represents an item in an order.
    Attributes:
        order_id (int): The ID of the order this item belongs to.
        product_id (int): The ID of the product.
        quantity (int): The quantity of the product in the order.
        price (float): The price of the product in the order.
    Relationships:
        order (Order): The order this item belongs to.
        product (Product): The product associated with this item.
    Methods:
        __repr__(): Returns a string representation of the OrderItem instance.
    """
    __tablename__ = "order_items"

    # Composite Primary Key
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey(
        "products.id", ondelete="RESTRICT"), primary_key=True)

    # Other Fields
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    order: Mapped["Order"] = relationship(
        "Order", back_populates="order_items")
    product: Mapped["Product"] = relationship("Product")

    # Methods
    def __repr__(self) -> str:
        return f"""<OrderItem(order_id={self.order_id},
                    product_id={self.product_id},
                    quantity={self.quantity},
                    price={self.price})>"""
