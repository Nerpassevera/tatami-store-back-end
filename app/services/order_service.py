from uuid import UUID
from datetime import datetime
from sqlalchemy import asc, desc
from sqlalchemy.orm import joinedload
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.address import Address
from app.db import db
from app.services.utility_functions import validate_model
from app.exceptions import ApplicationError, StockError, EmptyCartError, AddressOwnershipError, StatusError


def get_cart_items_with_prices(user_id: UUID) -> list[dict]:
    """
    Retrieves all cart items for a user along with their respective product prices.

    Args:
        user_id (UUID): The ID of the user.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains
                    cart item details and the corresponding product price.
    """
    try:
        cart_items = (
            db.session.query(
                CartItem.cart_id,
                CartItem.product_id,
                CartItem.quantity,
                Product.price
            )
            .join(Product, CartItem.product_id == Product.id)
            .filter(CartItem.cart.has(user_id=user_id))  # Filter by user's cart
            .all()
        )

        # Convert the results into a list of dictionaries
        return [
            {
                "cart_id": item.cart_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price
            }
            for item in cart_items
        ]
    except Exception as e:
        raise ApplicationError(f"Error retrieving cart items for user ID {user_id}: {str(e)}") from e


def place_order(user_id: UUID, address_id: int) -> Order:
    """
    Places an order for a user. Creates an order, removes items from the user's cart,
    and adjusts stock quantities for the ordered products.

    Args:
        user_id (UUID): The ID of the user placing the order.

    Returns:
        Order: The created order.

    Raises:
        Exception: If the user's cart is empty, a product is out of stock, or other errors occur.
    """
    
    try:
        # Start the transaction
        print("Session beggins ...")
        with db.session.begin():
            address = validate_model(address_id, Address)
            print(f"Address: {address}")
            print("Validating address ownership ...", address.user_id != user_id)
            if address.user_id != user_id:
                raise AddressOwnershipError(address.id, user_id)

            # Fetch the user's cart with item prices
            items_with_prices = get_cart_items_with_prices(user_id)
            print(items_with_prices)

            if not items_with_prices:
                raise EmptyCartError(user_id)
            # Calculate the total amount
            total_amount = sum(item['price'] * item['quantity'] for item in items_with_prices)
            print(f"Total amount: {total_amount}")

            # Create the order
            new_order = Order.from_dict(
                {"user_id": user_id, "total_amount": total_amount, "address_id": address.id})
            print(f"New order: {new_order.to_dict()}")
            db.session.add(new_order)
            db.session.flush()

            for item in items_with_prices:
                # Validate the product exists and get the product instance
                product = validate_model(item['product_id'], Product)

                # Check stock availability
                if product.stock < item["quantity"]:
                    raise StockError(product.name, item["quantity"], product.stock)

                # Create order item
                order_item = OrderItem.from_dict({
                    "order_id": new_order.id,
                    "product_id": product.id,
                    "quantity": item["quantity"],
                    "price": product.price
                })
                db.session.add(order_item)

                # Subtract stock
                product.stock -= item["quantity"]
                db.session.add(product)

            # Clear the user's cart
            cart_id = items_with_prices[0]["cart_id"]
            db.session.query(CartItem).filter_by(cart_id=cart_id).delete()

            db.session.commit()
            return new_order

    except Exception as e:
        db.session.rollback()
        raise ApplicationError(f"Error placing order for user ID {user_id}: {str(e)}") from e


def get_user_orders(
    user_id: UUID,
    start_date: datetime = None,
    end_date: datetime = None,
    min_total: float = None,
    max_total: float = None,
    status: str = None,
    order_by: str = "order_date",  # Default sorting by order_date
    order_direction: str = "desc"  # Default sorting direction is descending
) -> list[dict]:
    """
    Retrieves all orders placed by a specific user with optional filters and ordering.

    Args:
        user_id (UUID): The ID of the user whose orders are to be retrieved.
        start_date (datetime, optional): Filter by orders placed after this date.
        end_date (datetime, optional): Filter by orders placed before this date.
        min_total (float, optional): Filter by minimum total amount.
        max_total (float, optional): Filter by maximum total amount.
        status (str, optional): Filter by order status.
        order_by (str, optional): Field to order results by (e.g., "order_date", "total_amount").
        order_direction (str, optional): "asc" for ascending, "desc" for descending.

    Returns:
        list[dict]: A list of dictionaries containing order details.
    """
    try:
        # Base query for orders
        query = (
            db.session.query(Order)
            .filter_by(user_id=user_id)
            .options(joinedload(Order.order_items).joinedload(OrderItem.product))
        )

        # Apply filters if provided
        if start_date:
            query = query.filter(Order.order_date >= start_date)
        if end_date:
            query = query.filter(Order.order_date <= end_date)
        if min_total:
            query = query.filter(Order.total_amount >= min_total)
        if max_total:
            query = query.filter(Order.total_amount <= max_total)
        if status:
            query = query.filter(Order.status == status)

        # Apply ordering
        order_column = getattr(Order, order_by, None)
        if not order_column:
            raise ValueError(f"Invalid order_by field: {order_by}")
        if order_direction == "asc":
            query = query.order_by(asc(order_column))
        elif order_direction == "desc":
            query = query.order_by(desc(order_column))
        else:
            raise ValueError(f"Invalid order_direction: {order_direction}")

        # Execute the query
        orders = query.all()

        # Process and structure the orders
        orders_data = []
        for order in orders:
            order_data = {
                "order_id": str(order.id),
                "user_id": str(order.user_id),
                "address_id": order.address_id,
                "total_amount": float(order.total_amount),
                "order_date": order.order_date.isoformat(),
                "status": order.status.value,
                "items": [
                    {
                        "product_id": str(item.product_id),
                        "product_name": item.product.name,
                        "quantity": item.quantity,
                        "price": float(item.price),
                    }
                    for item in order.order_items
                ],
            }
            orders_data.append(order_data)

        return orders_data
    except Exception as e:
        raise ApplicationError(f"Error retrieving orders for user ID {user_id}: {str(e)}") from e


def change_order_status(order_id: UUID, new_status: str) -> Order:

            # Validate the new status
    if new_status not in OrderStatus.__members__:
        raise StatusError(new_status)

    with db.session.begin():
        # Retrieve the order
        order = validate_model(order_id, Order)
        if order.status == OrderStatus.PENDING and new_status.upper() == "CANCELLED":
            # If the order is pending and being cancelled, restock the products
            for item in order.order_items:
                product = validate_model(item.product_id, Product)
                product.stock += item.quantity
                db.session.add(product)

        elif order.status in {OrderStatus.CANCELED, OrderStatus.COMPLETED}:
            raise StatusError(order.status, new_status)

        order.status = OrderStatus[new_status]
        db.session.commit()

    return order
