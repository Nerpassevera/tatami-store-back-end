from enum import Enum as PyEnum
from typing import TYPE_CHECKING, Optional
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, Boolean, DateTime

from app.db import db

if TYPE_CHECKING:
    from app.models.order import Order
    from app.models.cart import Cart
    from app.models.address import Address


class UserRole(PyEnum):
    """
    Enum representing user roles in the system.
    """
    ADMIN = "Admin"
    USER = "User"


class User(db.Model):
    """
    User model representing a user in the system.
    Attributes:
        id (str): The unique identifier for the user.
        email (str): The email address of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        role (UserRole): The role of the user, default is UserRole.USER.
        phone (Optional[str]): The phone number of the user, nullable.
        is_active (bool): Indicates if the user is active, default is True.
        deleted_at (Optional[DateTime]): The timestamp when the user was deleted, nullable.
    Relationships:
        orders (list[Order]): The list of orders associated with the user.
        cart (Optional[Cart]): The cart associated with the user, if any.
        addresses (list[Address]): The list of addresses associated with the user.
    Methods:
        to_dict: Converts the User instance to a dictionary.
        from_dict: Creates a User instance from a dictionary of data.
    """

    __tablename__ = "users"

    # Fields
    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), nullable=False, default=UserRole.USER)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime, nullable=True)

    # Relationships
    orders: Mapped[list["Order"]] = relationship(
        "Order", back_populates="user", lazy="dynamic")
    cart: Mapped[Optional["Cart"]] = relationship(
        "Cart", back_populates="user", uselist=False)
    addresses: Mapped[list["Address"]] = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan")

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
            "role": self.role.value,
            "phone": self.phone,
            "is_active": self.is_active,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None
        }

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
                id=data["cognito_id"],
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                role=UserRole[data.get("role", "USER").upper()],
                phone=data.get("phone"),
                is_active=data.get("is_active", True),
                deleted_at=datetime.fromisoformat(
                    data["deleted_at"]) if data.get("deleted_at") else None
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}") from e
        except ValueError as e:
            raise ValueError(f"Invalid role value: {e}") from e

    # For future use
    # @classmethod
    # def role_choices(cls):
    #     """
    #     Class method for fetching all possible roles.
    #     """
    #     return [role.value for role in UserRole]
