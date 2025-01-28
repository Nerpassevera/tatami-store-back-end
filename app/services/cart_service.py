from uuid import UUID
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.db import db
from app.services.utility_functions import validate_model
from app.exceptions import ApplicationError, StockError, EmptyCartError


def get_cart_items(user_id: UUID) -> list[dict]:
    """
    Retrieve all items in the user's cart.

    Args:
        user_id (UUID): The ID of the user.

    Returns:
        list[dict]: A list of dictionaries containing cart item details.
    """
    try:
        cart_items = (
            db.session.query(
                CartItem.id.label("cart_item_id"),
                CartItem.product_id,
                CartItem.quantity,
                Product.name.label("product_name"),
                Product.price.label("product_price")
            )
            .join(Product, CartItem.product_id == Product.id)
            .filter(CartItem.cart.has(user_id=user_id))
            .all()
        )

        return [
            {
                "cart_item_id": item.cart_item_id,
                "product_id": item.product_id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "price": float(item.product_price),
                "total_price": float(item.product_price) * item.quantity
            }
            for item in cart_items
        ]
    except Exception as e:
        raise ApplicationError(f"Error retrieving cart items for user ID {user_id}: {str(e)}")


def add_item_to_cart(user_id: UUID, product_id: UUID, quantity: int) -> None:
    """
    Add an item to the user's cart.

    Args:
        user_id (UUID): The ID of the user.
        product_id (UUID): The ID of the product to add.
        quantity (int): The quantity of the product to add.

    Raises:
        StockError: If the requested quantity exceeds available stock.
    """
    try:
        # Validate the product exists
        product = validate_model(product_id, Product)

        # Check stock availability
        if product.stock < quantity:
            raise StockError(product.name, quantity, product.stock)

        # Retrieve or create the cart for the user
        cart = db.session.query(Cart).filter_by(user_id=user_id).first()
        if not cart:
            raise ApplicationError("Cart not found for the user.")

        # Check if the product already exists in the cart
        cart_item = db.session.query(CartItem).filter_by(
            cart_id=cart.id, product_id=product_id
        ).first()

        if cart_item:
            # Update the quantity if the item already exists
            cart_item.quantity += quantity
        else:
            # Create a new cart item
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)

        # Update the stock for the product
        product.stock -= quantity
        db.session.add(product)

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise ApplicationError(f"Error adding item to cart: {str(e)}")


def remove_item_from_cart(user_id: UUID, cart_item_id: UUID) -> None:
    """
    Remove an item from the user's cart.

    Args:
        user_id (UUID): The ID of the user.
        cart_item_id (UUID): The ID of the cart item to remove.
    """
    try:
        # Validate the cart item exists
        cart_item = validate_model(cart_item_id, CartItem)

        # Ensure the cart item belongs to the user's cart
        if not cart_item.cart or cart_item.cart.user_id != user_id:
            raise ApplicationError("Cart item does not belong to the user cart.")

        # Restore the stock for the product
        product = validate_model(cart_item.product_id, Product)
        product.stock += cart_item.quantity
        db.session.add(product)

        # Remove the cart item
        db.session.delete(cart_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ApplicationError(f"Error removing item from cart: {str(e)}")


def update_cart_item_quantity(user_id: UUID, cart_item_id: UUID, quantity: int) -> None:
    """
    Update the quantity of an item in the user's cart.

    Args:
        user_id (UUID): The ID of the user.
        cart_item_id (UUID): The ID of the cart item to update.
        quantity (int): The new quantity of the cart item.

    Raises:
        StockError: If the requested quantity exceeds available stock.
    """
    try:
        # Validate the cart item exists
        cart_item = validate_model(cart_item_id, CartItem)

        # Ensure the cart item belongs to the user's cart
        if not cart_item.cart or cart_item.cart.user_id != user_id:
            raise ApplicationError("Cart item does not belong to the user.")

        # Get the associated product
        product = validate_model(cart_item.product_id, Product)

        # Calculate the stock adjustment
        stock_adjustment = quantity - cart_item.quantity

        # Check stock availability
        if product.stock < stock_adjustment:
            raise StockError(product.name, quantity, product.stock)

        # Update the cart item quantity and product stock
        cart_item.quantity = quantity
        product.stock -= stock_adjustment

        db.session.add(cart_item)
        db.session.add(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ApplicationError(f"Error updating cart item quantity: {str(e)}")