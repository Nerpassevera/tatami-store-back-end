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
from app.models.order import Order, OrderStatus
from app.models.address import Address

load_dotenv()


@pytest.fixture
def app():
    """
    Create and configure a new instance of the Flask application for testing.

    This fixture sets up the Flask application with a test configuration,
    including setting the `TESTING` flag to True and configuring the
    SQLAlchemy database URI from an environment variable. It also ensures
    that the database is created before tests run and dropped after tests
    complete.

    Yields:
        flask.Flask: The configured Flask application instance.
    """
    # create the app with a test configuration
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

    # close and remove the temporary database
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
            stock=stock  # Updated to use 'stock' instead of 'stock_quantity'
        )
        db.session.add(product)
        db.session.commit()
        return product
    return _create_product


faker = Faker()


@pytest.fixture
def create_address():
    """Fixture to create an address."""
    def _create_address(
        user_id=None,
        label="Home",
        house_number=None,
        road=None,
        city=None,
        state=None,
        postcode=None,
        country=None
    ):
        if house_number is None:
            house_number = faker.building_number()
        if road is None:
            road = faker.street_name()
        if city is None:
            city = faker.city()
        if state is None:
            state = faker.state()
        if postcode is None:
            postcode = faker.postcode()
        if country is None:
            country = faker.country()

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
def create_user():
    """Fixture to create a user."""
    def _create_user(
        email=None,
        first_name=None,
        last_name=None,
        phone=None,
        role=UserRole.USER
    ):
        if email is None:
            email = faker.email()
        if first_name is None:
            first_name = faker.first_name()
        if last_name is None:
            last_name = faker.last_name()
        if phone is None:
            phone = faker.phone_number()

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role
        )
        db.session.add(user)
        db.session.commit()
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
def multiple_users(create_user, create_address):
    """Fixture to create multiple users with associated addresses."""
    users = [
        create_user(
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
            phone="9876543210",
        ),
        create_user(
            email="user1@example.com",
            first_name="User1",
            last_name="Test",
            role=UserRole.USER,
            phone="1231231234",
        ),
        create_user(
            email="user2@example.com",
            first_name="User2",
            last_name="Example",
            role=UserRole.USER,
            phone="3213214321",
        ),
    ]

    # Create addresses for each user
    for user in users:
        create_address(user_id=user.id)

    return users


@pytest.fixture
def admin_user(create_user):
    """Fixture to create an admin user."""
    return create_user(
        email="superadmin@example.com",
        first_name="Super",
        last_name="Admin",
        role=UserRole.ADMIN
    )


@pytest.fixture
def one_user(create_user):
    """Fixture to create a single user."""
    return create_user()


@pytest.fixture
def create_order(create_user, create_address):
    """Fixture to create an order."""
    def _create_order(user=None, address=None, total_amount=0.0, status=OrderStatus.PENDING):
        if user is None:
            user = create_user()
        if address is None:
            address = create_address(user_id=user.id)
        order = Order(
            user_id=user.id,
            address_id=address.id,
            total_amount=total_amount,
            status=status
        )
        db.session.add(order)
        db.session.commit()
        return order
    return _create_order


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
            price=price  # Updated to use 'price' instead of 'unit_price'
        )
        db.session.add(order_item)
        db.session.commit()
        return order_item
    return _create_order_item