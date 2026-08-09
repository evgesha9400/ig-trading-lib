from decimal import Decimal

import pytest
from pydantic import ValidationError

from ig_trading_lib.operations.costs import (
    CloseIndicativeCostRequest,
    EditIndicativeCostRequest,
    OpenIndicativeCostRequest,
)
from ig_trading_lib.operations.dealing import CreatePositionRequest


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


def test_create_position_accepts_every_official_order_type_and_field() -> None:
    quote = CreatePositionRequest(
        epic="CS.D.EURUSD.CFD.IP",
        direction="BUY",
        size=1,
        order_type="QUOTE",
        currency_code="GBP",
        level=Decimal("1.08"),
        quote_id="quote-id",
        time_in_force="FILL_OR_KILL",
    )

    assert quote.to_wire()["quoteId"] == "quote-id"
    assert quote.to_wire()["timeInForce"] == "FILL_OR_KILL"


@pytest.mark.parametrize(
    "overrides",
    [
        {"order_type": "STOP"},
        {"order_type": "LIMIT"},
        {"order_type": "LIMIT", "level": 1, "quote_id": "not-allowed"},
        {"order_type": "MARKET", "level": 1},
        {"order_type": "MARKET", "quote_id": "not-allowed"},
        {"order_type": "QUOTE", "level": 1},
        {"order_type": "QUOTE", "quote_id": "quote-id"},
        {"limit_level": 2, "limit_distance": 1},
        {"stop_level": 2, "stop_distance": 1},
        {"stop_level": 2, "force_open": False},
        {"guaranteed_stop": True},
        {"trailing_stop": False, "trailing_stop_increment": 1},
        {
            "trailing_stop": True,
            "stop_distance": 1,
            "stop_level": 2,
            "trailing_stop_increment": 0.1,
        },
        {"trailing_stop": True, "stop_distance": 1},
    ],
)
def test_create_position_rejects_official_cross_field_violations(
    overrides: dict[str, object],
) -> None:
    values: dict[str, object] = {
        "epic": "CS.D.EURUSD.CFD.IP",
        "direction": "BUY",
        "size": 1,
        "order_type": "MARKET",
        "currency_code": "GBP",
    }
    values.update(overrides)

    with pytest.raises(ValidationError):
        CreatePositionRequest.model_validate(values)
