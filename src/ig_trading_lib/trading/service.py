import logging

import requests
from pydantic import ValidationError

from ig_trading_lib import Tokens
from ig_trading_lib.trading.models import DealConfirmation, DealReference

logger = logging.getLogger(__name__)


class TradingException(Exception):
    """Exception raised for errors in the trading process."""


class TradingService:
    def __init__(self, api_key: str, tokens: Tokens, base_url: str):
        """Initialize the trading service.
        :param api_key: Your IG API key.
        :param tokens: Authentication tokens for the IG API.
        :param base_url: The base URL for the IG API (live or demo). e.g: https://demo-api.ig.com/gateway/deal
        """

        self.api_key = api_key
        self.tokens = tokens
        self.base_url = base_url

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json; charset=utf-8",
            "Version": "2",
            "X-IG-API-KEY": self.api_key,
            "X-SECURITY-TOKEN": self.tokens.x_security_token,
            "CST": self.tokens.cst_token,
        }

    def confirms(self, deal_reference: DealReference) -> DealConfirmation:
        """Returns a deal confirmation for the given deal reference.

        Please note, this should only be used if the deal confirmation isn't
        received via the streaming API.

        :param deal_reference: DealReference. The deal reference to get confirmation for.
        :return: DealConfirmation. The deal confirmation for the given deal reference.
        """
        url = f"{self.base_url}/gateway/deal/confirms/{deal_reference.dealReference}"
        headers = self.headers.copy()
        headers["Version"] = "1"

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return DealConfirmation.model_validate(response.json())
            else:
                raise TradingException(
                    "Deal confirmation request failed with status code %s: %s"
                    % (response.status_code, response.text)
                )
        except ValidationError as e:
            raise TradingException("Invalid deal confirmation response: %s" % e)
        except requests.RequestException as e:
            raise TradingException("Deal confirmation request failed: %s" % e)
