"""
Order management service decorated with execution logging.

Decorator Pattern role: Concrete Component — each public method is wrapped
by log_execution, which adds logging cross-cutting behaviour without
modifying the business logic inside the methods.
"""

from decorators.log_execution import log_execution


class OrderService:
    """Handles order lifecycle operations."""

    @log_execution
    def create_order(self, item: str, quantity: int) -> str:
        """Create a new order and return a confirmation message."""
        return f"Order created: {quantity}x {item}"

    @log_execution
    def cancel_order(self, order_id: str) -> str:
        """Cancel an existing order by ID."""
        return f"Order {order_id} cancelled"

    @log_execution
    def get_order_status(self, order_id: str) -> str:
        """Return the current status of an order."""
        return f"Order {order_id} status: processing"
