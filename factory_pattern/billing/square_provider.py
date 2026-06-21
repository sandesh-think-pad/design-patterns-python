"""
Concrete Square payment provider.

Factory Pattern role: Concrete Product.
Instantiated exclusively by PaymentFactory — never by client code directly.
"""

from billing.payment_interface import PaymentProvider


class SquareProvider(PaymentProvider):
    """Simulates Square payment processing."""

    def make_payment(self, amount: float) -> str:
        """Process a payment through Square.

        Args:
            amount: The monetary value to charge (in USD).

        Returns:
            A Square-specific confirmation string.
        """
        # In a real integration this would call the Square Payments API.
        return f"Square payment of ${amount} processed successfully"
