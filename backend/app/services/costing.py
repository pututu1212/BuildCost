from decimal import Decimal


def calculate_item_amount(
    quantity: Decimal,
    unit_rate: Decimal,
) -> Decimal:
    return quantity * unit_rate


def calculate_subtotal(amounts: list[Decimal]) -> Decimal:
    return sum(amounts, Decimal("0"))


def calculate_percentage(
    amount: Decimal,
    percentage: Decimal,
) -> Decimal:
    return amount * percentage / Decimal("100")


def calculate_cost_layers(
    subtotal: Decimal,
    wastage_percent: Decimal = Decimal("0"),
    overhead_percent: Decimal = Decimal("0"),
    contingency_percent: Decimal = Decimal("0"),
) -> dict[str, Decimal]:
    wastage = calculate_percentage(
        subtotal,
        wastage_percent,
    )

    overhead_base = subtotal + wastage

    overhead = calculate_percentage(
        overhead_base,
        overhead_percent,
    )

    contingency_base = overhead_base + overhead

    contingency = calculate_percentage(
        contingency_base,
        contingency_percent,
    )

    total = (
        subtotal
        + wastage
        + overhead
        + contingency
    )

    return {
        "subtotal": subtotal,
        "wastage": wastage,
        "overhead": overhead,
        "contingency": contingency,
        "total": total,
    }