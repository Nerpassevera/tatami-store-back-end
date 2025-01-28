from uuid import UUID
from flask import Blueprint, request, jsonify
from app.services.product_service import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
)
from app.exceptions import ApplicationError

bp = Blueprint("product_bp", __name__, url_prefix="/products")


@bp.route("/", methods=["GET"])
def retrieve_all_products():
    """
    Retrieve all products.
    """
    try:
        products = get_all_products()
        products_data = [product.to_dict() for product in products]
        return jsonify(products_data), 200
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Unexpected error occurred."}), 500


@bp.route("/<product_id>", methods=["GET"])
def retrieve_product(product_id):
    """
    Retrieve a single product by its ID.
    """
    try:
        product_id = UUID(product_id)
        product = get_product_by_id(product_id)
        return jsonify(product.to_dict()), 200
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Unexpected error occurred."}), 500


@bp.route("/", methods=["POST"])
def create_product_endpoint():
    """
    Create a new product.
    """
    try:
        product_data = request.json
        new_product = create_product(product_data)
        return jsonify(new_product.to_dict()), 201
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Unexpected error occurred."}), 500


@bp.route("/<product_id>", methods=["PUT"])
def update_product_endpoint(product_id):
    """
    Update an existing product by its ID.
    """
    try:
        product_id = UUID(product_id)
        product_data = request.json
        updated_product = update_product(product_id, product_data)
        return jsonify(updated_product.to_dict()), 200
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Unexpected error occurred."}), 500


@bp.route("/<product_id>", methods=["DELETE"])
def delete_product_endpoint(product_id):
    """
    Delete a product by its ID.
    """
    try:
        product_id = UUID(product_id)
        message = delete_product(product_id)
        return jsonify({"message": message}), 200
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Unexpected error occurred."}), 500