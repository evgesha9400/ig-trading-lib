import logging

import requests
from pydantic import ValidationError

from ig_trading_lib.trading.models import DealReference
from ig_trading_lib.trading.positions.models import (
    ClosePosition,
    CreatePosition,
    OpenPosition,
    OpenPositions,
    UpdatePosition,
)
from ig_trading_lib.trading.service import TradingService

logger = logging.getLogger(__name__)


class PositionsError(Exception):
    """Exception raised for errors in the positions process."""


class PositionService(TradingService):
    def get_open_position_by_deal_id(self, deal_id: str) -> OpenPosition:
        """Get open position by deal ID for the authenticated account.
        :param deal_id: str. The deal ID of the open position.
        :return: OpenPosition. The open position for the authenticated account.
        """
        url = f"{self.base_url}/gateway/deal/positions/{deal_id}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return OpenPosition.model_validate(response.json())
            else:
                raise PositionsError(
                    "Open position request failed with status code %s: %s"
                    % (response.status_code, response.text)
                )
        except ValidationError as e:
            raise PositionsError("Invalid open position response: %s" % e)
        except requests.RequestException as e:
            raise PositionsError("Open position request failed: %s" % e)

    def get_open_positions(self) -> OpenPositions:
        """Get open positions for the authenticated account.
        :return: OpenPositions. The open positions for the authenticated account.
        """
        url = f"{self.base_url}/gateway/deal/positions"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return OpenPositions.model_validate(response.json())
            else:
                raise PositionsError(
                    "Open positions request failed with status code %s: %s"
                    % (response.status_code, response.text)
                )
        except ValidationError as e:
            raise PositionsError("Invalid open positions response: %s" % e)
        except requests.RequestException as e:
            raise PositionsError("Open positions request failed: %s" % e)

    def create_position(self, position: CreatePosition) -> DealReference:
        """Create a new position for the authenticated account.
        :param position: CreatePosition. The position to create.
        :return: DealReference e.g: {'dealReference': 'DIAAAABBBCCC123'}
        """

        url = f"{self.base_url}/gateway/deal/positions/otc"
        try:
            response = requests.post(
                url, headers=self.headers, json=position.model_dump()
            )
            if response.status_code == 200:
                return DealReference.model_validate(response.json())
            else:
                raise PositionsError(
                    "Create position request failed with status code %s: %s"
                    % (response.status_code, response.text)
                )
        except requests.RequestException as e:
            raise PositionsError("Create position request failed: %s" % e)

    def update_position(self, deal_id: str, position: UpdatePosition) -> DealReference:
        """Update a position for the authenticated account.
        :param deal_id: str. The deal ID of the position to update.
        :param position: UpdatePosition. Position update details.
        :return: DealReference e.g: {'dealReference': 'DIAAAABBBCCC123'}
        """

        url = f"{self.base_url}/gateway/deal/positions/otc/{deal_id}"
        try:
            response = requests.put(
                url, headers=self.headers, json=position.model_dump()
            )
            if response.status_code == 200:
                return DealReference.model_validate(response.json())
            else:
                raise PositionsError(
                    "Update position request failed with status code %s: %s"
                    % (response.status_code, response.text)
                )
        except requests.RequestException as e:
            raise PositionsError("Update position request failed: %s" % e)

    def close_position(self, position: ClosePosition) -> DealReference:
        """Close a position for the authenticated account.
        :param position: ClosePosition. The position to close.
        :return: DealReference e.g: {'dealReference': 'DIAAAABBBCCC123'}
        """

        url = f"{self.base_url}/gateway/deal/positions/otc"
        headers = self.headers.copy()
        headers["Version"] = "1"
        headers["_method"] = "DELETE"
        json = position.model_dump(exclude_none=True)
        try:
            response = requests.post(url, headers=headers, json=json)
            if response.status_code == 200:
                return DealReference.model_validate(response.json())
            else:
                raise PositionsError(
                    "Close position request failed with status code %s: %s"
                    % (response.status_code, response.text)
                )
        except requests.RequestException as e:
            raise PositionsError("Close position request failed: %s" % e)
