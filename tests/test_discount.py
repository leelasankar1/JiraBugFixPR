import pytest

from discount_app.discount import apply_discount


def test_full_price_no_discount():
    assert apply_discount("10.00", 0) == "10.00"


def test_half_price():
    assert apply_discount("10.00", 50) == "5.00"


def test_string_price():
    assert apply_discount("20.00", 25) == "15.00"


def test_rounds_to_cents():
    assert apply_discount("9.99", 10) == "8.99"


def test_full_discount():
    assert apply_discount("9.99", 100) == "0.00"


@pytest.mark.parametrize("price", ["abc", "NaN", "Infinity"])
def test_invalid_price_raises(price):
    with pytest.raises(ValueError):
        apply_discount(price, 10)


def test_negative_price_raises():
    with pytest.raises(ValueError):
        apply_discount("-1", 10)


@pytest.mark.parametrize("percent", [-1, 101, "NaN", "Infinity", "bad"])
def test_invalid_percent_raises(percent):
    with pytest.raises(ValueError):
        apply_discount("10.00", percent)
