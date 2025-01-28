from uuid import UUID

class ApplicationError(Exception):
    """
    Base class for all custom application errors.
    """
    def __init__(self, message: str):
        super().__init__(message)


class StockError(ApplicationError):
    """
    Raised when there is an issue with stock availability.

    Attributes:
        product_name (str): The name of the product.
        requested_quantity (int): The quantity requested by the user.
        available_quantity (int): The quantity available in stock.
    """
    def __init__(self, product_name: str, requested_quantity: int, available_quantity: int):
        super().__init__(
            f"Insufficient stock for product '{product_name}'. "
            f"Requested: {requested_quantity}, Available: {available_quantity}."
        )


class EmptyCartError(ApplicationError):
    """
    Raised when the user's cart is empty.
    
    Attributes:
        user_id (UUID): The ID of the user with the empty cart.
    """
    def __init__(self, user_id):
        super().__init__(f"Cart for user ID {user_id} is empty. Cannot place an order.")


class AddressOwnershipError(ApplicationError):
    """
    Raised when the provided address does not belong to the user.

    Attributes:
        address_id (int): The ID of the address.
        user_id (UUID): The ID of the user attempting to use the address.
    """
    def __init__(self, address_id: int, user_id):
        super().__init__(
            f"Address with ID {address_id} does not belong to user ID {user_id}. "
            "Please provide a valid address."
        )

class StatusError(ApplicationError):
    """
    Raised when there is an invalid status transition.

    Attributes:
        current_status (str): The current status of the order.
        new_status (str): The attempted new status.
    """
    def __init__(self, current_status, new_status=None):
        if new_status:
            super().__init__(
                f"Cannot change status from {current_status.value} to {new_status}."
            )
        else:
            super().__init__(f"Invalid status: {current_status}.")

class InstanceNotFoundError(Exception):
    """Custom exception raised when a model instance is not found."""
    def __init__(self, model, model_id: UUID):
        super().__init__(f"{model.__name__} with ID {model_id} not found.")