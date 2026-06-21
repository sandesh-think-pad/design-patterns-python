"""
Factory responsible for creating PaymentProvider instances.

This is the heart of the Factory Pattern in this project.

Factory Pattern roles:
  - PaymentFactory  →  Creator / Factory
  - PaymentProvider →  Product interface
  - Stripe/PayPal/SquareProvider → Concrete Products

Key design decisions:
  1. A registry dict maps provider names to their classes.  Adding a new
     provider only requires adding one entry here — nothing else changes.
  2. `create_provider` is a @classmethod so callers never need a factory
     instance; they call PaymentFactory.create_provider("stripe") directly.
  3. Client code imports PaymentFactory only — concrete provider modules
     remain hidden inside this file.
"""

from billing.payment_interface import PaymentProvider
from billing.stripe_provider import StripeProvider
from billing.paypal_provider import PaypalProvider
from billing.square_provider import SquareProvider


class PaymentFactory:
    """Creates and returns the requested PaymentProvider implementation.

    Factory Pattern role: Creator.
    Centralises all object-creation logic so that adding a new provider
    requires a single-line registry change here and a new concrete class —
    zero changes anywhere else.
    """

    # --- Registry: the only place that knows about concrete classes ---
    # To add a fourth provider (e.g. Razorpay), add one line:
    #   "razorpay": RazorpayProvider
    _providers: dict[str, type[PaymentProvider]] = {
        "stripe": StripeProvider,
        "paypal": PaypalProvider,
        "square": SquareProvider,
    }

    @classmethod
    def create_provider(cls, provider_name: str) -> PaymentProvider:
        """Instantiate and return the correct PaymentProvider.

        This is the Factory Method — the single point of object creation
        for all payment providers.

        Args:
            provider_name: Case-insensitive key identifying the provider
                           ("stripe", "paypal", "square").

        Returns:
            A concrete PaymentProvider ready to process payments.

        Raises:
            ValueError: If the requested provider is not registered.
        """
        key = provider_name.lower()

        # Look up the class from the registry — no if/elif chains needed.
        provider_class = cls._providers.get(key)

        if provider_class is None:
            supported = ", ".join(cls._providers.keys())
            raise ValueError(
                f"Unsupported payment provider: '{provider_name}'. "
                f"Supported providers are: {supported}"
            )

        # The factory creates the instance; the caller receives a
        # PaymentProvider and never sees the concrete type.
        return provider_class()
