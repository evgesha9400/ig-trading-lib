from decimal import Decimal
from unittest import mock
from unittest.mock import MagicMock

import pytest
import requests
from pydantic import ValidationError

from ig_trading_lib.trading.models import OpenPositions, OpenPosition, CreatePosition
from ig_trading_lib.trading.positions import (
    get_open_positions,
    get_open_position_by_deal_id,
)


@mock.patch("ig_trading_lib.trading.positions.requests.get")
def test_get_open_positions(mock_get, api_key, tokens, test_open_position):
    test_positions = {"positions": [test_open_position]}
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = test_positions
    mock_get.return_value = response

    positions = get_open_positions(
        api_key=api_key, tokens=tokens, base_url="https://demo-api.ig.com"
    )

    assert len(positions.positions) == 1
    expected = OpenPositions.model_validate(test_positions)
    assert positions == expected


@mock.patch("ig_trading_lib.trading.positions.requests.get")
def test_get_open_position_by_deal_id(mock_get, api_key, tokens, test_open_position):
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = test_open_position
    mock_get.return_value = response

    position = get_open_position_by_deal_id(
        deal_id=test_open_position["position"]["dealId"],
        api_key=api_key,
        tokens=tokens,
        base_url="https://demo-api.ig.com",
    )
    expected = OpenPosition.model_validate(test_open_position)
    assert position == expected


@pytest.mark.parametrize("data, error", [
    # Force Open constraints
    ({"forceOpen": False, "limitDistance": Decimal("10.0")}, "forceOpen must be true if limit or stop constraints are set."),
    ({"forceOpen": True, "limitDistance": Decimal("10.0")}, None),
    ({"forceOpen": False, "limitLevel": Decimal("100.0")}, "forceOpen must be true if limit or stop constraints are set."),
    ({"forceOpen": True, "limitLevel": Decimal("100.0")}, None),
    ({"forceOpen": False, "stopDistance": Decimal("10.0")}, "forceOpen must be true if limit or stop constraints are set."),
    ({"forceOpen": True, "stopDistance": Decimal("10.0")}, None),
    ({"forceOpen": False, "stopLevel": Decimal("100.0")}, "forceOpen must be true if limit or stop constraints are set."),
    ({"forceOpen": True, "stopLevel": Decimal("100.0")}, None),
    # Guaranteed Stop constraints
    ({"guaranteedStop": True, "stopLevel": Decimal("100.0"), "stopDistance": Decimal("10.0")}, "When guaranteedStop is true, specify exactly one of stopLevel or stopDistance."),
    ({"guaranteedStop": True, "stopLevel": Decimal("100.0")}, None),
    # Order Type constraints
    ({"orderType": "LIMIT", "quoteId": "12345"}, "Do not set quoteId when orderType is LIMIT."),
    ({"orderType": "MARKET", "level": Decimal("100.0")}, "Do not set level or quoteId when orderType is MARKET."),
    ({"orderType": "QUOTE", "level": Decimal("100.0"), "quoteId": "12345"}, None),
    # Trailing Stop constraints
    ({"trailingStop": True, "stopLevel": Decimal("100.0")}, "Do not set stopLevel when trailingStop is true."),
    ({"trailingStop": True, "guaranteedStop": True}, "guaranteedStop must be false when trailingStop is true."),
    ({"trailingStop": True, "stopDistance": Decimal("10.0"), "trailingStopIncrement": Decimal("1.0")}, None),
    # Unique constraints
    ({"limitLevel": Decimal("100.0"), "limitDistance": Decimal("10.0")}, "Set only one of limitLevel or limitDistance."),
    ({"stopLevel": Decimal("100.0"), "stopDistance": Decimal("10.0")}, "Set only one of stopLevel or stopDistance."),
])
def test_create_position_validation(data, error):
    base_data = {
        "currencyCode": "USD",
        "direction": "BUY",
        "epic": "IX.D.FTSE.DAILY.IP",
        "expiry": "DFB",
        "forceOpen": True,
        "guaranteedStop": False,
        "orderType": "MARKET",
        "size": Decimal("1"),
        "timeInForce": "EXECUTE_AND_ELIMINATE",
        "trailingStop": False,
    }
    base_data.update(data)

    if error is not None:
        with pytest.raises(ValidationError, match=error):
            CreatePosition.model_validate(base_data)
    else:
        position = CreatePosition.model_validate(base_data)
        assert position is not None