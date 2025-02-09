from uuid import UUID
from app.models.product import Product
from app.models.category import Category
from app.models.product_category import ProductCategory
from app.db import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from app.services.utility_functions import validate_model
from app.exceptions import ApplicationError


# def get_all_products() -> list[Product]:
#     """
#     Retrieve all products from the database.

#     Returns:
#         list[Product]: A list of all products.
#     """
#     try:
#         return db.session.query(Product).all()
#     except SQLAlchemyError as e:
#         raise ApplicationError(f"Error retrieving products: {str(e)}")
def get_all_products(search: str = None, category: str = None, order_by: str = None, price_max: str = None) -> dict:

    try:
        # Build the base query with outer joins to include products without categories
        query = (
            db.session.query(
                Product,
                func.coalesce(func.array_agg(Category.name), func.cast("{}", type_=func.array_agg(Category.name).type)).label("categories")
            )
            .outerjoin(ProductCategory, Product.id == ProductCategory.product_id)
            .outerjoin(Category, Category.id == ProductCategory.category_id)
            .group_by(Product.id)
        )

        # Filter by search term (case-insensitive) on name or description
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(Product.name.ilike(search_pattern) | Product.description.ilike(search_pattern))
        
        # Filter by category: only return products that contain the selected category.
        # Using the PostgreSQL operator @> to check if the array of category names contains [category]
        if category and category.lower() != "all":
            query = query.having(func.array_agg(Category.name).op('@>')( [category] ))
        
        # Filter by price maximum
        if price_max is not None:
            query = query.filter(Product.price <= price_max)

        # Apply ordering: options "a-z", "z-a", "high", "low"
        if order_by:
            if order_by == "a-z":
                query = query.order_by(Product.name.asc())
            elif order_by == "z-a":
                query = query.order_by(Product.name.desc())
            elif order_by == "high":
                query = query.order_by(Product.price.desc())
            elif order_by == "low":
                query = query.order_by(Product.price.asc())
        
        products = query.all()

        # Map each product row to a dictionary
        products_list = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "stock": product.stock,
                "image_url": product.image_url,
                "categories": categories if categories is not None else []
            }
            for product, categories in products
        ]
        return products_list
    except Exception as e:
        raise ApplicationError(f"Error retrieving products: {str(e)}") from e


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