"""
Tests for the log_execution decorator and OrderService integration.

Coverage areas:
  - Decorator preserves function name and return value
  - Correct log line printed for each decorated method
  - Integration: all OrderService methods emit the expected log
"""

import pytest

from decorators.log_execution import log_execution
from services.order_service import OrderService


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def service() -> OrderService:
    """Return a fresh OrderService for each test."""
    return OrderService()


# ---------------------------------------------------------------------------
# log_execution — unit tests
# ---------------------------------------------------------------------------

class TestLogExecutionDecorator:
    def test_preserves_return_value(self) -> None:
        @log_execution
        def add(a: int, b: int) -> int:
            return a + b

        assert add(2, 3) == 5

    def test_preserves_function_name(self) -> None:
        @log_execution
        def my_func() -> None:
            pass

        assert my_func.__name__ == "my_func"

    def test_prints_method_name_executed(self, capsys: pytest.CaptureFixture[str]) -> None:
        @log_execution
        def process() -> str:
            return "done"

        process()
        captured = capsys.readouterr()
        assert captured.out.strip() == "process executed"

    def test_log_format_is_name_space_executed(self, capsys: pytest.CaptureFixture[str]) -> None:
        @log_execution
        def calculate_total() -> int:
            return 42

        calculate_total()
        captured = capsys.readouterr()
        assert captured.out.strip() == "calculate_total executed"

    def test_passes_args_and_kwargs(self) -> None:
        @log_execution
        def greet(name: str, *, greeting: str = "Hello") -> str:
            return f"{greeting}, {name}"

        assert greet("Alice", greeting="Hi") == "Hi, Alice"

    def test_log_emitted_once_per_call(self, capsys: pytest.CaptureFixture[str]) -> None:
        @log_execution
        def noop() -> None:
            pass

        noop()
        noop()
        lines = capsys.readouterr().out.strip().splitlines()
        assert len(lines) == 2
        assert all(line == "noop executed" for line in lines)


# ---------------------------------------------------------------------------
# OrderService — integration tests
# ---------------------------------------------------------------------------

class TestOrderServiceLogging:
    def test_create_order_logs(
        self, service: OrderService, capsys: pytest.CaptureFixture[str]
    ) -> None:
        service.create_order("Widget", 3)
        assert capsys.readouterr().out.strip() == "create_order executed"

    def test_cancel_order_logs(
        self, service: OrderService, capsys: pytest.CaptureFixture[str]
    ) -> None:
        service.cancel_order("ORD-001")
        assert capsys.readouterr().out.strip() == "cancel_order executed"

    def test_get_order_status_logs(
        self, service: OrderService, capsys: pytest.CaptureFixture[str]
    ) -> None:
        service.get_order_status("ORD-001")
        assert capsys.readouterr().out.strip() == "get_order_status executed"

    def test_create_order_return_value(self, service: OrderService) -> None:
        assert service.create_order("Widget", 3) == "Order created: 3x Widget"

    def test_cancel_order_return_value(self, service: OrderService) -> None:
        assert service.cancel_order("ORD-001") == "Order ORD-001 cancelled"

    def test_get_order_status_return_value(self, service: OrderService) -> None:
        assert service.get_order_status("ORD-001") == "Order ORD-001 status: processing"


# ---------------------------------------------------------------------------
# Parameterised — multiple method names produce correct log lines
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("method,args,expected_log", [
    ("create_order", ("Gadget", 1), "create_order executed"),
    ("cancel_order", ("ORD-999",), "cancel_order executed"),
    ("get_order_status", ("ORD-123",), "get_order_status executed"),
])
def test_all_service_methods_log_correct_name(
    service: OrderService,
    capsys: pytest.CaptureFixture[str],
    method: str,
    args: tuple,
    expected_log: str,
) -> None:
    getattr(service, method)(*args)
    assert capsys.readouterr().out.strip() == expected_log
