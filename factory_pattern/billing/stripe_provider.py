"""
Concrete Stripe payment provider.

Factory Pattern role: Concrete Product.
Instantiated exclusively by PaymentFactory — never by client code directly.
"""

from billing.payment_interface import PaymentProvider


class StripeProvider(PaymentProvider):
    """Simulates Stripe payment processing."""

    def make_payment(self, amount: float) -> str:
        """Process a payment through Stripe.

        Args:
            amount: The monetary value to charge (in USD).

        Returns:
            A Stripe-specific confirmation string.
        """
        # In a real integration this would call the Stripe SDK.
        return f"Stripe payment of ${amount} processed successfully"
