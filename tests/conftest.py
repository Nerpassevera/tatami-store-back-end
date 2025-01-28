import os
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from flask import request_finished
from faker import Faker

from app import create_app
from app.db import db
from app.models.user import User, UserRole
from app.models.cart import Cart
from app.models.product import Product
from app.models.order_item import OrderItem
from app.models.address import Address

load_dotenv()
faker = Faker()

@pytest.fixture
def app():
    """Create and configure a new instance of the Flask application for testing."""
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    flask_app = create_app(test_config)

    @request_finished.connect_via(flask_app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with flask_app.app_context():
        db.create_all()
        yield flask_app

    with flask_app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def create_product():
    """Fixture to create a product."""
    def _create_product(name=None, price=9.99, description=None, stock=0):
        if name is None:
            name = f"test_item_{uuid4()}"
        product = Product(
            name=name,
            price=price,
            description=description,
            stock=stock
        )
        db.session.add(product)
        db.session.commit()
        return product
    return _create_product


@pytest.fixture
def create_address():
    """Fixture to create an address without requiring a user."""
    def _create_address(
        user_id,
        label="Home",
        house_number=None,
        road=None,
        city=None,
        state=None,
        postcode=None,
        country=None
    ):
        if user_id is None:
            raise ValueError("Missing required field: user_id")

        house_number = house_number or faker.building_number()
        road = road or faker.street_name()
        city = city or faker.city()
        state = state or faker.state()
        postcode = postcode or faker.postcode()
        country = country or faker.country()

        address = Address(
            user_id=user_id,
            label=label,
            house_number=house_number,
            road=road,
            city=city,
            state=state,
            postcode=postcode,
            country=country
        )
        db.session.add(address)
        db.session.commit()
        return address
    return _create_address


@pytest.fixture
def create_user(create_address):
    """Fixture to create a user with an associated address."""
    def _create_user(email=None, first_name=None, last_name=None, phone=None, role=UserRole.USER):
        email = email or faker.email()
        first_name = first_name or faker.first_name()
        last_name = last_name or faker.last_name()
        phone = phone or faker.phone_number()

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role
        )
        db.session.add(user)
        db.session.commit()

        # Create an associated address for the user
        create_address(user_id=user.id)

        return user
    return _create_user


@pytest.fixture
def create_cart(create_user):
    """Fixture to create a cart for a user."""
    def _create_cart(user=None):
        if user is None:
            user = create_user()
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()
        return cart
    return _create_cart


@pytest.fixture
def multiple_users(create_user):
    """Fixture to create multiple users with associated addresses."""
    users = [
        create_user(email="admin@example.com", first_name="Admin", last_name="User", role=UserRole.ADMIN, phone="9876543210"),
        create_user(email="user1@example.com", first_name="User1", last_name="Test", role=UserRole.USER, phone="1231231234"),
        create_user(email="user2@example.com", first_name="User2", last_name="Example", role=UserRole.USER, phone="3213214321"),
    ]
    return users


@pytest.fixture
def admin_user(create_user):
    """Fixture to create an admin user."""
    return create_user(email="superadmin@example.com", first_name="Super", last_name="Admin", role=UserRole.ADMIN)


@pytest.fixture
def create_order_item(create_product, create_order):
    """Fixture to create an order item."""
    def _create_order_item(order=None, product=None, quantity=1, price=10.0):
        if order is None:
            order = create_order()
        if product is None:
            product = create_product()
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            price=price
        )
        db.session.add(order_item)
        db.session.commit()
        return order_item
    return _create_order_item
