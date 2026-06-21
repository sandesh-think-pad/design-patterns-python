"""
Unit tests for StripeProvider.

Coverage areas:
  - Interface compliance (is-a PaymentProvider)
  - Return value format and content
  - Correct handling of typical, edge-case, and boundary amounts
"""

import pytest

from billing.payment_interface import PaymentProvider
from billing.stripe_provider import StripeProvider


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def provider() -> StripeProvider:
    """Return a fresh StripeProvider for each test."""
    return StripeProvider()


# ---------------------------------------------------------------------------
# Interface compliance
# ---------------------------------------------------------------------------

class TestStripeProviderInterface:
    def test_is_payment_provider_subclass(self) -> None:
        """StripeProvider must satisfy the PaymentProvider contract."""
        assert issubclass(StripeProvider, PaymentProvider)

    def test_instance_is_payment_provider(self, provider: StripeProvider) -> None:
        assert isinstance(provider, PaymentProvider)

    def test_has_make_payment_method(self, provider: StripeProvider) -> None:
        assert callable(getattr(provider, "make_payment", None))


# ---------------------------------------------------------------------------
# Return value — content
# ---------------------------------------------------------------------------

class TestMakePaymentContent:
    def test_result_mentions_stripe(self, provider: StripeProvider) -> None:
        result = provider.make_payment(100.0)
        assert "Stripe" in result

    def test_result_mentions_amount(self, provider: StripeProvider) -> None:
        result = provider.make_payment(100.0)
        assert "100.0" in result

    def test_result_indicates_success(self, provider: StripeProvider) -> None:
        result = provider.make_payment(100.0)
        assert "successfully" in result.lower()

    def test_result_is_string(self, provider: StripeProvider) -> None:
        result = provider.make_payment(100.0)
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# Return value — exact format
# ---------------------------------------------------------------------------

class TestMakePaymentFormat:
    def test_exact_message_integer_amount(self, provider: StripeProvider) -> None:
        assert provider.make_payment(100.0) == "Stripe payment of $100.0 processed successfully"

    def test_exact_message_decimal_amount(self, provider: StripeProvider) -> None:
        assert provider.make_payment(49.99) == "Stripe payment of $49.99 processed successfully"

    def test_exact_message_zero_amount(self, provider: StripeProvider) -> None:
        assert provider.make_payment(0.0) == "Stripe payment of $0.0 processed successfully"


# ---------------------------------------------------------------------------
# Parameterised — various amounts
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("amount", [0.0, 0.01, 1.0, 99.99, 250.50, 10_000.0])
def test_make_payment_contains_amount(amount: float) -> None:
    """make_payment should embed the exact amount in the confirmation string."""
    provider = StripeProvider()
    result = provider.make_payment(amount)
    assert str(amount) in result


@pytest.mark.parametrize("amount", [0.0, 0.01, 1.0, 99.99, 250.50, 10_000.0])
def test_make_payment_returns_non_empty_string(amount: float) -> None:
    provider = StripeProvider()
    assert provider.make_payment(amount) != ""


# ---------------------------------------------------------------------------
# Independence — each call returns a fresh string
# ---------------------------------------------------------------------------

class TestMakePaymentIndependence:
    def test_multiple_calls_return_consistent_results(
        self, provider: StripeProvider
    ) -> None:
        """Calling make_payment twice with the same amount must give identical results."""
        first = provider.make_payment(75.0)
        second = provider.make_payment(75.0)
        assert first == second

    def test_different_amounts_produce_different_messages(
        self, provider: StripeProvider
    ) -> None:
        assert provider.make_payment(10.0) != provider.make_payment(20.0)
