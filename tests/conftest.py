import os
from uuid import uuid4


import pytest
from dotenv import load_dotenv
from flask import request_finished

from app import create_app
from app.db import db
from app.models.user import User, UserRole
from app.models.cart import Cart
from app.models.product import Product

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
    def _create_product(name="test_item", price=9.99, description=None, stock_quantity=0):
        product = Product(name=name, price=price,
                          description=description, stock_quantity=stock_quantity)
        db.session.add(product)
        db.session.commit()
        return product
    return _create_product


@pytest.fixture
def create_user(app):
    """Fixture to create a user."""
    def _create_user(
        email="testuser@example.com",
        first_name="Test",
        last_name="User",
        street_address="123 Test St, Test City",
        phone="1234567890",
        role=UserRole.USER
    ):
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            street_address=street_address,
            phone=phone,
            role=role
        )
        db.session.add(user)
        db.session.commit()
        return user
    return _create_user


@pytest.fixture
def create_cart(app, create_user):
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
def one_user(app, create_user):
    """Fixture to create a single user."""
    return create_user()


@pytest.fixture
def multiple_users(app):
    """Fixture to create multiple users."""
    users = [
        User(
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            street_address="1 Admin Rd, Admin City",
            role=UserRole.ADMIN,
            phone="9876543210",
        ),
        User(
            email="user1@example.com",
            first_name="User1",
            last_name="Test",
            street_address="456 User Ln, Test Town",
            role=UserRole.USER,
            phone="1231231234",
        ),
        User(
            email="user2@example.com",
            first_name="User2",
            last_name="Example",
            street_address="789 Example Ave, Sample City",
            role=UserRole.USER,
            phone="3213214321",
        ),
    ]
    db.session.add_all(users)
    db.session.commit()
    return users


@pytest.fixture
def admin_user(create_user):
    return create_user(
        email="superadmin@example.com",
        first_name="Super",
        last_name="Admin",
        role=UserRole.ADMIN
    )
