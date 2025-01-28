"""
This module defines the Address model for the database.

Classes:
    Address: A SQLAlchemy model representing an address.

Methods:
    to_dict(self) -> dict:
        Converts the Address instance to a dictionary.

    __repr__(self) -> str:
        Returns a string representation of the Address instance.

    from_dict(cls, data: dict) -> 'Address':
        Creates an Address instance from a dictionary of data.
"""
from uuid import UUID
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

from app.db import db

if TYPE_CHECKING:
    from .user import User

class Address(db.Model):
    """
    Represents an address associated with a user.

    Attributes:
        id (int): The unique identifier for the address.
        user_id (UUID): The unique identifier for the user associated with the address.
        label (Optional[str]): An optional label for the address (e.g., "Home", "Work").
        house_number (str): The house number of the address.
        road (str): The road or street name of the address.
        city (str): The city of the address.
        state (str): The state of the address.
        postcode (str): The postal code of the address.
        country (str): The country of the address.
        user (User): The user associated with the address.

    Methods:
        to_dict(): Converts the address object to a dictionary.
        __repr__(): Returns a string representation of the address object.
        from_dict(data): Creates an address object from a dictionary. Raises ValueError if required fields are missing.
    """
    __tablename__ = "addresses"

    # Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    label: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    house_number: Mapped[str] = mapped_column(String, nullable=False)
    road: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False)
    postcode: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="addresses")

    # def to_dict(self):
    #     """
    #     Converts the Address object to a dictionary representation.

    #     Returns:
    #         dict: A dictionary containing the address details with the following keys:
    #             - id (int): The unique identifier of the address.
    #             - user_id (str): The unique identifier of the user as a string.
    #             - label (str): The label for the address.
    #             - house_number (str): The house number of the address.
    #             - road (str): The road name of the address.
    #             - city (str): The city of the address.
    #             - state (str): The state of the address.
    #             - postcode (str): The postal code of the address.
    #             - country (str): The country of the address.
    #     """
    #     return {
    #         "id": self.id,
    #         "user_id": str(self.user_id),
    #         "label": self.label,
    #         "house_number": self.house_number,
    #         "road": self.road,
    #         "city": self.city,
    #         "state": self.state,
    #         "postcode": self.postcode,
    #         "country": self.country,
    #     }

    # def __repr__(self):
    #     return f"<Address(id={self.id}, user_id={self.user_id}, city={self.city})>"

    # @classmethod
    # def from_dict(cls, data):
    #     """
    #     Create an instance of the class from a dictionary.

    #     Args:
    #         data (dict): A dictionary containing the data to create the instance. 
    #                      Must include the keys: "user_id", "house_number", "road", 
    #                      "city", "state", "postcode", and "country". Optional key: "label".

    #     Returns:
    #         cls: An instance of the class.

    #     Raises:
    #         ValueError: If any of the required keys are missing from the data dictionary.
    #     """
    #     for attr in ["user_id", "house_number", "road", "city", "state", "postcode", "country"]:
    #         if attr not in data:
    #             raise ValueError(f"Missing required field: {attr}")

    #     return cls(
    #         user_id=data["user_id"],
    #         label=data.get("label"),
    #         house_number=data["house_number"],
    #         road=data["road"],
    #         city=data["city"],
    #         state=data["state"],
    #         postcode=data["postcode"],
    #         country=data["country"]
    #     )
