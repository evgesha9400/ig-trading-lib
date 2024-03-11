from unittest import mock
from unittest.mock import MagicMock

import requests

from ig_trading_lib.trading.models import OpenPositions, OpenPosition
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
