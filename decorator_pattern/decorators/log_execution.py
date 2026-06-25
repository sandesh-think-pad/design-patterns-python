"""
Core logging decorator for the Decorator Pattern showcase.

Decorator Pattern role: Decorator function — wraps any callable and prints
'<function_name> executed' to stdout after each successful call, without
changing the wrapped function's signature, return value, or name.
"""

import functools
from collections.abc import Callable
from typing import Any


def log_execution(func: Callable[..., Any]) -> Callable[..., Any]:
    """Wrap func to print '<func_name> executed' after each call."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        print(f"{func.__name__} executed")
        return result

    return wrapper
