from uuid import UUID
from flask import Blueprint, request, jsonify
from app.services.user_service import *
from app.models.user import User

bp = Blueprint("user_bp", __name__, url_prefix="/users")

@bp.route("/", methods=["POST"])
def create_user():
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
    # Get data from the request
    user_data = request.json

    # Create the user with a cart
    new_user = create_user_with_cart(user_data)

    return jsonify({"id": str(new_user.id), "message": "User created with cart!"}), 201

@bp.route("/", methods=["GET"])
def retrieve_all_users():
    """
    Endpoint to retrieve all users.

    Returns:
        Response: JSON response containing all users.
    """
    users = get_all_users()
    # Convert each user object to a dictionary representation
    users_data = [user.to_dict() for user in users]
    return jsonify(users_data), 200


@bp.route("/<user_id>", methods=["GET"])
def retrieve_user(user_id):
    """
    Endpoint to retrieve a single user by ID.

    Args:
        user_id: The ID of the user to retrieve.

    Returns:
        Response: JSON response containing the user's data or an error message.
    """
    user_id = UUID(user_id)
    user = get_user_by_id(user_id)
    return jsonify(user.to_dict()), 200


@bp.route("/<user_id>", methods=["PUT"])
def update_user_endpoint(user_id):
    """
    Endpoint to update a user's information.

    Args:
        user_id: The ID of the user to update.

    Returns:
        JSON response containing the updated user or an error message.
    """
    updated_data = request.json
    user_id = UUID(user_id)
    updated_user = update_user(user_id, updated_data)

    return jsonify(updated_user.to_dict()), 200


@bp.route("/<user_id>", methods=["DELETE"])
def delete_user_endpoint(user_id):
    """
    Endpoint to delete a user by ID.

    Args:
        user_id: The ID of the user to delete.

    Returns:
        JSON response indicating the result of the operation or an error message.
    """
    user_id = UUID(user_id)
    message = delete_user(user_id)
    return jsonify({"message": message}), 200
