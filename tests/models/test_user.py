import pytest
from uuid import uuid4
from app.models.user import User, UserRole
from app.models.address import Address
from app.db import db


@pytest.fixture
def new_user(app, create_address):
    """Fixture to create a new User object with an associated address."""
    with app.app_context():
        user = User(
            id=uuid4(),
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            phone="1234567890",
            role=UserRole.USER
        )
        db.session.add(user)
        db.session.commit()
        address = create_address(user.id)
        db.session.add(address)
        db.session.commit()
        return User.query.get(user.id)


@pytest.fixture
def multiple_users(create_address):
    """Fixture to create multiple User objects with associated addresses."""
    users = [
        User(
            id=uuid4(),
            email="user1@example.com",
            first_name="User1",
            last_name="One",
            phone="1234567890",
            role=UserRole.USER,
        ),
        User(
            id=uuid4(),
            email="user2@example.com",
            first_name="User2",
            last_name="Two",
            phone="0987654321",
            role=UserRole.ADMIN,
        ),
        User(
            id=uuid4(),
            email="user3@example.com",
            first_name="User3",
            last_name="Three",
            phone="1122334455",
            role=UserRole.USER,
        )
    ]
    db.session.add_all(users)
    db.session.commit()

    for user in users:
        create_address(user_id=user.id)

    return users


def test_create_user(app, create_user, create_address):
    """Test creating and saving a new user in the database."""
    with app.app_context():
        assert User.query.count() == 0
        user = create_user(email="testuser@example.com")
        address = create_address(user_id=user.id)

        # Save the user
        db.session.add(user)
        db.session.add(address)
        db.session.commit()

        # Check the user exists in the database
        assert User.query.count() == 1
        user = User.query.first()
        assert user.email == "testuser@example.com"
        assert user.role == UserRole.USER


def test_update_user(app, create_user):
    """Test updating an existing user's information."""
    with app.app_context():
        user = create_user()

        # Update user
        user.first_name = "Updated"
        user.role = UserRole.ADMIN
        db.session.commit()

        # Check the update
        updated_user = User.query.first()
        assert updated_user.first_name == "Updated"
        assert updated_user.role == UserRole.ADMIN


def test_delete_user(app, create_user, create_address):
    """Test deleting a user from the database."""
    with app.app_context():
        user = create_user()
        address = create_address(user_id=user.id)
        db.session.add(address)
        db.session.commit()

        # Delete the user
        db.session.delete(user)
        db.session.commit()

        # Ensure the user no longer exists
        assert User.query.count() == 0
        assert Address.query.count() == 0


def test_query_users(app, multiple_users):
    """Test querying multiple users from the database."""
    with app.app_context():
        # Add users to the database
        db.session.commit()

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
    assert user_dict["role"] == "User"
    assert user_dict["phone"] == "1234567890"


def test_user_from_dict(app):
    """Test creating a user using the `from_dict` method."""
    user_data = {
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
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


def test_user_choices():
    """Test the `choices` class method of the User model."""
    roles = User.role_choices()
    assert roles == ["Admin", "User"]
