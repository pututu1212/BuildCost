from decimal import Decimal

from backend.app.services.costing import (
    calculate_cost_layers,
    calculate_item_amount,
    calculate_percentage,
    calculate_subtotal,
)


def test_calculate_item_amount():
    assert calculate_item_amount(
        Decimal("500"),
        Decimal("68"),
    ) == Decimal("34000")


def test_calculate_subtotal():
    assert calculate_subtotal(
        [
            Decimal("42000"),
            Decimal("34000"),
            Decimal("18000"),
        ]
    ) == Decimal("94000")


def test_calculate_percentage():
    assert calculate_percentage(
        Decimal("100000"),
        Decimal("5"),
    ) == Decimal("5000")


def test_calculate_cost_layers():
    result = calculate_cost_layers(
        Decimal("100000"),
        Decimal("5"),
        Decimal("10"),
        Decimal("5"),
    )

    assert result["subtotal"] == Decimal("100000")
    assert result["wastage"] == Decimal("5000")
    assert result["overhead"] == Decimal("10500")
    assert result["contingency"] == Decimal("5775")
    assert result["total"] == Decimal("121275")