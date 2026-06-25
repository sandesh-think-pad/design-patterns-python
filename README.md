# design-patterns-python

A collection of common design patterns implemented in Python, each with a realistic example, clean structure, and tests.

## Patterns Implemented

### 1. Singleton Pattern
**Location:** [singleton_pattern/](singleton_pattern/)

Ensures a class has only one instance and provides a global access point to it. Uses double-checked locking for thread safety.

**Example:** `DatabaseConnection` — guarantees a single shared connection instance across the app.

```python
db1 = DatabaseConnection()
db2 = DatabaseConnection()
assert db1 is db2  # True — same instance
```

**Key files:**
- [singleton_pattern/singleton.py](singleton_pattern/singleton.py) — thread-safe `DatabaseConnection` singleton
- [singleton_pattern/tests/test_singleton.py](singleton_pattern/tests/test_singleton.py)

---

### 2. Factory Pattern
**Location:** [factory_pattern/](factory_pattern/)

Centralises object creation behind a factory so callers never depend on concrete classes. Adding a new variant requires only a one-line registry change.

**Example:** `PaymentFactory` — creates `StripeProvider`, `PaypalProvider`, or `SquareProvider` from a string key.

```python
provider = PaymentFactory.create_provider("stripe")
provider.process_payment(100)
```

**Key files:**
- [factory_pattern/billing/payment_factory.py](factory_pattern/billing/payment_factory.py) — factory with registry dict
- [factory_pattern/billing/payment_interface.py](factory_pattern/billing/payment_interface.py) — `PaymentProvider` ABC
- [factory_pattern/tests/test_stripe_provider.py](factory_pattern/tests/test_stripe_provider.py)

---

### 3. Decorator Pattern
**Location:** [decorator_pattern/](decorator_pattern/)

Wraps a callable to add behaviour (logging, timing, auth, etc.) without modifying its source. Uses `functools.wraps` to preserve the original function's metadata.

**Example:** `@log_execution` — prints `<function_name> executed` after every call.

```python
@log_execution
def place_order(order_id: str): ...

place_order("123")  # logs: "place_order executed"
```

**Key files:**
- [decorator_pattern/decorators/log_execution.py](decorator_pattern/decorators/log_execution.py) — `log_execution` decorator
- [decorator_pattern/services/order_service.py](decorator_pattern/services/order_service.py) — decorated service
- [decorator_pattern/tests/test_log_execution.py](decorator_pattern/tests/test_log_execution.py)

---

## Running Tests

Each pattern has its own test suite. Run from the pattern's directory:

```bash
cd singleton_pattern && python -m pytest tests/
cd factory_pattern  && python -m pytest tests/
cd decorator_pattern && python -m pytest tests/
```

## Structure

```
design-patterns-python/
├── singleton_pattern/
│   ├── singleton.py
│   ├── main.py
│   └── tests/
├── factory_pattern/
│   ├── billing/
│   │   ├── payment_factory.py
│   │   ├── payment_interface.py
│   │   ├── stripe_provider.py
│   │   ├── paypal_provider.py
│   │   └── square_provider.py
│   ├── main.py
│   └── tests/
└── decorator_pattern/
    ├── decorators/
    ├── services/
    ├── main.py
    └── tests/
```
