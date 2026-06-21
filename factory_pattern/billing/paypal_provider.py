"""
Concrete PayPal payment provider.

Factory Pattern role: Concrete Product.
Instantiated exclusively by PaymentFactory — never by client code directly.
"""

from billing.payment_interface import PaymentProvider


class PaypalProvider(PaymentProvider):
    """Simulates PayPal payment processing."""

    def make_payment(self, amount: float) -> str:
        """Process a payment through PayPal.

        Args:
            amount: The monetary value to charge (in USD).

        Returns:
            A PayPal-specific confirmation string.
        """
        # In a real integration this would call the PayPal REST SDK.
        return f"PayPal payment of ${amount} processed successfully"
