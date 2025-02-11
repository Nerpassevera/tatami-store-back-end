from uuid import UUID, uuid4
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from app.db import db

if TYPE_CHECKING:
    from .user import User
    from .cart_item import CartItem


class Cart(db.Model):
    """
        Represents a shopping cart in the tatami store back-end application.
        Attributes:
            id (UUID): The unique identifier for the cart.
            user_id (String): The unique identifier for the user associated with the cart.
            user (User): The user who owns the cart.
            items (Optional[list[CartItem]]): The list of items in the cart.
        Relationships:
            user: A one-to-one relationship with the User model.
            items: A one-to-many relationship with the CartItem model, with cascading delete-orphan behavior.
    """
    __tablename__ = "carts"

    # Fields
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[String] = mapped_column(ForeignKey(
        "users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="cart")
    items: Mapped[Optional[list["CartItem"]]] = relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan"
    )
