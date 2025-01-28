import pytest
from app.models.product import Product
from app.models.cart_item import CartItem
from app.models.product_category import ProductCategory
from app.models.category import Category
from app.db import db


def test_product_cascade_deletion_for_cart_items(app, create_product, create_cart):
    """Ensure deleting a product cascades to CartItem."""
    # Create a product and associate it with a cart item
    product = create_product("Test Product", 10.0, "A product for testing")
    cart = create_cart()

    # Add the product to the cart
    cart_item = CartItem(
        cart_id=cart.id,
        product_id=product.id,
        quantity=1
    )
    db.session.add(cart_item)
    db.session.commit()

    # Verify initial state
    assert CartItem.query.count() == 1

    # Action: Delete the product
    with app.app_context():
        product = db.session.merge(product)  # Ensure product is in the current session
        db.session.delete(product)
        db.session.commit()

    # Verify cascading deletions
    assert Product.query.count() == 0  # Product is deleted
    assert CartItem.query.count() == 0  # Cart item is deleted


def test_product_cascade_deletion_for_product_category(app, create_product):
    """Ensure deleting a product cascades to ProductCategory."""
    # Create a category and add it to the database
    category = Category(id=1, name="Electronics")
    db.session.add(category)
    db.session.commit()

    # Create a product and associate it with the category
    product = create_product("Test Product", 10.0, "A product for testing")
    product_category = ProductCategory(product_id=product.id, category_id=category.id)
    db.session.add(product_category)
    db.session.commit()

    # Verify initial state
    assert ProductCategory.query.count() == 1

    # Action: Delete the product
    with app.app_context():
        product = db.session.merge(product)  # Ensure product is in the current session
        db.session.delete(product)
        db.session.commit()

    # Verify cascading deletions
    assert Product.query.count() == 0  # Product is deleted
    assert ProductCategory.query.count() == 0  # ProductCategory is deleted


def test_product_creation(app):
    """Test creating a product."""
    product = Product(name="Test Product", price=10.0, description="Sample product", stock=5)
    db.session.add(product)
    db.session.commit()

    assert Product.query.count() == 1
    assert product.name == "Test Product"
    assert product.price == 10.0
    assert product.stock == 5


def test_product_update(app, create_product):
    """Test updating a product."""
    product = create_product("Original Product", 15.0, "Original description", 10)
    product.name = "Updated Product"
    product.price = 20.0
    product.description = "Updated description"
    product.stock_quantity = 50

    db.session.commit()

    updated_product = Product.query.get(product.id)
    assert updated_product.name == "Updated Product"
    assert updated_product.price == 20.0
    assert updated_product.description == "Updated description"
    assert updated_product.stock_quantity == 50


def test_product_association_with_multiple_categories(app, create_product):
    """Test associating a product with multiple categories."""
    product = create_product("Test Product", 10.0)
    categories = [
        Category(id=1, name="Electronics"),
        Category(id=2, name="Home Appliances"),
    ]
    db.session.add_all(categories)
    db.session.commit()

    for category in categories:
        product_category = ProductCategory(product_id=product.id, category_id=category.id)
        db.session.add(product_category)

    db.session.commit()

    assert ProductCategory.query.filter_by(product_id=product.id).count() == len(categories)


def test_product_deletion_does_not_affect_other_products(app, create_product):
    """Ensure deleting one product does not affect others."""
    product1 = create_product("Product 1", 15.0)
    product2 = create_product("Product 2", 20.0)

    with app.app_context():
        # Ensure product1 is in the current session
        product1 = db.session.merge(product1)
        db.session.delete(product1)
        db.session.commit()

    assert Product.query.count() == 1
    remaining_product = Product.query.first()
    assert remaining_product.name == "Product 2"


def test_product_stock_quantity_validation(app, create_product):
    """Test product stock quantity cannot be negative."""
    with pytest.raises(ValueError):
        create_product("Invalid Product", 10.0, stock=-5)


def test_product_to_dict_method(app, create_product):
    """Test the `to_dict` method of the Product model."""
    product = create_product("Test Product", 25.0, "A product for testing", 10)
    product_dict = product.to_dict()

    assert product_dict["name"] == "Test Product"
    assert product_dict["price"] == 25.0
    assert product_dict["description"] == "A product for testing"
    assert product_dict["stock"] == 10