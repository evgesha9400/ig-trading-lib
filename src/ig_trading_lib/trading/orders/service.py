import logging

import requests
from pydantic import ValidationError

from ig_trading_lib.trading.models import DealReference
from ig_trading_lib.trading.orders.models import CreateWorkingOrder, WorkingOrders
from ig_trading_lib.trading.service import TradingService

logger = logging.getLogger(__name__)


class OrderException(Exception):
    """Exception raised for errors in the order process."""


class OrderService(TradingService):
    def get_orders(self) -> WorkingOrders:
        """Get working orders list
        :return: WorkingOrders instance
        """
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

    def create_order(self, order: CreateWorkingOrder) -> DealReference:
        """Create a new working order
        :param order: CreateWorkingOrder instance
        :return: DealReference e.g: {'dealReference': 'DIAAAABBBCCC123'}
        """
        url = f"{self.base_url}/gateway/deal/workingorders/otc"
        try:
            response = requests.post(url, headers=self.headers, json=order.model_dump())
            if response.status_code == 200:
                return DealReference.model_validate(response.json())
            else:
                raise OrderException(
                    "Create working order failed with status code %s: %s"
                    % (response.status_code, response.text)
                )
        except ValidationError as e:
            raise OrderException("Invalid create working order response: %s" % e)
        except requests.RequestException as e:
            raise OrderException("Create working order request failed: %s" % e)

    def delete_order(self, deal_id: str) -> DealReference:
        """Delete a working order
        :param deal_id: str
        :return: DealReference e.g: {'dealReference': 'DIAAAABBBCCC123'}
        """
        url = f"{self.base_url}/gateway/deal/workingorders/otc/{deal_id}"
        try:
            response = requests.delete(url, headers=self.headers)
            if response.status_code == 200:
                return DealReference.model_validate(response.json())
            else:
                raise OrderException(
                    "Delete working order failed with status code %s: %s"
                    % (response.status_code, response.text)
                )
        except ValidationError as e:
            raise OrderException("Invalid delete working order response: %s" % e)
        except requests.RequestException as e:
            raise OrderException("Delete working order request failed: %s" % e)
