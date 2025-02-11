from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Integer, Boolean

from app.db import db

if TYPE_CHECKING:
    from .order_item import OrderItem
    from .cart_item import CartItem
    from .product_category import ProductCategory


class Product(db.Model):
    """
    Represents a product in the store.
    Attributes:
        id (UUID): The unique identifier for the product.
        name (str): The name of the product. Must be unique and not null.
        description (str): A description of the product. Can be null.
        price (float): The price of the product. Must not be null.
        stock (int): The number of items in stock. Must not be null.
        image_url (str): The URL of the product's image. Can be null.
        is_active (bool): Indicates whether the product is active. Defaults to True and must not be null.
    Relationships:
        order_items (list[OrderItem]): The order items associated with the product.
        cart_items (list[CartItem]): The cart items associated with the product.
        categories (list[ProductCategory]): The categories associated with the product.
    """
    __tablename__ = "products"

    # Fields
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str] = mapped_column(String(2048), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)

    # Relationships
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="product", lazy="dynamic", cascade=None
    )
    cart_items: Mapped[list["CartItem"]] = relationship(
        "CartItem", back_populates="product", lazy="dynamic", cascade="all, delete"
    )
    categories: Mapped[list["ProductCategory"]] = relationship(
        "ProductCategory", back_populates="product", lazy="select", cascade="all, delete"
    )
