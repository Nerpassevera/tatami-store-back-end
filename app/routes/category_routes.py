"""
This module defines the routes for category-related operations in the application.

Routes:
- GET /categories/:
    - retrieve_all_categories: Retrieve all categories.
- GET /categories/<category_id>:
    - retrieve_category: Retrieve a single category by its ID.

Commented Routes for future Admin portal implementation:
- POST /categories/:
    - create_category_endpoint: Create a new category.
- POST /categories/<product_id>/<category_id>:
    - assign_product_to_category: Assign a product to a category.
- PUT /categories/<category_id>:
    - update_category_endpoint: Update an existing category by its ID.
- DELETE /categories/<category_id>:
    - delete_category_endpoint: Delete a category by its ID.
"""

from uuid import UUID
from flask import Blueprint, jsonify
from app.services.category_service import (
    get_all_categories,
    get_category_by_id,
    # create_category,
    # update_category,
    # delete_category,
    # assign_category_to_product
)
from app.exceptions import ApplicationError
# from app.services.auth_services import token_required


bp = Blueprint("category_bp", __name__, url_prefix="/categories")


@bp.route("/", methods=["GET"])
def retrieve_all_categories():
    """
    Retrieve all categories.
    """
    try:
        categories = get_all_categories()
        categories_data = [category.to_dict() for category in categories]
        return jsonify(categories_data), 200
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Unexpected error occurred."}), 500


@bp.route("/<category_id>", methods=["GET"])
def retrieve_category(category_id):
    """
    Retrieve a single category by its ID.
    """
    try:
        category_id = UUID(category_id)
        category = get_category_by_id(category_id)
        return jsonify(category.to_dict()), 200
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Unexpected error occurred."}), 500


# Route for future Admin portal implementation
# @bp.route("/", methods=["POST"])
# @token_required
# def create_category_endpoint():
#     """
#     Create a new category.
#     """
#     try:
#         category_data = request.json
#         new_category = create_category(category_data)
#         return jsonify(new_category.to_dict()), 201
#     except ApplicationError as e:
#         return jsonify({"error": str(e)}), 400
#     except Exception:
#         return jsonify({"error": "Unexpected error occurred."}), 500


# Route for future Admin portal implementation
# @bp.route("/<product_id>/<category_id>", methods=["POST"])
# @token_required
# def assign_product_to_category(product_id, category_id):
#     """
#     Create a new category.
#     """
#     try:
#         product_id = UUID(product_id)
#         category_id = int(category_id)
#         confirmation = assign_category_to_product(product_id, category_id)
#         return confirmation, 201
#     except ApplicationError as e:
#         return jsonify({"error": str(e)}), 400
#     except Exception as e:
#         return jsonify({"error": "Unexpected error occurred - {e}"}), 500


# Route for future Admin portal implementation
# @bp.route("/<category_id>", methods=["PUT"])
# @token_required
# def update_category_endpoint(category_id):
#     """
#     Update an existing category by its ID.
#     """
#     try:
#         category_id = UUID(category_id)
#         category_data = request.json
#         updated_category = update_category(category_id, category_data)
#         return jsonify(updated_category.to_dict()), 200
#     except ApplicationError as e:
#         return jsonify({"error": str(e)}), 400
#     except Exception:
#         return jsonify({"error": "Unexpected error occurred."}), 500


# Route for future Admin portal implementation
# @bp.route("/<category_id>", methods=["DELETE"])
# @token_required
# def delete_category_endpoint(category_id):
#     """
#     Delete a category by its ID.
#     """
#     try:
#         category_id = UUID(category_id)
#         message = delete_category(category_id)
#         return jsonify({"message": message}), 200
#     except ApplicationError as e:
#         return jsonify({"error": str(e)}), 400
#     except Exception:
#         return jsonify({"error": "Unexpected error occurred."}), 500