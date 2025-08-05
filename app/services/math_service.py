"""
Business-logic layer that provides
  • cached math helpers  (factorial, fibonacci, power)
  • automatic logging of every call (success OR failure)
in the local SQLite database.

Design choices
--------------
* Iterative implementations to avoid Python recursion limits.
* LRU cache size = 128 per function.
* Input guards:
* n must be 0 … 170 (factorial).
* n must be 0 … 1,476 (Fibonacci).
* power() accepts floats for `base` and floats for `exponent`
  (negative exponents are allowed).
"""

from __future__ import annotations

from datetime import datetime, timezone
from functools import lru_cache
from math import factorial as _py_factorial, isfinite, log10
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.database.db_connection import SessionLocal
from app.models.calculation_model import Request

# Constants
MAX_FACTORIAL_N = 170
MAX_FIBONACCI_N = 1_476


# Helpers: Logging
def _log_request(
        operation: str,
        payload: Dict[str, Any],
        result: Optional[float],
        status: str,
        message: Optional[str] = None
) -> None:
    """
    Insert a row in the `requests` table.
    Opens and closes its own SQLAlchemy session per call.
    """
    db: Session = SessionLocal()
    try:
        entry = Request(
            operation=operation,
            input=payload,
            result=result,  # Result may be None on failure
            timestamp=datetime.now(timezone.utc),
            status=status,
            message=message
        )
        db.add(entry)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# Cached math kernels (pure functions)
@lru_cache(maxsize=128)
def _factorial_cached(n: int) -> int:
    """Iterative factorial with cache."""
    if n < 0:
        raise ValueError("n must be non-negative (n >= 0)")
    if n <= 20:  # Python’s C-optimised factorial is faster for small n
        return _py_factorial(n)
    if n > MAX_FACTORIAL_N:
        raise ValueError(f"n must not exceed {MAX_FACTORIAL_N}")
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result


@lru_cache(maxsize=128)
def _fibonacci_cached(n: int) -> int:
    """Iterative (O(n)) Fibonacci with cache."""
    if n < 0:
        raise ValueError("n must be non-negative (n >= 0)")
    if n > MAX_FIBONACCI_N:
        raise ValueError(f"n must not exceed {MAX_FIBONACCI_N}")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@lru_cache(maxsize=128)
def _power_cached(base: float, exponent: float) -> float:
    """
    Simple power function (allows negative exponent)
    with float overflow protection.
    """
    if base != 0 and exponent > 0:
        if exponent * log10(abs(base)) > 308:
            raise ValueError("Result overflows 64‑bit float; "
                             "try smaller exponent or base")
    try:
        result = base ** exponent
    except OverflowError:
        raise ValueError("Result overflows 64‑bit float; "
                         "try smaller exponent or base") from None
    if not isfinite(result):
        raise ValueError("Result overflows 64‑bit float; "
                         "try smaller exponent or base")
    return result


# Public API called from controllers
def calculate_factorial(n: int) -> int:
    """Compute factorial(n) and log the call."""
    result: Optional[int] = None
    try:
        result = _factorial_cached(n)
        _log_request("factorial",
                     {"n": n},
                     float(result),
                     "success",
                     "Factorial calculated successfully")
        return result
    except ValueError as e:
        _log_request("factorial",
                     {"n": n},
                     None,
                     "error",
                     str(e))
        raise


def calculate_fibonacci(n: int) -> int:
    """Compute fibonacci(n) and log the call."""
    result: Optional[int] = None
    try:
        result = _fibonacci_cached(n)
        _log_request("fibonacci",
                     {"n": n},
                     float(result),
                     "success",
                     "Fibonacci calculated successfully")
        return result
    except ValueError as e:
        _log_request("fibonacci",
                     {"n": n},
                     None,
                     "error",
                     str(e))
        raise


def calculate_power(base: float, exponent: float) -> float:
    """Compute base ** exponent and log the call."""
    result: Optional[float] = None
    try:
        result = _power_cached(base, exponent)
        _log_request("power",
                     {"base": base, "exponent": exponent},
                     result,
                     "success",
                     "Power calculated successfully")
        return result
    except ValueError as e:
        _log_request("power",
                     {"base": base, "exponent": exponent},
                     None,
                     "error",
                     str(e))
        raise
