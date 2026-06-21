"""
High-level billing service used by application entry points.

This layer demonstrates the Dependency Inversion Principle working alongside
the Factory Pattern: BillingService depends on the PaymentProvider abstraction
(via the factory) and never imports a concrete provider class.
"""

from billing.payment_factory import PaymentFactory


class BillingService:
    """Orchestrates payment processing without knowing provider internals.

    Client code talks only to BillingService.  BillingService talks only to
    PaymentFactory and the PaymentProvider interface.  No concrete provider
    class ever appears outside the factory registry.
    """

    def process_payment(self, provider_name: str, amount: float) -> str:
        """Charge `amount` using the named payment provider.

        The Factory Pattern is invoked here: the factory decides which
        concrete class to instantiate; BillingService just uses the result.

        Args:
            provider_name: Identifier for the payment provider
                           ("stripe", "paypal", "square").
            amount:        The monetary value to charge (in USD).

        Returns:
            A confirmation message from the provider.

        Raises:
            ValueError: Propagated from PaymentFactory when the provider
                        is not registered.
        """
        # --- Factory Pattern in action ---
        # We ask the factory for a provider; we receive a PaymentProvider.
        # BillingService has no idea whether it's Stripe, PayPal, or Square.
        provider = PaymentFactory.create_provider(provider_name)

        return provider.make_payment(amount)
