from unittest.mock import MagicMock

import requests

from ig_trading_lib.trading.orders import (
    WorkingOrders,
)


def test_get_working_orders(mocker, working_orders, order_service):
    mock_get = mocker.patch("ig_trading_lib.trading.orders.service.requests.get")
    test_working_orders = working_orders
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = test_working_orders
    mock_get.return_value = response

    working_orders = order_service.get_working_orders()

    assert len(working_orders.workingOrders) == 1
    expected = WorkingOrders.model_validate(test_working_orders)
    assert working_orders.model_dump() == expected.model_dump()