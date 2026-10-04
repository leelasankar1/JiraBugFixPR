"""Utilities for calculating percentage discounts."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

_CENT = Decimal("0.01")


def _as_decimal(value, name):
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"invalid {name}: {value!r}") from exc
    if not result.is_finite():
        raise ValueError(f"{name} must be finite")
    return result


def apply_discount(price, percent):
    """Return the discounted price as a two-decimal string.

    ``price`` may be a string or number. ``percent`` must be between 0 and 100.
    Rounding uses conventional half-up currency rounding.
    """
    amount = _as_decimal(price, "price")
    rate = _as_decimal(percent, "discount percent")

    if amount < 0:
        raise ValueError("price cannot be negative")
    if rate < 0 or rate > 100:
        raise ValueError("discount percent must be between 0 and 100")

    remaining_percent = Decimal("100") - rate
    discounted = amount * remaining_percent / Decimal("100")
    return str(discounted.quantize(_CENT, rounding=ROUND_HALF_UP))
