import os

import pytest
from dotenv import load_dotenv
from uuid import uuid4
from flask.signals import request_finished  # ?

from app import create_app
from app.db import db
from app.models.user import User, UserRole

load_dotenv()

@pytest.fixture
def app():
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
def one_user(app):
    """Fixture to create a single user."""
    new_user = User(
        id=uuid4(),
        email="testuser@example.com",
        first_name="Test",
        last_name="User",
        street_address="123 Test St, Test City",
        role=UserRole.USER,
        phone="1234567890",
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user


@pytest.fixture
def multiple_users(app):
    """Fixture to create multiple users."""
    users = [
        User(
            id=uuid4(),
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            street_address="1 Admin Rd, Admin City",
            role=UserRole.ADMIN,
            phone="9876543210",
        ),
        User(
            id=uuid4(),
            email="user1@example.com",
            first_name="User1",
            last_name="Test",
            street_address="456 User Ln, Test Town",
            role=UserRole.USER,
            phone="1231231234",
        ),
        User(
            id=uuid4(),
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
def admin_user(app):
    """Fixture to create a single admin user."""
    admin = User(
        id=uuid4(),
        email="superadmin@example.com",
        first_name="Super",
        last_name="Admin",
        street_address="999 Admin Blvd, Admin City",
        role=UserRole.ADMIN,
        phone="1122334455",
    )
    db.session.add(admin)
    db.session.commit()
    return admin