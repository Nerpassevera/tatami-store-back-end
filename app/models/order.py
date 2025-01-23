"""
This module defines the Order model and related functionality.
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from enum import Enum as PyEnum
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric, DateTime, Enum

from app.db import db

if TYPE_CHECKING:
    from .user import User
    from .order_item import OrderItem


class OrderStatus(PyEnum):
    """
    Enum class representing the status of an order.

    Attributes:
        PENDING (str): The order is pending and has not been completed or canceled.
        COMPLETED (str): The order has been completed successfully.
        CANCELED (str): The order has been canceled and will not be completed.
    """
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELED = "Canceled"


class Order(db.Model):
    """
    Represents an order in the tatami store.

    Attributes:
        id (UUID): The unique identifier for the order.
        user_id (UUID): The unique identifier for the user who placed the order.
        total_amount (Numeric): The total amount for the order.
        order_date (datetime): The date and time when the order was placed.
        status (OrderStatus): The current status of the order.

    Relationships:
        user (User): The user who placed the order.
        items (list[OrderItem]): The items included in the order.

    Methods:
        to_dict(): Converts the order instance to a dictionary.
        __repr__(): Returns a string representation of the order instance.
        from_dict(data): Creates an order instance from a dictionary.

    Raises:
        ValueError: If required fields are missing or if an invalid status value is provided.
    """
    __tablename__ = "orders"

    # Fields
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    total_amount: Mapped[Numeric] = mapped_column(
        Numeric(10, 2), nullable=False, default=0.00)
    order_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )

    # Methods
    def to_dict(self):
        """
        Converts the Order object to a dictionary representation.

        Returns:
            dict: A dictionary containing the order details with the following keys:
                - id (str): The unique identifier of the order.
                - user_id (str): The unique identifier of the user who placed the order.
                - total_amount (float): The total amount of the order.
                - order_date (str): The date the order was placed in ISO 8601 format.
                - status (str): The current status of the order.
                - items (list): A list of dictionaries representing the items in the order.
        """
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "total_amount": float(self.total_amount),
            "order_date": self.order_date.isoformat(),
            "status": self.status.value,
            "items": [item.to_dict() for item in self.items],
        }

    def __repr__(self):
        return f"<Order {self.id} - Status: {self.status.value}>"

    @classmethod
    def from_dict(cls, data):
        """
        Create an instance of the class from a dictionary of data.

        Args:
                - "order_date" (datetime, optional): The date of the order.
                    Defaults to the current UTC time.
                Expected keys are:
                - "user_id" (int): The ID of the user.
                - "total_amount" (float, optional): The total amount of the order. Defaults to 0.00.
                - "order_date" (datetime, optional): The date of the order. 
                    Defaults to the current UTC time.
                - "status" (str, optional): The status of the order. Defaults to "PENDING".

        Returns:
            An instance of the class.

        Raises:
            ValueError: If a required field is missing or if the status value is invalid.
        """
        try:
            return cls(
                user_id=data["user_id"],
                total_amount=data.get("total_amount", 0.00),
                order_date=data.get("order_date", datetime.now(timezone.utc)),
                status=OrderStatus[data.get("status", "PENDING")],
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}") from e
        except ValueError as e:
            raise ValueError(f"Invalid status value: {e}") from e
