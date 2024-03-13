from unittest.mock import MagicMock

import requests

from ig_trading_lib.trading.models import (
    OpenPositions,
    OpenPosition,
    CreatePosition,
    ClosePosition,
    UpdatePosition,
)


def test_get_open_positions(mocker, open_position, position_service):
    mock_get = mocker.patch("ig_trading_lib.trading.positions.requests.get")
    test_positions = {"positions": [open_position]}
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = test_positions
    mock_get.return_value = response

    positions = position_service.get_open_positions()

    assert len(positions.positions) == 1
    expected = OpenPositions.model_validate(test_positions)
    assert positions.model_dump() == expected.model_dump()


def test_get_open_position_by_deal_id(mocker, open_position, position_service):
    mock_get = mocker.patch("ig_trading_lib.trading.positions.requests.get")
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = open_position
    mock_get.return_value = response

    position = position_service.get_open_position_by_deal_id(
        deal_id=open_position["position"]["dealId"],
    )
    expected = OpenPosition.model_validate(open_position)
    assert position.model_dump() == expected.model_dump()


def test_create_position(mocker, position_service):
    mock_post = mocker.patch("ig_trading_lib.trading.positions.requests.post")
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = {"dealReference": "DIAAAABBBCCC123"}
    mock_post.return_value = response

    response = position_service.create_position(
        create=CreatePosition.model_validate(
            {
                "currencyCode": "USD",
                "direction": "BUY",
                "epic": "CS.D.GBPUSD.TODAY.IP",
                "expiry": "DFB",
                "forceOpen": True,
                "guaranteedStop": False,
                "orderType": "MARKET",
                "size": 1,
                "timeInForce": "EXECUTE_AND_ELIMINATE",
                "trailingStop": False,
            }
        )
    )
    assert response == {"dealReference": "DIAAAABBBCCC123"}
    assert mock_post.call_count == 1


def test_close_position(mocker, position_service):
    mock_post = mocker.patch("ig_trading_lib.trading.positions.requests.post")
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = {"dealReference": "DIAAAABBBCCC123"}
    mock_post.return_value = response

    response = position_service.close_position(
        close=ClosePosition.model_validate(
            {
                "direction": "SELL",
                "orderType": "MARKET",
                "size": 1,
                "timeInForce": "EXECUTE_AND_ELIMINATE",
                "dealId": "DIAAAAPJCL8RHAM",
            }
        )
    )
    assert response == {"dealReference": "DIAAAABBBCCC123"}
    assert mock_post.call_count == 1


def test_update_position(mocker, position_service):
    mock_put = mocker.patch("ig_trading_lib.trading.positions.requests.put")
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = {"dealReference": "DIAAAABBBCCC123"}
    mock_put.return_value = response

    response = position_service.update_position(
        deal_id="DIAAAAPJCL8RHAM",
        update=UpdatePosition.model_validate(
            {
                "limitLevel": 1.0,
                "stopLevel": 1.0,
            }
        ),
    )
    assert response == {"dealReference": "DIAAAABBBCCC123"}
    assert mock_put.call_count == 1
