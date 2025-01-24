"""
This module defines the User model and related components for the tatami-store-back-end application.

Classes:
    UserRole(PyEnum): Enum representing user roles in the system.
    User(db.Model): User model representing a user in the system.

Attributes:
    id (UUID): Primary key for the User model.
    email (str): Unique email address of the user.
    first_name (str): First name of the user.
    last_name (str): Last name of the user.
    street_address (Optional[str]): Street address of the user.
    role (UserRole): Role of the user in the system, default is UserRole.USER.
    phone (Optional[str]): Phone number of the user.
    orders (list[Order]): List of orders associated with the user.
    cart (Optional[Cart]): Cart associated with the user.

Methods:
    to_dict(self): Convert the User instance to a dictionary.
    from_dict(cls, data): Create a User instance from a dictionary of data.
    choices(cls): Class method for fetching all possible roles.
"""

from enum import Enum as PyEnum
from uuid import UUID, uuid4
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum
from app.db import db


if TYPE_CHECKING:
    from app.models.order import Order
    from app.models.cart import Cart


class UserRole(PyEnum):
    """
    Enum representing user roles in the system.
    """
    ADMIN = "Admin"
    USER = "User"


class User(db.Model):
    """
    User model representing a user in the system.
    """
    __tablename__ = "users"

    # Fields
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    street_address: Mapped[Optional[str]] = mapped_column(
        String, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), nullable=False, default=UserRole.USER)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    orders: Mapped[list["Order"]] = relationship(
        "Order", back_populates="user", lazy="dynamic")
    cart: Mapped[Optional["Cart"]] = relationship(
        "Cart", back_populates="user", uselist=False)

    # Methods
    def to_dict(self):
        """
        Convert the User instance to a dictionary.

        :return: A dictionary representation of the User instance.
        """
        return {
            "id": str(self.id),
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "street_address": self.street_address,
            "role": self.role.value,
            "phone": self.phone,
        }

    def __repr__(self):
        return f"<User {self.email}>"

    @classmethod
    def from_dict(cls, data):
        """
        Create a User instance from a dictionary of data.

        :param data: A dictionary containing user data.
        :return: A User instance.
        :raises ValueError: If a required field is missing or if the role value is invalid.
        """
        try:
            return cls(
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                street_address=data.get("street_address"),
                role=UserRole[data.get("role", "USER")],
                phone=data.get("phone"),
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}") from e
        except ValueError as e:
            raise ValueError(f"Invalid role value: {e}") from e

    @classmethod
    def role_choices(cls):
        """
        Class method for fetching all possible roles.
        """
        return [role.value for role in UserRole]
