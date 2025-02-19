from datetime import datetime, timezone
from typing import TYPE_CHECKING
from enum import Enum as PyEnum
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship,  validates
from sqlalchemy import ForeignKey, Numeric, DateTime, Enum, String

from app.db import db

if TYPE_CHECKING:
    from .user import User
    from .order_item import OrderItem
    from .address import Address


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
    Represents an order in the system.
    Attributes:
        id (UUID): The unique identifier for the order.
        user_id (str): The ID of the user who placed the order.
        address_id (int): The ID of the address associated with the order.
        total_amount (Decimal): The total amount of the order.
        order_date (datetime): The date and time when the order was placed.
        status (OrderStatus): The current status of the order.
    Relationships:
        user (User): The user who placed the order.
        address (Address): The address associated with the order.
        order_items (list[OrderItem]): The items included in the order.
    Methods:
        validate_total_amount(key, value):
            Validates that the total amount is not negative.
        from_dict(data):
            Creates an instance of the class from a dictionary of data.
    """

    __tablename__ = "orders"

    # Fields
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[String] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    address_id: Mapped[int] = mapped_column(
        ForeignKey("addresses.id"), nullable=False)
    total_amount: Mapped[Numeric] = mapped_column(
        Numeric(10, 2), nullable=False, default=0.00)
    order_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="orders")
    address: Mapped["Address"] = relationship("Address")
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )

    @validates("total_amount")
    def validate_total_amount(self, key, value):
        """
        Validate that total_amount is not negative.

        Args:
            key (str): The name of the field being validated.
            value (float): The value to validate.

        Returns:
            float: The validated value.

        Raises:
            ValueError: If the total_amount is negative.
        """
        if value < 0:
            raise ValueError("Total amount cannot be negative.")
        return value

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
                id=uuid4(),
                user_id=data["user_id"],
                address_id=data["address_id"],
                total_amount=data.get("total_amount", 0.00),
                order_date=data.get("order_date", datetime.now(timezone.utc)),
                status=OrderStatus[data.get("status", "PENDING")],
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}") from e
        except ValueError as e:
            raise ValueError(f"Invalid status value: {e}") from e
