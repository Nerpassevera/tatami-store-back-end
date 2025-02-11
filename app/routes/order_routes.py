from uuid import UUID
from flask import Blueprint, request, jsonify
from app.services.order_service import (
    get_cart_items_with_prices,
    place_order,
    get_user_orders,
    change_order_status
)
from app.exceptions import ApplicationError
from app.services.auth_services import token_required


bp = Blueprint("order_bp", __name__, url_prefix="/orders")


@bp.route("/cart-items/<user_id>", methods=["GET"])
@token_required
def retrieve_cart_items(user_id):
    """
    Retrieve all cart items for a user along with their respective product prices.

    Args:
        user_id (String): The ID of the user.

    Returns:
        JSON response containing cart items or an error message.
    """
    try:
        cart_items = get_cart_items_with_prices(user_id)
        return jsonify(cart_items), 200
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": f"Unexpected error occurred - {e}"}), 500


@bp.route("/", methods=["POST"])
@token_required
def create_order():
    """
    Place an order for a user.

    Request Body:
        - user_id (str): The ID of the user placing the order.
        - address_id (int): The ID of the delivery address.

    Returns:
        JSON response with order details or an error message.
    """
    try:
        data = request.json
        user_id = data.get("user_id").strip()
        address_id = data.get("address_id")

        if not user_id or not address_id:
            return jsonify({"error": "Missing user_id or address_id."}), 400

        new_order = place_order(user_id, address_id)
        return jsonify({"order_id": str(new_order.id), "message": "Order placed successfully!"}), 201
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except ValueError:
        return jsonify({"error": "Unexpected value error occurred."}), 500
    except TypeError:
        return jsonify({"error": "Unexpected type error occurred."}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error occurred - {e}"}), 500


@bp.route("/<user_id>", methods=["GET"])
@token_required
def retrieve_user_orders(user_id):
    """
    Retrieve all orders for a specific user with optional filters.

    Query Parameters:
        - start_date (str): Filter by orders placed after this date (ISO format).
        - end_date (str): Filter by orders placed before this date (ISO format).
        - min_total (float): Filter by minimum total amount.
        - max_total (float): Filter by maximum total amount.
        - status (str): Filter by order status.
        - order_by (str): Field to order results by (default: "order_date").
        - order_direction (str): "asc" for ascending, "desc" for descending (default: "desc").

    Returns:
        JSON response with the user's orders or an error message.
    """
    try:
        # Extract filters from query parameters
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        min_total = request.args.get("min_total", type=float)
        max_total = request.args.get("max_total", type=float)
        status = request.args.get("status")
        order_by = request.args.get("order_by", "order_date")
        order_direction = request.args.get("order_direction", "desc")

        orders = get_user_orders(
            user_id,
            start_date=start_date,
            end_date=end_date,
            min_total=min_total,
            max_total=max_total,
            status=status,
            order_by=order_by,
            order_direction=order_direction,
        )

        return jsonify(orders), 200
    except ApplicationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error occurred - {e}"}), 500


# Route for future Admin portal implementation
# @bp.route("/<order_id>/status", methods=["PATCH"])
# @token_required
# def update_order_status(order_id):
#     """
#     Update the status of an order.

#     Request Body:
#         - new_status (str): The new status for the order.

#     Returns:
#         JSON response with the updated order details or an error message.
#     """
#     try:
#         data = request.json
#         new_status = data.get("new_status")

#         if not new_status:
#             return jsonify({"error": "Missing new_status in request body."}), 400

#         order_id = UUID(order_id)
#         updated_order = change_order_status(order_id, new_status)
#         return jsonify({
#             "order_id": str(updated_order.id),
#             "new_status": updated_order.status.value,
#             "message": "Order status updated successfully!"
#         }), 200
#     except ApplicationError as e:
#         return jsonify({"error": str(e)}), 400
#     except Exception as e:
#         return jsonify({"error": f"Unexpected error occurred - {e}"}), 500
