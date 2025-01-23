from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer
from uuid import UUID, uuid4
from app.db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cart import Cart
    from .product import Product


class CartItem(db.Model):
    __tablename__ = "cart_items"

    # Fields
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    cart_id: Mapped[UUID] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    product: Mapped["Product"] = relationship("Product")

    # Methods
    def to_dict(self):
        return {
            "id": str(self.id),
            "cart_id": str(self.cart_id),
            "product_id": str(self.product_id),
            "quantity": self.quantity,
            "product_details": self.product.to_dict() if self.product else None,
        }

    def __repr__(self):
        return f"<CartItem {self.id} - Cart ID: {self.cart_id}, Product ID: {self.product_id}>"

    @classmethod
    def from_dict(cls, data):
        try:
            return cls(
                cart_id=data["cart_id"],
                product_id=data["product_id"],
                quantity=data["quantity"],
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")