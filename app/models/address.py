from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Float

from app.db import db

if TYPE_CHECKING:
    from .user import User


class Address(db.Model):
    """
    Represents an address associated with a user.

    Attributes:
        id (int): Unique identifier for the address.
        user_id (str): Foreign key referencing the user this address belongs to.
        label (Optional[str]): Optional label for the address (e.g., "Home", "Work").
        house_number (str): House number of the address.
        street (str): Street name of the address.
        city (str): City of the address.
        state (str): State of the address.
        postcode (str): Postal code of the address.
        country (str): Country of the address.
        unit (Optional[str]): Optional unit or apartment number.
        latitude (Optional[float]): Latitude coordinate of the address.
        longitude (Optional[float]): Longitude coordinate of the address.

    Relationships:
        user (User): The user associated with this address.
    """

    __tablename__ = "addresses"

    # Fields
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    label: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    house_number: Mapped[str] = mapped_column(String, nullable=False)
    street: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False)
    postcode: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="addresses")
