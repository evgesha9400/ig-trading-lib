import logging

from pydantic import ValidationError

from ig_trading_lib.trading.client import TradingClient
from ig_trading_lib.trading.models import DealReference
from ig_trading_lib.trading.orders_models import CreateWorkingOrder, UpdateWorkingOrder, WorkingOrders

logger = logging.getLogger(__name__)


class OrderException(Exception):
    pass


class OrderService:
    def __init__(self, client: TradingClient) -> None:
        self.client = client

    def get_orders(self) -> WorkingOrders:
        try:
            resp = self.client.get("/gateway/deal/workingorders")
            if resp.status_code == 200:
                return WorkingOrders.model_validate(resp.json())
            raise OrderException(f"Working orders failed with status code {resp.status_code}: {resp.text}")
        except ValidationError as e:
            raise OrderException(f"Invalid working orders response: {e}")

    def create_order(self, order: CreateWorkingOrder) -> DealReference:
        try:
            resp = self.client.post("/gateway/deal/workingorders/otc", json=order.model_dump())
            if resp.status_code == 200:
                return DealReference.model_validate(resp.json())
            raise OrderException(f"Create working order failed with status code {resp.status_code}: {resp.text}")
        except ValidationError as e:
            raise OrderException(f"Invalid create working order response: {e}")

    def update_order(self, deal_id: str, order: UpdateWorkingOrder) -> DealReference:
        try:
            resp = self.client.put(f"/gateway/deal/workingorders/otc/{deal_id}", json=order.model_dump())
            if resp.status_code == 200:
                return DealReference.model_validate(resp.json())
            raise OrderException(f"Update working order failed with status code {resp.status_code}: {resp.text}")
        except ValidationError as e:
            raise OrderException(f"Invalid update working order response: {e}")

    def delete_order(self, deal_id: str) -> DealReference:
        try:
            resp = self.client.delete(f"/gateway/deal/workingorders/otc/{deal_id}")
            if resp.status_code == 200:
                return DealReference.model_validate(resp.json())
            raise OrderException(f"Delete working order failed with status code {resp.status_code}: {resp.text}")
        except ValidationError as e:
            raise OrderException(f"Invalid delete working order response: {e}")
