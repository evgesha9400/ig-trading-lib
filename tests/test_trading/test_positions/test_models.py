from decimal import Decimal

import pytest
from pydantic import ValidationError

from ig_trading_lib.trading.positions import (
    ClosePosition,
    CreatePosition,
    UpdatePosition,
)


@pytest.mark.parametrize(
    "data, error",
    [
        # Force Open constraints
        (
            {"forceOpen": False, "limitDistance": Decimal("10.0")},
            "forceOpen must be true if limit or stop constraints are set.",
        ),
        ({"forceOpen": True, "limitDistance": Decimal("10.0")}, None),
        (
            {"forceOpen": False, "limitLevel": Decimal("100.0")},
            "forceOpen must be true if limit or stop constraints are set.",
        ),
        ({"forceOpen": True, "limitLevel": Decimal("100.0")}, None),
        (
            {"forceOpen": False, "stopDistance": Decimal("10.0")},
            "forceOpen must be true if limit or stop constraints are set.",
        ),
        ({"forceOpen": True, "stopDistance": Decimal("10.0")}, None),
        (
            {"forceOpen": False, "stopLevel": Decimal("100.0")},
            "forceOpen must be true if limit or stop constraints are set.",
        ),
        ({"forceOpen": True, "stopLevel": Decimal("100.0")}, None),
        # Guaranteed Stop constraints
        (
            {
                "guaranteedStop": True,
                "stopLevel": Decimal("100.0"),
                "stopDistance": Decimal("10.0"),
            },
            "When guaranteedStop is true, specify exactly one of stopLevel or stopDistance.",
        ),
        ({"guaranteedStop": True, "stopLevel": Decimal("100.0")}, None),
        # Order Type constraints
        (
            {"orderType": "LIMIT", "quoteId": "12345"},
            "Do not set quoteId when orderType is LIMIT.",
        ),
        (
            {"orderType": "MARKET", "level": Decimal("100.0")},
            "Do not set level or quoteId when orderType is MARKET.",
        ),
        ({"orderType": "QUOTE", "level": Decimal("100.0"), "quoteId": "12345"}, None),
        # Trailing Stop constraints
        (
            {"trailingStop": True, "stopLevel": Decimal("100.0")},
            "Do not set stopLevel when trailingStop is true.",
        ),
        (
            {"trailingStop": True, "guaranteedStop": True},
            "guaranteedStop must be false when trailingStop is true.",
        ),
        (
            {
                "trailingStop": True,
                "stopDistance": Decimal("10.0"),
                "trailingStopIncrement": Decimal("1.0"),
            },
            None,
        ),
        # Unique constraints
        (
            {"limitLevel": Decimal("100.0"), "limitDistance": Decimal("10.0")},
            "Set only one of limitLevel or limitDistance.",
        ),
        (
            {"stopLevel": Decimal("100.0"), "stopDistance": Decimal("10.0")},
            "Set only one of stopLevel or stopDistance.",
        ),
    ],
)
def test_create_position_model_validation(data, error):
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
        # Check that the validation error is raised with the expected message
        with pytest.raises(ValidationError, match=error):
            CreatePosition.model_validate(base_data)
    else:
        # Check that the data is validated without raising an error
        position = CreatePosition.model_validate(base_data)
        assert position is not None


@pytest.mark.parametrize(
    "data, error",
    [
        # Order Type constraints
        (
            {"orderType": "QUOTE", "quoteId": None, "level": Decimal("100.0")},
            "quoteId is required when orderType is QUOTE.",
        ),
        (
            {"orderType": "MARKET", "level": Decimal("100.0"), "quoteId": "12345"},
            "level and quoteId are not allowed when orderType is MARKET.",
        ),
        (
            {"orderType": "LIMIT", "quoteId": "12345"},
            "quoteId is not allowed when orderType is LIMIT.",
        ),
        (
            {"orderType": "LIMIT", "level": None},
            "level is required when orderType is LIMIT.",
        ),
        # Unique constraints
        (
            {"dealId": "DIAAAABBBCCC123", "epic": "CS.D.GBPUSD.TODAY.IP"},
            "Set only one of dealId or epic.",
        ),
        (
            {"dealId": None, "epic": None},
            "Set one of dealId or epic.",
        ),
    ],
)
def test_close_position_model_validation(data, error):
    base_data = {
        "direction": "SELL",
        "orderType": "MARKET",
        "size": Decimal("1"),
        "timeInForce": "EXECUTE_AND_ELIMINATE",
        "dealId": "DIAAAABBBCCC123",
    }
    base_data.update(data)

    if error is not None:
        # Check that the validation error is raised with the expected message
        with pytest.raises(ValidationError, match=error):
            ClosePosition.model_validate(base_data)
    else:
        # Check that the data is validated without raising an error
        position = ClosePosition.model_validate(base_data)
        assert position is not None


@pytest.mark.parametrize(
    "data, expected_error",
    [
        # Testing guaranteedStop and trailingStop conflict
        (
            {
                "guaranteedStop": True,
                "trailingStop": True,
                "stopLevel": Decimal("100.0"),
            },
            "guaranteedStop and trailingStop cannot both be true.",
        ),
        # Testing missing stopLevel when guaranteedStop is True
        (
            {"guaranteedStop": True, "trailingStop": False},
            "If guaranteedStop is true, then stopLevel must be set.",
        ),
        # Testing trailingStop constraints when it's True
        (
            {"trailingStop": True, "guaranteedStop": False},
            "If trailingStop is true, then trailingStopDistance, trailingStopIncrement, and stopLevel.",
        ),
        # Testing forbidden trailingStopDistance when trailingStop is False
        (
            {"trailingStop": False, "trailingStopDistance": Decimal("10.0")},
            "If trailingStop is false, then DO NOT set trailingStopDistance or trailingStopIncrement.",
        ),
        # Valid scenario for guaranteedStop
        (
            {
                "guaranteedStop": True,
                "stopLevel": Decimal("100.0"),
                "trailingStop": False,
            },
            None,  # No error expected
        ),
        # Valid scenario for trailingStop
        (
            {
                "trailingStop": True,
                "trailingStopDistance": Decimal("5.0"),
                "trailingStopIncrement": Decimal("1.0"),
                "stopLevel": Decimal("100.0"),
                "guaranteedStop": False,
            },
            None,  # No error expected
        ),
    ],
)
def test_update_position_validation(data, expected_error):
    if expected_error:
        with pytest.raises(ValueError, match=expected_error):
            UpdatePosition.model_validate(data)
    else:
        position = UpdatePosition.model_validate(data)
        assert position is not None
