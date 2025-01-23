from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from uuid import UUID, uuid4
from app.db import db
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .user import User
    from .cart_item import CartItem


class Cart(db.Model):
    __tablename__ = "carts"

    # Fields
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="cart")
    items: Mapped[Optional[list["CartItem"]]] = relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan"
    )

    # Methods
    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "items": [item.to_dict() for item in self.items] if self.items else [],
        }

    def __repr__(self):
        return f"<Cart {self.id} - User ID: {self.user_id}>"

    @classmethod
    def from_dict(cls, data):
        try:
            return cls(
                user_id=data["user_id"],
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")