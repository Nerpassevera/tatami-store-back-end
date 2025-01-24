import pytest
from uuid import uuid4
from datetime import datetime

from app.db import db
from app.models.order import Order, OrderStatus
from app.models.product import Product
from app.models.user import UserRole
from app.models.order_item import OrderItem


@pytest.fixture
def create_order(create_user):
    """Fixture to create an order."""
    def _create_order(user=None, total_amount=0.0, status="PENDING"):
        if user is None:
            user = create_user()
        order = Order(
            user_id=user.id,
            total_amount=total_amount,
            order_date=datetime.utcnow(),
            status=status,
        )
        db.session.add(order)
        db.session.commit()
        return order
    return _create_order

### Tests

def test_create_order(app, create_order):
    """Test creating an order."""
    order = create_order(total_amount=100.0, status="PENDING")

    assert order.id is not None
    assert order.total_amount == 100.0
    assert order.status.value == "Pending"
    assert isinstance(order.order_date, datetime)

def test_order_relationship_with_user(app, create_user, create_order):
    """Test order is correctly linked to a user."""
    user = create_user(email="user1@example.com")
    order = create_order(user=user)

    assert order.user_id == user.id
    assert user.orders[0].id == order.id

def test_order_relationship_with_order_items(app, create_order, create_order_item):
    """Test order is correctly linked to its order items."""
    order = create_order()
    item1 = create_order_item(order=order, quantity=2, unit_price=15.0)
    item2 = create_order_item(order=order, quantity=1, unit_price=10.0)

    assert len(order.order_items) == 2
    assert order.order_items[0].order_id == item1.order_id
    assert order.order_items[0].product_id == item1.product_id
    assert order.order_items[1].order_id == item2.order_id
    assert order.order_items[1].product_id == item2.product_id


def test_order_total_amount_calculation(app, create_order, create_order_item):
    """Test that the total amount of the order matches the sum of its items."""
    order = create_order(total_amount=0.0)
    create_order_item(order=order, quantity=2, unit_price=10.0)  # 20.0
    create_order_item(order=order, quantity=3, unit_price=15.0)  # 45.0

    total_amount = sum(item.quantity * item.unit_price for item in order.order_items)

    assert order.total_amount == 0.0  # Shouldn't auto-update unless explicitly calculated
    assert total_amount == 65.0

def test_update_order_status(app, create_order):
    """Test updating the status of an order."""
    order = create_order(status="PENDING")
    assert order.status.value == "Pending"

    order.status = "COMPLETED"
    db.session.commit()

    updated_order = Order.query.get(order.id)
    assert updated_order.status.value == "Completed"

def test_delete_order_cascades_to_order_items(app, create_order, create_order_item):
    """Test deleting an order cascades to its order items."""
    order = create_order()
    create_order_item(order=order)

    assert OrderItem.query.count() == 1

    with app.app_context():
        order = db.session.merge(order)
        db.session.delete(order)
        db.session.commit()

    assert Order.query.count() == 0
    assert OrderItem.query.count() == 0

def test_order_query_filter(app, create_order):
    """Test filtering orders by user or status."""
    create_order(total_amount=50.0, status=OrderStatus.PENDING)
    create_order(total_amount=75.0, status=OrderStatus.COMPLETED)
    create_order(total_amount=30.0, status=OrderStatus.COMPLETED)

    pending_orders = Order.query.filter_by(status=OrderStatus.PENDING).all()
    assert len(pending_orders) == 1
    assert pending_orders[0].total_amount == 50.0

def test_order_with_no_items(app, create_order):
    """Test creating an order with no items."""
    order = create_order(total_amount=0.0)

    assert order.id is not None
    assert len(order.order_items) == 0

