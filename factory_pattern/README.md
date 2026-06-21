# Factory Pattern — Billing Service

A focused Python project that demonstrates the **Factory Design Pattern** using a
billing/payment service as the domain.

---

## What is the Factory Pattern?

The **Factory Pattern** is a creational design pattern that centralises object
creation behind a dedicated creator class (the *factory*).  Client code never
calls `ProviderClass()` directly; it calls the factory and receives back an
object typed to an *interface* (abstract base class).  This decouples the
client from every concrete implementation.

Two closely related variants exist:

| Variant | Description |
|---|---|
| **Simple Factory** | A single class with a static/class method that maps a key to a concrete type (used here). |
| **Factory Method** | Subclasses override a creator method to decide which concrete type to return. |

This project uses the **Simple Factory** variant because it is the most
readable starting point for learning the pattern.

---

## Why is the Factory Pattern useful here?

A billing service must support multiple payment gateways (Stripe, PayPal,
Square …).  Without a factory, every piece of client code would contain:

```python
# Without factory — tightly coupled, hard to extend
if provider == "stripe":
    p = StripeProvider()
elif provider == "paypal":
    p = PaypalProvider()
...
```

This violates the **Open/Closed Principle** — adding a new provider forces you
to touch every place that chooses a provider.

With a factory:

```python
# With factory — decoupled, easy to extend
provider = PaymentFactory.create_provider("stripe")
```

Adding a fourth gateway requires:
1. A new file with a concrete class.
2. One line added to the factory registry.
3. **Zero changes** to `BillingService`, `main.py`, or any other caller.

---

## Class Diagram (ASCII)

```
          «abstract»
        PaymentProvider
        ───────────────
        + make_payment(amount: float) -> str   (abstract)
               △
               │  inherits
       ┌───────┼───────┐
       │       │       │
StripeProvider  PaypalProvider  SquareProvider
───────────────  ──────────────  ──────────────
+ make_payment() + make_payment() + make_payment()


         PaymentFactory
         ──────────────
         _providers: dict[str, type[PaymentProvider]]
         + create_provider(name: str) -> PaymentProvider


         BillingService
         ──────────────
         + process_payment(provider: str, amount: float) -> str
               │  uses
               ▼
         PaymentFactory.create_provider()
               │  returns
               ▼
         PaymentProvider  (abstract — the concrete type is hidden)
```

---

## Sequence of Execution

```
main.py           BillingService     PaymentFactory      ConcreteProvider
   │                    │                  │                    │
   │ process_payment()  │                  │                    │
   │───────────────────>│                  │                    │
   │                    │ create_provider()│                    │
   │                    │─────────────────>│                    │
   │                    │                  │  ProviderClass()   │
   │                    │                  │───────────────────>│
   │                    │                  │<───────────────────│
   │                    │<─────────────────│ provider instance  │
   │                    │                  │                    │
   │                    │         make_payment(amount)          │
   │                    │──────────────────────────────────────>│
   │                    │<──────────────────────────────────────│
   │<───────────────────│ confirmation string                   │
```

---

## Benefits of the Pattern

| Benefit | Detail |
|---|---|
| **Decoupling** | Client code depends only on `PaymentProvider` interface and `PaymentFactory`, never on concrete classes. |
| **Open/Closed** | Add providers without modifying existing code. |
| **Single Responsibility** | Object creation logic lives in one place. |
| **Testability** | Easy to inject a mock provider by registering it under a test key. |
| **Readability** | `create_provider("stripe")` is self-documenting. |

---

## How to Add a Fourth Provider (Razorpay)

**Step 1 — Create the concrete class**

```python
# billing/razorpay_provider.py
from billing.payment_interface import PaymentProvider

class RazorpayProvider(PaymentProvider):
    def make_payment(self, amount: float) -> str:
        return f"Razorpay payment of ${amount} processed successfully"
```

**Step 2 — Register it in the factory**

```python
# billing/payment_factory.py  — add ONE line to _providers:
from billing.razorpay_provider import RazorpayProvider

_providers: dict[str, type[PaymentProvider]] = {
    "stripe":   StripeProvider,
    "paypal":   PaypalProvider,
    "square":   SquareProvider,
    "razorpay": RazorpayProvider,   # <-- new line
}
```

**Step 3 — Use it**

```python
service.process_payment("razorpay", 300.0)
```

No other file changes are required.

---

## Project Structure

```
factory_pattern/
│
├── billing/
│   ├── __init__.py           # Package marker
│   ├── payment_interface.py  # Abstract base class (Product interface)
│   ├── stripe_provider.py    # Concrete Product
│   ├── paypal_provider.py    # Concrete Product
│   ├── square_provider.py    # Concrete Product
│   ├── payment_factory.py    # Creator / Factory  ← pattern lives here
│   └── billing_service.py    # High-level service (uses the factory)
│
├── main.py                   # Entry point / demo
├── README.md
└── requirements.txt
```

---

## Running the Demo

```bash
cd factory_pattern
python main.py
```

### Expected Output

```
=======================================================
  Factory Pattern — Billing Service Demo
=======================================================
  Stripe payment of $100.0 processed successfully
  PayPal payment of $250.5 processed successfully
  Square payment of $75.0 processed successfully
=======================================================

Testing unknown provider:
  Error caught as expected → Unsupported payment provider: 'bitcoin'. Supported providers are: stripe, paypal, square
```

---

## Requirements

- Python 3.11+
- No third-party packages required
