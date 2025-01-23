import pytest
from app.models.user import User, UserRole
from uuid import uuid4
from app.db import db

@pytest.fixture
def new_user():
    """Fixture to create a new User object without saving it to the database."""
    return User(
        id=uuid4(),
        email="testuser@example.com",
        first_name="Test",
        last_name="User",
        street_address="123 Test St, Test City",
        role=UserRole.USER,
        phone="1234567890"
    )


def test_create_user(app, new_user):
    """Test creating and saving a new user in the database."""
    with app.app_context():
        assert User.query.count() == 0

        # Save the user
        db.session.add(new_user)
        db.session.commit()

        # Check the user exists in the database
        assert User.query.count() == 1
        user = User.query.first()
        assert user.email == "testuser@example.com"
        assert user.role == UserRole.USER


def test_update_user(app, new_user):
    """Test updating an existing user's information."""
    with app.app_context():
        # Add user to the database
        db.session.add(new_user)
        db.session.commit()

        # Update user
        user = User.query.first()
        user.first_name = "Updated"
        user.role = UserRole.ADMIN
        db.session.commit()

        # Check the update
        updated_user = User.query.first()
        assert updated_user.first_name == "Updated"
        assert updated_user.role == UserRole.ADMIN


def test_delete_user(app, new_user):
    """Test deleting a user from the database."""
    with app.app_context():
        # Add user to the database
        db.session.add(new_user)
        db.session.commit()

        # Delete the user
        user = User.query.first()
        db.session.delete(user)
        db.session.commit()

        # Ensure the user no longer exists
        assert User.query.count() == 0


def test_query_users(app, multiple_users):
    """Test querying multiple users from the database."""
    with app.app_context():
        # Use the `multiple_users` fixture to add users
        assert len(multiple_users) == 3

        # Query all users
        users = User.query.all()
        assert len(users) == 3

        # Query a specific user
        user = User.query.filter_by(email="user1@example.com").first()
        assert user is not None
        assert user.first_name == "User1"


def test_user_to_dict(new_user):
    """Test the `to_dict` method of the User model."""
    user_dict = new_user.to_dict()
    assert user_dict["email"] == "testuser@example.com"
    assert user_dict["first_name"] == "Test"
    assert user_dict["last_name"] == "User"
    assert user_dict["street_address"] == "123 Test St, Test City"
    assert user_dict["role"] == "User"
    assert user_dict["phone"] == "1234567890"


def test_user_from_dict(app):
    """Test creating a user using the `from_dict` method."""
    user_data = {
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
        "street_address": "456 Example Rd, Example City",
        "role": "ADMIN",
        "phone": "9876543210"
    }
    with app.app_context():
        user = User.from_dict(user_data)
        db.session.add(user)
        db.session.commit()

        # Verify user creation
        assert User.query.count() == 1
        created_user = User.query.first()
        assert created_user.email == "newuser@example.com"
        assert created_user.role == UserRole.ADMIN
