from uuid import UUID
from flask import Blueprint, request, jsonify
from app.services.cart_service import (
    get_cart_items,
    add_item_to_cart,
    remove_item_from_cart,
    update_cart_item_quantity,
)
from app.exceptions import ApplicationError

bp = Blueprint("cart_bp", __name__, url_prefix="/cart")

@bp.route("/<user_id>", methods=["GET"])
def retrieve_cart_items(user_id):
    """
    Retrieve all items in the cart for a specific user.
    """
    try:
        cart_items = get_cart_items(user_id)
        return jsonify(cart_items), 200
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Unexpected error occurred."}), 500

@bp.route("/<user_id>", methods=["POST"])
def add_item_to_cart_endpoint(user_id):
    """
    Add an item to the user's cart.
    """
    try:
        data = request.json
        product_id = UUID(data.get("product_id"))
        quantity = data.get("quantity", 1)

        if not product_id or quantity <= 0:
            return jsonify({"error": "Invalid product_id or quantity."}), 400

        # Call the service which now returns the cart item details
        cart_item_data = add_item_to_cart(user_id, product_id, quantity)
        return jsonify(cart_item_data), 201
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Unexpected error occurred."}), 500

@bp.route("/<user_id>/<cart_item_id>", methods=["DELETE"])
def remove_item_from_cart_endpoint(user_id, cart_item_id):
    """
    Remove an item from the user's cart.
    """
    try:
        cart_item_id = UUID(cart_item_id)
        remove_item_from_cart(user_id, cart_item_id)
        return jsonify({"message": "Item removed from cart successfully!"}), 200
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Unexpected error occurred."}), 500

@bp.route("/<user_id>/<cart_item_id>", methods=["PATCH"])
def update_cart_item_quantity_endpoint(user_id, cart_item_id):
    """
    Update the quantity of an item in the user's cart.
    """
    try:
        cart_item_id = UUID(cart_item_id)
        data = request.json
        quantity = data.get("quantity")

        if quantity is None or quantity <= 0:
            return jsonify({"error": "Invalid quantity."}), 400

        update_cart_item_quantity(user_id, cart_item_id, quantity)
        return jsonify({"message": "Cart item quantity updated successfully!"}), 200
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Unexpected error occurred."}), 500