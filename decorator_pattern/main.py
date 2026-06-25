"""
Entry point — demonstrates the Decorator Pattern via log_execution.

The log_execution decorator is applied at definition time with @log_execution.
Every call automatically prints '<method_name> executed' to stdout, giving
developers a zero-effort execution trace for troubleshooting.
"""

from services.order_service import OrderService


def main() -> None:
    """Run demonstration order flows to show the logging decorator in action."""

    service = OrderService()

    print("=" * 55)
    print("  Decorator Pattern — Execution Logging Demo")
    print("=" * 55)

    result = service.create_order("Wireless Headphones", 2)
    print(f"  → {result}\n")

    result = service.get_order_status("ORD-42")
    print(f"  → {result}\n")

    result = service.cancel_order("ORD-42")
    print(f"  → {result}")

    print("=" * 55)


if __name__ == "__main__":
    main()
