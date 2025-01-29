"""
This module provides services for managing users in the application, including creating users with carts,
retrieving users, updating user information, and deleting users with specific behaviors based on their roles.

Functions:
    create_user_with_cart(user_data: dict, role: str = "User") -> User:

    get_all_users() -> list[User]:

    get_user_by_id(user_id: UUID) -> User:

    update_user(user_id: UUID, updated_data: dict) -> User:

    delete_user(user_id: UUID) -> str:
"""

from uuid import UUID
from datetime import datetime
from app.models.user import User, UserRole
from app.models.cart import Cart
from app.db import db
from app.services.utility_functions import validate_model
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID

def create_user_with_cart(user_data: dict, role: str = "User") -> User:
    """
    Creates a new user with the specified role and automatically creates a cart for them.

    Args:
        user_data (dict): Data for creating the user (name, email, password, etc.).
        role (str): The user's role (default is "User").

    Returns:
        User: The created user with an associated cart.

    Raises:
        Exception: In case of a failed transaction.
    """
    try:
        # Start a transaction
        with db.session.begin():
            # Create the user
            new_user = User.from_dict(user_data)
            db.session.add(new_user)

            # Create a cart for the user
            user_cart = Cart(user_id=new_user.id)
            db.session.add(user_cart)

        return new_user

    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error creating user with cart: {str(e)}")


def get_all_users(active_only: bool = False, limit: int = None) -> list[User]:
    """
    Retrieve a list of users from the database.

    Args:
        active_only (bool): If True, only retrieve active users. Defaults to False.
        limit (int): The maximum number of users to retrieve. If None, retrieve all users. Defaults to None.

    Returns:
        list[User]: A list of User objects.

    Raises:
        Exception: If there is an error retrieving users from the database.
    """
    try:
        query = db.session.query(User)
        if active_only:
            query = query.filter_by(is_active=True)
        if limit:
            query = query.limit(limit)
        return query.all()
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving users: {str(e)}")


def get_user_by_id(user_id: UUID) -> User:  # Rewrite this function!
    """
    Retrieves a single user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The retrieved user.

    Raises:
        Exception: If the user is not found or another error occurs.
    """
    return validate_model(user_id, User)


def update_user(user_id: UUID, updated_data: dict) -> User:
    """
    Updates a user's information in the database.

    Args:
        user_id (UUID): The ID of the user to update.
        updated_data (dict): A dictionary containing the fields to update and their new values.

    Returns:
        User: The updated user.

    Raises:
        Exception: If the user is not found or another error occurs.
    """
    try:
        user = validate_model(user_id, User)
        print("initial user id: ", user.id)

        for key, value in updated_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        print("user id after update: ", user.id)
        db.session.commit()
        return user
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error updating user with ID {user_id}: {str(e)}")


def delete_user(user_id: UUID) -> str:
    """
    Deletes a user from the database with specific behavior based on their role.

    - If the user's role is 'Admin', deletion is blocked.
    - If the user's role is 'User', anonymizes their data, sets `is_active` to False, and deletes their cart.

    Args:
        user_id (UUID): The ID of the user to delete.

    Returns:
        str: A message indicating the result of the operation.

    Raises:
        Exception: If the user is not found or another error occurs.
    """
    try:
        user = validate_model(user_id, User)

        # Block deletion if the user is an Admin
        if user.role == UserRole.ADMIN:
            raise Exception("Cannot delete a user with the 'Admin' role.")

        # Anonymize user data if the role is 'User'
        if user.role == UserRole.USER:
            user.first_name = "Deleted"
            user.last_name = "User"
            user.email = f"deleted_user_{user.id}@example.com"
            user.street_address = "N/A"
            user.phone = "000-000-0000"
            user.is_active = False
            user.deleted_at = datetime.now()

            # Delete the user's cart
            cart = db.session.query(Cart).filter_by(user_id=user.id).first()
            db.session.delete(cart)

            # Commit the changes
            db.session.add(user)
            db.session.commit()

        return f"User with ID {user_id} has been anonymized and deactivated."
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error deleting user with ID {user_id}: {str(e)}")
