"""
This module provides services for managing addresses in the application.
Functions:
    create_address(data: dict) -> Address:
    get_user_addresses(user_id) -> list[Address]:
    update_address(address_id: int, data: dict) -> Address:
    delete_address(address_id: int) -> None:
"""
from app.models.address import Address
from app.db import db
from app.services.utility_functions import validate_model
from app.exceptions import ApplicationError


def create_address(data: dict) -> Address:
    """
    Creates a new address for a user.
    Args:
        data (dict): Dictionary containing the address details.
    Returns:
        Address: The newly created address.
    """
    try:
        new_address = Address.from_dict(data)
        db.session.add(new_address)
        db.session.commit()
        return new_address
    except Exception as e:
        db.session.rollback()
        raise ApplicationError(f"Error creating address: {str(e)}") from e


def get_user_addresses(user_id) -> list[Address]:
    """
    Retrieves all addresses for a specific user.
    Args:
        user_id (UUID): The ID of the user.
    Returns:
        list[Address]: A list of addresses for the user.
    """
    try:
        return db.session.query(Address).filter_by(user_id=user_id).all()
    except Exception as e:
        raise ApplicationError(
            f"Error retrieving addresses for user ID {user_id}: {str(e)}") from e


def update_address(address_id: int, data: dict) -> Address:
    """
    Updates an existing address.
    Args:
        address_id (int): The ID of the address to update.
        data (dict): A dictionary containing the updated fields.
    Returns:
        Address: The updated address.
    """
    try:
        address = validate_model(address_id, Address)
        for key, value in data.items():
            if hasattr(address, key):
                setattr(address, key, value)
        db.session.commit()
        return address
    except Exception as e:
        db.session.rollback()
        raise ApplicationError(
            f"Error updating address ID {address_id}: {str(e)}") from e


def delete_address(address_id: int) -> None:
    """
    Deletes an address by its ID.
    Args:
        address_id (int): The ID of the address to delete.
    """
    try:
        address = validate_model(address_id, Address)
        db.session.delete(address)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ApplicationError(
            f"Error deleting address ID {address_id}: {str(e)}") from e
