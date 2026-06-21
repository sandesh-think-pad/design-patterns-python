"""
Defines the abstract interface that all payment providers must implement.

This is the 'Product' interface in the Factory Pattern — it establishes the
contract that every concrete provider must honour, allowing client code to
work with any provider without knowing its concrete type.
"""

from abc import ABC, abstractmethod


class PaymentProvider(ABC):
    """Abstract base class for all payment providers.

    Factory Pattern role: Product interface.
    Every concrete provider (Stripe, PayPal, Square …) must subclass this
    and implement `make_payment`.  Client code depends only on this
    abstraction, never on a concrete class.
    """

    @abstractmethod
    def make_payment(self, amount: float) -> str:
        """Process a payment for the given amount.

        Args:
            amount: The monetary value to charge (in USD).

        Returns:
            A confirmation message describing which provider handled the charge.
        """
