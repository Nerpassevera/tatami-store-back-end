"""
This module provides services for managing categories in the database.

Functions:
    - get_all_categories() -> list[Category]:
    - get_category_by_id(category_id: UUID) -> Category:
    - assign_category_to_product(product_id: UUID, category_id: UUID) -> str:
    - create_category(category_data: dict) -> Category:
    - update_category(category_id: UUID, category_data: dict) -> Category:
    - delete_category(category_id: UUID) -> str:

"""

from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError

from app.models.category import Category
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.db import db
from app.services.utility_functions import validate_model
from app.exceptions import ApplicationError


def get_all_categories() -> list[Category]:
    """
    Retrieve all categories from the database.
    Returns:
        list[Category]: A list of all categories.
    """
    try:
        return db.session.query(Category).all()
    except SQLAlchemyError as e:
        raise ApplicationError(f"Error retrieving categories: {str(e)}")


def get_category_by_id(category_id: UUID) -> Category:
    """
    Retrieve a single category by its ID.
    Args:
        category_id (UUID): The ID of the category.
    Returns:
        Category: The retrieved category.
    """
    return validate_model(category_id, Category)


def assign_category_to_product(product_id: UUID, category_id: UUID) -> str:
    """
    Assign a category to a product.
    Args:
        product_id (UUID): The ID of the product.
        category_id (int): The ID of the category.
    Returns:
        str: A success message.
    """
    try:
        product = validate_model(product_id, Product)
        category = validate_model(category_id, Category)
        product_category = ProductCategory(
            product_id=product_id, category_id=category_id)
        db.session.add(product_category)
        db.session.commit()

        category_name = category.to_dict()['name']
        product_name = product.to_dict()['name']
        return f"Category \"{category_name}\" assigned to product \"{product_name}\"."
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ApplicationError(
            f"Error assigning category to product: {str(e)}") from e


def create_category(category_data: dict) -> Category:
    """
    Create a new category.
    Args:
        category_data (dict): Data for the new category.
    Returns:
        Category: The created category.
    """
    try:
        new_category = Category.from_dict(category_data)
        db.session.add(new_category)
        db.session.commit()
        return new_category
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ApplicationError(f"Error creating category: {str(e)}") from e


def update_category(category_id: UUID, category_data: dict) -> Category:
    """
    Update an existing category.
    Args:
        category_id (UUID): The ID of the category to update.
        category_data (dict): The new data for the category.
    Returns:
        Category: The updated category.
    """
    try:
        category = validate_model(category_id, Category)
        for key, value in category_data.items():
            if hasattr(category, key):
                setattr(category, key, value)
        db.session.commit()
        return category
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ApplicationError(
            f"Error updating category with ID {category_id}: {str(e)}") from e


def delete_category(category_id: UUID) -> str:
    """
    Delete a category by its ID.
    Args:
        category_id (UUID): The ID of the category to delete.
    Returns:
        str: A success message.
    """
    try:
        category = validate_model(category_id, Category)
        db.session.delete(category)
        db.session.commit()
        return f"Category with ID {category_id} has been deleted."
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ApplicationError(
            f"Error deleting category with ID {category_id}: {str(e)}") from e
