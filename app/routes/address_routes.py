import traceback
from uuid import UUID
from flask import Blueprint, request, jsonify
from app.services.address_service import (
    create_address,
    get_user_addresses,
    # update_address,
    # delete_address
)
from app.services.auth_services import token_required


bp = Blueprint("address_bp", __name__, url_prefix="/addresses")

@bp.route("/", methods=["POST"])
def create_address_endpoint():
    """
    Endpoint to create a new address for a user.
    """
    try:
        data = request.json
        address = create_address(data)
        return jsonify({"message": "Address created successfully!", "address": address.to_dict()}), 201
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 400


@bp.route("/user/<user_id>", methods=["GET"])
@token_required
def get_addresses_endpoint(user_id):
    """
    Endpoint to get all addresses for a user.
    """
    try:
        addresses = get_user_addresses(user_id)
        return jsonify([address.to_dict() for address in addresses]), 200
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 400


# Route for future address update implementation
# @bp.route("/<address_id>", methods=["PUT"])
# @token_required
# def update_address_endpoint(address_id):
#     """
#     Endpoint to update an address.
#     """
#     try:
#         data = request.json
#         address_id = UUID(address_id)
#         updated_address = update_address(address_id, data)
#         return jsonify({"message": "Address updated successfully!", "address": updated_address.to_dict()}), 200
#     except Exception as e:
#         print(traceback.format_exc())
#         return jsonify({"error": str(e)}), 400


# Route for future address deletion implementation
# @bp.route("/<address_id>", methods=["DELETE"])
# @token_required
# def delete_address_endpoint(address_id):
#     """
#     Endpoint to delete an address.
#     """
#     try:
#         address_id = UUID(address_id)
#         delete_address(address_id)
#         return jsonify({"message": "Address deleted successfully!"}), 200
#     except Exception as e:
#         print(traceback.format_exc())
#         return jsonify({"error": str(e)}), 400