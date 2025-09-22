from decimal import Decimal
from unittest.mock import MagicMock

import requests

from ig_trading_lib.trading import CreateWorkingOrder, UpdateWorkingOrder, WorkingOrders


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


def test_update_working_order(mocker, order_service):
    mock_put = mocker.patch("ig_trading_lib.trading.client.requests.put")
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = {"dealReference": "DIAAAABBBCCC456"}
    mock_put.return_value = response

    deal_id = "DEAL123"
    update_order = UpdateWorkingOrder(level=Decimal("7500.0"))
    result = order_service.update_order(deal_id, update_order)

    assert result.dealReference == "DIAAAABBBCCC456"
    assert mock_put.call_count == 1


def test_delete_working_order(mocker, order_service):
    mock_delete = mocker.patch("ig_trading_lib.trading.client.requests.delete")
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = {"dealReference": "DIAAAABBBCCC789"}
    mock_delete.return_value = response

    deal_id = "DEAL456"
    result = order_service.delete_order(deal_id)

    assert result.dealReference == "DIAAAABBBCCC789"
    assert mock_delete.call_count == 1
