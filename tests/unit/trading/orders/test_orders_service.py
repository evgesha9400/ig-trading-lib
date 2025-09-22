from decimal import Decimal
from unittest.mock import MagicMock

import requests

from ig_trading_lib.trading import CreateWorkingOrder, WorkingOrders


def test_get_working_orders(mocker, working_orders, order_service):
    mock_get = mocker.patch("ig_trading_lib.trading.client.requests.get")
    test_working_orders = working_orders
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = test_working_orders
    mock_get.return_value = response

    working_orders = order_service.get_orders()

    assert len(working_orders.workingOrders) == 1
    expected = WorkingOrders.model_validate(test_working_orders)
    assert working_orders.model_dump() == expected.model_dump()


def test_create_working_order(mocker, order_service):
    mock_post = mocker.patch("ig_trading_lib.trading.client.requests.post")
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = {"dealReference": "DIAAAABBBCCC123"}
    mock_post.return_value = response

    response = order_service.create_order(
        order=CreateWorkingOrder.model_validate(
            {
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
        )
    )
    assert response.model_dump() == {"dealReference": "DIAAAABBBCCC123"}
    assert mock_post.call_count == 1
