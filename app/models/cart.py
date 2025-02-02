"""
Cart model representing a shopping cart in the database.

Attributes:
    id (UUID): Primary key, unique identifier for the cart.
    user_id (String): Foreign key referencing the user who owns the cart.
    user (User): Relationship to the User model.
    items (Optional[list[CartItem]]): Relationship to the CartItem model, representing items in the cart.

Methods:
    to_dict() -> dict:
        Converts the Cart instance to a dictionary representation.
    
    __repr__() -> str:
        Returns a string representation of the Cart instance.
    
    from_dict(cls, data: dict) -> 'Cart':
        Creates a Cart instance from a dictionary of data.
        Args:
            data (dict): Dictionary containing the user_id.
        Raises:
            ValueError: If the required field 'user_id' is missing.
"""

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
    Represents a shopping cart in the database.

    Attributes:
        id (UUID): The unique identifier for the cart.
        user_id (String): The unique identifier for the user associated with the cart.
        user (User): The user associated with the cart.
        items (Optional[list[CartItem]]): The list of items in the cart.

    Methods:
        to_dict(): Converts the cart instance to a dictionary.
        __repr__(): Returns a string representation of the cart instance.
        from_dict(data): Creates a cart instance from a dictionary.

    Raises:
        ValueError: If a required field is missing in the data dictionary.
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

    # Methods
    # def to_dict(self):
    #     """
    #     Converts the Cart object to a dictionary representation.

    #     Returns:
    #         dict: A dictionary containing the cart's id, user_id, and a list of items.
    #               The 'id' and 'user_id' are converted to strings, and 'items' is a list
    #               of dictionaries representing each item in the cart. If there are no items,
    #               an empty list is returned.
    #     """
    #     return {
    #         "id": str(self.id),
    #         "user_id": str(self.user_id),
    #         "items": [item.to_dict() for item in self.items] if self.items else [],
    #     }

    # def __repr__(self):
    #     return f"<Cart {self.id} - User ID: {self.user_id}>"

    # @classmethod
    # def from_dict(cls, data):
    #     """
    #     Create an instance of the class from a dictionary.

    #     Args:
    #         data (dict): A dictionary containing the data to create the instance.

    #     Returns:
    #         An instance of the class.

    #     Raises:
    #         ValueError: If a required field is missing from the dictionary.
    #     """
    #     try:
    #         return cls(
    #             user_id=data["user_id"],
    #         )
    #     except KeyError as e:
    #         raise ValueError(f"Missing required field: {e}") from e
