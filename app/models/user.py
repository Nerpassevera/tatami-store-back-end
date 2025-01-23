from enum import Enum as PyEnum
from uuid import UUID, uuid4
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum
from app.db import db

# if TYPE_CHECKING:
    # from .order import Order
    # from .cart import Cart


class UserRole(PyEnum):
    ADMIN = "Admin"
    USER = "User"


class User(db.Model):
    __tablename__ = "users"

    # Fields
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    street_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
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
            raise ValueError(f"Missing required field: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid role value: {e}")

    # class method for fetching all possible roles
    @classmethod
    def choices(cls):
        return [role.value for role in cls]
