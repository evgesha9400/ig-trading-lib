from decimal import Decimal

import pytest
from pydantic import ValidationError

from ig_trading_lib.trading import CreateWorkingOrder, WorkingOrders


def test_working_orders_validation(working_orders):
    working_order = WorkingOrders.model_validate(working_orders)
    assert working_order is not None


@pytest.mark.parametrize(
    "data, error",
    [
        # Testing missing stopLevel when guaranteedStop is True
        (
            {"guaranteedStop": True, "stopLevel": None, "stopDistance": None},
            "When guaranteedStop is true, specify exactly one of stopLevel or stopDistance.",
        ),
        # Testing both stopLevel and stopDistance when guaranteedStop is True
        (
            {
                "guaranteedStop": True,
                "stopLevel": Decimal("100.0"),
                "stopDistance": Decimal("10.0"),
            },
            "When guaranteedStop is true, specify exactly one of stopLevel or stopDistance.",
        ),
        # Testing both limitLevel and limitDistance
        (
            {"limitLevel": Decimal("100.0"), "limitDistance": Decimal("10.0")},
            "Set only one of limitLevel or limitDistance.",
        ),
        # Testing timeInForce GOOD_TILL_DATE without goodTillDate
        (
            {"timeInForce": "GOOD_TILL_DATE", "goodTillDate": None},
            "timeInForce GOOD_TILL_DATE requires a goodTillDate value.",
        ),
        # Valid scenario for guaranteedStop
        (
            {
                "guaranteedStop": True,
                "stopLevel": Decimal("100.0"),
            },
            None,  # No error expected
        ),
        # Valid scenario for limitLevel
        (
            {
                "limitLevel": Decimal("100.0"),
            },
            None,  # No error expected
        ),
        # Valid scenario for limitDistance
        (
            {
                "limitDistance": Decimal("10.0"),
            },
            None,  # No error expected
        ),
        # Valid scenario for timeInForce GOOD_TILL_DATE with goodTillDate
        (
            {
                "timeInForce": "GOOD_TILL_DATE",
                "goodTillDate": "2023/12/31 23:59:59",
            },
            None,  # No error expected
        ),
    ],
)
def test_create_working_order_validation(data, error):
    base_data = {
        "currencyCode": "USD",
        "direction": "BUY",
        "epic": "IX.D.FTSE.DAILY.IP",
        "expiry": "DFB",
        "forceOpen": True,
        "goodTillDate": "2023/12/31 23:59:59",
        "level": Decimal("1.0"),
        "size": Decimal("1.0"),
        "type": "LIMIT",
        "guaranteedStop": False,
        "timeInForce": "GOOD_TILL_CANCELLED",
    }
    base_data.update(data)

    if error is not None:
        # Check that the validation error is raised with the expected message
        with pytest.raises(ValidationError, match=error):
            CreateWorkingOrder.model_validate(base_data)
    else:
        # Check that the data is validated without raising an error
        working_order = CreateWorkingOrder.model_validate(base_data)
        assert working_order is not None
