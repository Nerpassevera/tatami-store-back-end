from uuid import UUID
from flask import Blueprint, request, jsonify
from app.services.category_service import (
    get_all_categories,
    get_category_by_id,
    create_category,
    update_category,
    delete_category,
    assign_category_to_product
)
from app.exceptions import ApplicationError

bp = Blueprint("category_bp", __name__, url_prefix="/categories")


@bp.route("/", methods=["GET"])
def retrieve_all_categories():
    """
    Retrieve all categories.
    """
    try:
        categories = get_all_categories()
        categories_data = [category.to_dict() for category in categories]
        print("CAT", categories_data)
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


@bp.route("/", methods=["POST"])
def create_category_endpoint():
    """
    Create a new category.
    """
    try:
        category_data = request.json
        new_category = create_category(category_data)
        return jsonify(new_category.to_dict()), 201
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Unexpected error occurred."}), 500


@bp.route("/<product_id>/<category_id>", methods=["POST"])
def assign_product_to_category(product_id, category_id):
    """
    Create a new category.
    """
    try:
        product_id = UUID(product_id)
        category_id = int(category_id)
        confirmation = assign_category_to_product(product_id, category_id)
        return confirmation, 201
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Unexpected error occurred - {e}"}), 500


@bp.route("/<category_id>", methods=["PUT"])
def update_category_endpoint(category_id):
    """
    Update an existing category by its ID.
    """
    try:
        category_id = UUID(category_id)
        category_data = request.json
        updated_category = update_category(category_id, category_data)
        return jsonify(updated_category.to_dict()), 200
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Unexpected error occurred."}), 500


@bp.route("/<category_id>", methods=["DELETE"])
def delete_category_endpoint(category_id):
    """
    Delete a category by its ID.
    """
    try:
        category_id = UUID(category_id)
        message = delete_category(category_id)
        return jsonify({"message": message}), 200
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Unexpected error occurred."}), 500