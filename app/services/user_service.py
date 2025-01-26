from uuid import UUID
from datetime import datetime
from app.models.user import User, UserRole
from app.models.cart import Cart
from app.db import db  # SQLAlchemy session

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
    print(user_data)
    try:
        # Start a transaction
        with db.session.begin():
            # Create the user
            # new_user = User(**user_data, role=role)
            new_user = User.from_dict(user_data)
            print(new_user.to_dict())
            db.session.add(new_user)

            # Create a cart for the user
            user_cart = Cart(user_id=new_user.id)
            db.session.add(user_cart)

        return new_user
    except Exception as e:
        db.session.rollback()
        raise e


def get_all_users() -> list[User]:
    """
    Retrieves all users from the database.

    Returns:
        list[User]: A list of all users in the database.
    """
    try:
        users = db.session.query(User).all()
        return users
    except Exception as e:
        raise Exception(f"Error retrieving users: {str(e)}")


def get_user_by_id(user_id: UUID) -> User:
    """
    Retrieves a single user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The retrieved user.

    Raises:
        Exception: If the user is not found or another error occurs.
    """
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            raise Exception(f"User with ID {user_id} not found.")
        return user
    except Exception as e:
        raise Exception(f"Error retrieving user with ID {user_id}: {str(e)}")


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
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            raise Exception(f"User with ID {user_id} not found.")

        for key, value in updated_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        db.session.commit()
        return user
    except Exception as e:
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
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            raise Exception(f"User with ID {user_id} not found.")

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