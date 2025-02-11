"""
This module defines the routes for user-related operations in the application.

Routes:
    - POST /users/:

    - GET /users/<user_id>:
        Retrieves a single user by ID.

    - GET /users/ (commented out for future implementation):
        Retrieves all users.
            Response: JSON response containing all users.

    - PUT /users/<user_id> (commented out for future implementation):
        Updates a user's information.
            user_id: The ID of the user to update.
            JSON response containing the updated user or an error message.

    - DELETE /users/<user_id> (commented out for future implementation):
        Deletes a user by ID.
            user_id: The ID of the user to delete.
            JSON response indicating the result of the operation or an error message.
"""
from flask import Blueprint, request, jsonify
from app.services.user_service import *
from app.services.auth_services import token_required

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
    user_data = request.json

    new_user = create_user_with_cart(user_data)

    return jsonify({"id": str(new_user.id), "message": "User created with cart!"}), 201

# Route for future Admin portal implementation
# @bp.route("/", methods=["GET"])
# @token_required
# def retrieve_all_users():
#     """
#     Endpoint to retrieve all users.

#     Returns:
#         Response: JSON response containing all users.
#     """
#     users = get_all_users()
#     users_data = [user.to_dict() for user in users]
#     return jsonify(users_data), 200


@bp.route("/<user_id>", methods=["GET"])
@token_required
def retrieve_user(user_id):
    """
    Endpoint to retrieve a single user by ID.

    Args:
        user_id: The ID of the user to retrieve.

    Returns:
        Response: JSON response containing the user's data or an error message.
    """
    user = get_user_by_id(user_id)
    return jsonify(user.to_dict()), 200


# Route for future user account update feature implementation
# @bp.route("/<user_id>", methods=["PUT"])
# @token_required
# def update_user_endpoint(user_id):
#     """
#     Endpoint to update a user's information.

#     Args:
#         user_id: The ID of the user to update.

#     Returns:
#         JSON response containing the updated user or an error message.
#     """
#     updated_data = request.json
#     updated_user = update_user(user_id, updated_data)

#     return jsonify(updated_user.to_dict()), 200


# Route for future user account deletion feature implementation
# @bp.route("/<user_id>", methods=["DELETE"])
# def delete_user_endpoint(user_id):
#     """
#     Endpoint to delete a user by ID.

#     Args:
#         user_id: The ID of the user to delete.

#     Returns:
#         JSON response indicating the result of the operation or an error message.
#     """
#     message = delete_user(user_id)
#     return jsonify({"message": message}), 200
