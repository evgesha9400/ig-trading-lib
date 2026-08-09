from decimal import Decimal

from ig_trading_lib.operations.costs import (
    CloseIndicativeCostRequest,
    EditIndicativeCostRequest,
    OpenIndicativeCostRequest,
)


def test_indicative_cost_requests_use_the_official_operation_specific_fields() -> None:
    common = {
        "ask": Decimal("1.09"),
        "bid": Decimal("1.08"),
        "deal_currency_code": "GBP",
        "deal_reference": "deal-reference",
        "size": Decimal("1.5"),
    }

    opened = OpenIndicativeCostRequest(**common)
    closed = CloseIndicativeCostRequest(**common, opening_level=Decimal("1.07"))
    edited = EditIndicativeCostRequest(**common, opening_level=Decimal("1.07"))

    assert opened.to_wire() == {
        "ask": 1.09,
        "bid": 1.08,
        "dealCurrencyCode": "GBP",
        "dealReference": "deal-reference",
        "size": 1.5,
    }
    assert closed.to_wire()["openingLevel"] == 1.07
    assert edited.to_wire()["openingLevel"] == 1.07
