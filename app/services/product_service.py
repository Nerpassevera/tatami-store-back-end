from uuid import UUID
from app.models.product import Product
from app.db import db
from sqlalchemy.exc import SQLAlchemyError
from app.services.utility_functions import validate_model
from app.exceptions import ApplicationError


def get_all_products() -> list[Product]:
    """
    Retrieve all products from the database.

    Returns:
        list[Product]: A list of all products.
    """
    try:
        return db.session.query(Product).all()
    except SQLAlchemyError as e:
        raise ApplicationError(f"Error retrieving products: {str(e)}")


def get_product_by_id(product_id: UUID) -> Product:
    """
    Retrieve a single product by its ID.

    Args:
        product_id (UUID): The ID of the product.

    Returns:
        Product: The retrieved product.

    Raises:
        ApplicationError: If the product is not found.
    """
    return validate_model(product_id, Product)


def create_product(product_data: dict) -> Product:
    """
    Create a new product.

    Args:
        product_data (dict): Data for the new product.

    Returns:
        Product: The created product.
    """
    try:
        new_product = Product.from_dict(product_data)
        db.session.add(new_product)
        db.session.commit()
        return new_product
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ApplicationError(f"Error creating product: {str(e)}")


def update_product(product_id: UUID, product_data: dict) -> Product:
    """
    Update an existing product.

    Args:
        product_id (UUID): The ID of the product to update.
        product_data (dict): The new data for the product.

    Returns:
        Product: The updated product.
    """
    try:
        product = validate_model(product_id, Product)
        for key, value in product_data.items():
            if hasattr(product, key):
                setattr(product, key, value)
        db.session.commit()
        return product
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ApplicationError(f"Error updating product with ID {product_id}: {str(e)}")


def delete_product(product_id: UUID) -> str:
    """
    Delete a product by its ID.

    Args:
        product_id (UUID): The ID of the product to delete.

    Returns:
        str: A success message.
    """
    try:
        product = validate_model(product_id, Product)
        db.session.delete(product)
        db.session.commit()
        return f"Product with ID {product_id} has been deleted."
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ApplicationError(f"Error deleting product with ID {product_id}: {str(e)}")