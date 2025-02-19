"""
This module provides services for managing the user's shopping cart, including
retrieving cart items, adding items to the cart, removing items from the cart,
and updating the quantity of items in the cart.
Functions:
    get_cart_items(user_id: str) -> list[dict]:
    add_item_to_cart(user_id: str, product_id: UUID, quantity: int) -> dict:
    remove_item_from_cart(user_id: str, product_id: UUID) -> None:
    update_cart_item_quantity(user_id: str, product_id: UUID, quantity: int) -> None:
"""
from uuid import UUID
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.db import db
from app.services.utility_functions import validate_model
from app.exceptions import ApplicationError, StockError

def get_cart_items(user_id: str) -> list[dict]:
    """
    Retrieve all items in the user's cart.
    Args:
        user_id (str): The ID of the user.
    Returns:
        list[dict]: A list of dictionaries containing cart item details,
                    including the product's image URL.
    """
    try:
        cart_items = (
            db.session.query(
                CartItem.cart_id.label("cartID"),
                CartItem.product_id,
                CartItem.quantity,
                Product.name.label("product_name"),
                Product.price.label("product_price"),
                Product.image_url.label("image_url"),
                Product.stock.label("availableStock")
            )
            .join(Product, CartItem.product_id == Product.id)
            .filter(CartItem.cart.has(user_id=user_id))
            .all()
        )

        return [
            {
                "cartID": str(item.cartID),
                "productID": str(item.product_id),
                "title": item.product_name,
                "amount": item.quantity,
                "price": item.product_price.toString() if hasattr(item.product_price, "toString") else str(item.product_price),
                "image": item.image_url,
                "availableStock": item.availableStock
            }
            for item in cart_items
        ]
    except Exception as e:
        raise ApplicationError(f"Error retrieving cart items for user ID {user_id}:{str(e)}") from e


def add_item_to_cart(user_id: str, product_id: UUID, quantity: int) -> dict:
    """
    Add an item to the user's cart and return the updated cart item details.
    Args:
        user_id (str): The ID of the user.
        product_id (UUID): The ID of the product to add.
        quantity (int): The quantity of the product to add.
    Raises:
        StockError: If the requested quantity exceeds available stock.
    Returns:
        dict: A dictionary containing the updated cart item details.
    """
    try:
        product = validate_model(product_id, Product)

        if product.stock < quantity:
            raise StockError(product.name, quantity, product.stock)

        cart = db.session.query(Cart).filter_by(user_id=user_id).first()
        if not cart:
            raise ApplicationError("Cart not found for the user.")

        cart_item = db.session.query(CartItem).filter_by(
            cart_id=cart.id, product_id=product_id
        ).first()

        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)

        product.stock -= quantity
        db.session.add(product)

        db.session.commit()

        return {
            "cartID": str(cart_item.cart_id),
            "productID": str(cart_item.product_id),
            "amount": cart_item.quantity,
            "price": float(product.price)
        }
    except Exception as e:
        db.session.rollback()
        raise ApplicationError(f"Error adding item to cart: {str(e)}") from e


def remove_item_from_cart(user_id: str, product_id: UUID) -> None:
    """
    Remove an item from the user's cart by product ID.
    Args:
        user_id (str): The ID of the user.
        product_id (UUID): The ID of the product to remove from the cart.
    """
    try:
        cart = db.session.query(Cart).filter_by(user_id=user_id).first()
        if not cart:
            raise ApplicationError("Cart not found for the user.")

        cart_item = db.session.query(CartItem).filter_by(
            cart_id=cart.id, product_id=product_id
        ).first()
        if not cart_item:
            raise ApplicationError("Cart item not found for the given product.")

        product = validate_model(product_id, Product)
        db.session.add(product)

        db.session.delete(cart_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ApplicationError(f"Error removing item from cart: {str(e)}") from e


def update_cart_item_quantity(user_id: str, product_id: UUID, quantity: int) -> None:
    """
    Update the quantity of an item in the user's cart by product ID.
    Args:
        user_id (str): The ID of the user.
        product_id (UUID): The ID of the product to update in the cart.
        quantity (int): The new quantity of the cart item.
    Raises:
        StockError: If the requested quantity exceeds available stock.
    """
    try:
        cart = db.session.query(Cart).filter_by(user_id=user_id).first()
        if not cart:
            raise ApplicationError("Cart not found for the user.")

        cart_item = db.session.query(CartItem).filter_by(
            cart_id=cart.id, product_id=product_id
        ).first()
        if not cart_item:
            raise ApplicationError("Cart item not found for the given product.")

        product = validate_model(product_id, Product)

        stock_adjustment = quantity - cart_item.quantity

        if product.stock < stock_adjustment:
            raise StockError(product.name, quantity, product.stock)

        cart_item.quantity = quantity

        db.session.add(cart_item)
        db.session.add(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ApplicationError(f"Error updating cart item quantity: {str(e)}") from e
