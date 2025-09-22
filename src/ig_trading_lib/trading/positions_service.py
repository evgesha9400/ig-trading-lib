import logging

from pydantic import ValidationError

from .client import TradingClient
from .models import DealReference
from .positions_models import (
    ClosePosition,
    CreatePosition,
    OpenPosition,
    OpenPositions,
    UpdatePosition,
)

logger = logging.getLogger(__name__)


class PositionsError(Exception):
    pass


class PositionService:
    def __init__(self, client: TradingClient) -> None:
        self.client = client

    def get_open_position_by_deal_id(self, deal_id: str) -> OpenPosition:
        try:
            resp = self.client.get(f"/gateway/deal/positions/{deal_id}")
            if resp.status_code == 200:
                return OpenPosition.model_validate(resp.json())
            raise PositionsError(f"Open position request failed with status code {resp.status_code}: {resp.text}")
        except ValidationError as e:
            raise PositionsError(f"Invalid open position response: {e}")

    def get_open_positions(self) -> OpenPositions:
        try:
            resp = self.client.get("/gateway/deal/positions")
            if resp.status_code == 200:
                return OpenPositions.model_validate(resp.json())
            raise PositionsError(f"Open positions request failed with status code {resp.status_code}: {resp.text}")
        except ValidationError as e:
            raise PositionsError(f"Invalid open positions response: {e}")

    def create_position(self, position: CreatePosition) -> DealReference:
        try:
            resp = self.client.post("/gateway/deal/positions/otc", json=position.model_dump())
            if resp.status_code == 200:
                return DealReference.model_validate(resp.json())
            raise PositionsError(f"Create position request failed with status code {resp.status_code}: {resp.text}")
        except ValidationError as e:
            raise PositionsError(f"Invalid create position response: {e}")

    def update_position(self, deal_id: str, position: UpdatePosition) -> DealReference:
        try:
            resp = self.client.put(f"/gateway/deal/positions/otc/{deal_id}", json=position.model_dump())
            if resp.status_code == 200:
                return DealReference.model_validate(resp.json())
            raise PositionsError(f"Update position request failed with status code {resp.status_code}: {resp.text}")
        except ValidationError as e:
            raise PositionsError(f"Invalid update position response: {e}")

    def close_position(self, position: ClosePosition) -> DealReference:
        headers = {"Version": "1", "_method": "DELETE"}
        try:
            resp = self.client.post(
                "/gateway/deal/positions/otc",
                json=position.model_dump(exclude_none=True),
                headers=headers,
            )
            if resp.status_code == 200:
                return DealReference.model_validate(resp.json())
            raise PositionsError(f"Close position request failed with status code {resp.status_code}: {resp.text}")
        except ValidationError as e:
            raise PositionsError(f"Invalid close position response: {e}")
