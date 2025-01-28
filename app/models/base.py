"""
This module defines the base class for SQLAlchemy models.

Classes:
    Base: A declarative base class for all SQLAlchemy models.
"""

from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import inspect


class Base(DeclarativeBase):
    __abstract__ = True  # Ensures this class is not mapped to a table

    @declared_attr
    def __tablename__(cls):
        """
        Automatically generates table names by pluralizing class names.
        You can customize the naming convention here.
        """
        return cls.__name__.lower() + "s"

    def to_dict(self):
        """
        Convert the model instance to a dictionary.
        This dynamically retrieves all columns and their values.
        """
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @classmethod
    def from_dict(cls, data):
        """
        Create an instance of the model from a dictionary.
        Automatically maps dictionary keys to model attributes.
        
        Args:
            data (dict): A dictionary containing the data to populate the instance.

        Returns:
            An instance of the class populated with the provided data.

        Raises:
            ValueError: If any required field is missing.
        """
        instance = cls()
        missing_fields = []

        # Check for required fields defined in the model
        for column in inspect(cls).mapper.column_attrs:
            column_name = column.key
            if column.info.get("required", False) and column_name not in data:
                missing_fields.append(column_name)

        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Set attributes from the provided data
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        return instance


    def __repr__(self):
        """
        String representation of the model for debugging purposes.
        """
        return f"<{self.__class__.__name__}(id={getattr(self, 'id', 'N/A')})>"