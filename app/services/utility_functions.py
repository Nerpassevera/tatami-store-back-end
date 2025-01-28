from typing import Type
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from app.db import db
from app.models.base import Base
from app.exceptions import InstanceNotFoundError


def validate_model(instance_id: UUID, model: Type[Base]) -> Base:
    """
    Validate that a model instance exists in the database.

    Args:
        id (UUID): The ID of the model instance to validate.
        model (Type[Base]): The model class to query.

    Returns:
        Base: The model instance if it exists.

    Raises:
        Exception: If the model instance is not found.
    """
    try:
        instance = db.session.query(model).filter_by(id=instance_id).first()
        if not instance:
            raise InstanceNotFoundError(model, instance_id)
        return instance
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f"Error retrieving {model.__name__} with ID {instance_id}: {str(e)}") from e
