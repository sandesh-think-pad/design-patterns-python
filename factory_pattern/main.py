"""
Entry point — demonstrates the Factory Pattern via BillingService.

Client code only knows about BillingService and provider name strings.
It never imports or instantiates StripeProvider, PaypalProvider, or
SquareProvider directly — that is the whole point of the Factory Pattern.
"""

from billing.billing_service import BillingService


def main() -> None:
    """Run demonstration payment flows for all supported providers."""

    service = BillingService()

    print("=" * 55)
    print("  Factory Pattern — Billing Service Demo")
    print("=" * 55)

    # --- Each call goes: client → BillingService → PaymentFactory → Provider
    scenarios: list[tuple[str, float]] = [
        ("stripe",  100.0),
        ("paypal",  250.50),
        ("square",   75.0),
    ]

    for provider_name, amount in scenarios:
        result = service.process_payment(provider_name, amount)
        print(f"  {result}")

    print("=" * 55)

    # --- Demonstrate graceful error handling for unknown providers ---
    print("\nTesting unknown provider:")
    try:
        service.process_payment("blahblah", 500.0)
    except ValueError as exc:
        print(f"  Error caught as expected → {exc}")


if __name__ == "__main__":
    main()
