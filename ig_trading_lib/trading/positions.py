from typing import Dict

import requests
from pydantic import ValidationError

from ig_trading_lib import Tokens
from .models import OpenPositions, OpenPosition, CreatePosition


class PositionsError(Exception):
    """Exception raised for errors in the positions process."""


def get_open_position_by_deal_id(
    api_key: str, tokens: Tokens, base_url: str, deal_id: str
) -> OpenPosition:
    """Get open position by deal ID for the authenticated account.
    :param api_key: str. Your IG API key.
    :param tokens: Tokens. The authentication tokens.
    :param base_url: str. The base URL for the IG API. e.g. 'https://demo-api.ig.com'.
    :param deal_id: str. The deal ID of the open position.
    :return: OpenPosition. The open position for the authenticated account.
    """
    url = f"{base_url}/gateway/deal/positions/{deal_id}"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json; charset=utf-8",
        "Version": "2",
        "X-IG-API-KEY": api_key,
        "X-SECURITY-TOKEN": tokens.x_security_token,
        "CST": tokens.cst_token,
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return OpenPosition.model_validate(response.json())
        else:
            raise PositionsError(
                "Open position by deal ID request failed with status code %s: %s"
                % (response.status_code, response.text)
            )
    except ValidationError as e:
        raise PositionsError(f"Invalid open position by deal ID response: %s" % e)
    except requests.RequestException as e:
        raise PositionsError(f"Open position by deal ID request failed: %s" % e)


def get_open_positions(api_key: str, tokens: Tokens, base_url: str) -> OpenPositions:
    """Get open positions for the authenticated account.
    :param api_key: str. Your IG API key.
    :param tokens: Tokens. The authentication tokens.
    :param base_url: str. The base URL for the IG API. e.g. 'https://demo-api.ig.com'.
    :return: OpenPositions. The open positions for the authenticated account.
    """
    url = f"{base_url}/gateway/deal/positions"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json; charset=utf-8",
        "Version": "2",
        "X-IG-API-KEY": api_key,
        "X-SECURITY-TOKEN": tokens.x_security_token,
        "CST": tokens.cst_token,
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return OpenPositions.model_validate(response.json())
        else:
            raise PositionsError(
                "Open positions request failed with status code %s: %s"
                % (response.status_code, response.text)
            )
    except ValidationError as e:
        raise PositionsError(f"Invalid open positions response: %s" % e)
    except requests.RequestException as e:
        raise PositionsError(f"Open positions request failed: %s" % e)


def create_position(
    api_key: str, tokens: Tokens, base_url: str, position: CreatePosition
) -> Dict[str, str]:
    """Create a new position for the authenticated account.
    :param api_key: str. Your IG API key.
    :param tokens: Tokens. The authentication tokens.
    :param base_url: str. The base URL for the IG API. e.g. 'https://demo-api.ig.com'.
    :param position: CreatePosition. The position to create.
    :return: dict. The response from the IG API. e.g. {'dealReference': 'DIAAAABBBCCC123'}
    """

    url = f"{base_url}/gateway/deal/positions/otc"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json; charset=utf-8",
        "Version": "2",
        "X-IG-API-KEY": api_key,
        "X-SECURITY-TOKEN": tokens.x_security_token,
        "CST": tokens.cst_token,
    }
    try:
        response = requests.post(url, headers=headers, json=position.model_dump())
        if response.status_code == 200:
            return response.json()
        else:
            raise PositionsError(
                "Create position request failed with status code %s: %s"
                % (response.status_code, response.text)
            )
    except requests.RequestException as e:
        raise PositionsError(f"Create position request failed: %s" % e)
