import logging

from ig_trading_lib import Tokens
from .models import WorkingOrders
import requests
from pydantic import ValidationError


logger = logging.getLogger(__name__)


class OrderException(Exception):
    """Exception raised for errors in the order process."""
    pass


class OrderService:
    def __init__(self, api_key: str, tokens: Tokens, base_url: str):
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


    def get_working_orders(self) -> WorkingOrders:
        """Get working orders list"""
        url = f"{self.base_url}/gateway/deal/workingorders"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return WorkingOrders.model_validate(response.json())
            else:
                raise OrderException(
                    "Working orders failed with status code %s: %s"
                    % (response.status_code, response.text)
                )
        except ValidationError as e:
            raise OrderException("Invalid working orders response: %s" % e)
        except requests.RequestException as e:
            raise OrderException("Working orders request failed: %s" % e)
