import logging

import requests
from pydantic import ValidationError

from .models import (
    OpenPositions,
    OpenPosition,
    CreatePosition,
    ClosePosition,
    UpdatePosition,
    DealReference,
)


logger = logging.getLogger(__name__)


class PositionsError(Exception):
    """Exception raised for errors in the positions process."""


class PositionService:
    def __init__(self, api_key, tokens, base_url):
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
            raise PositionsError(f"Invalid open position response: %s" % e)
        except requests.RequestException as e:
            raise PositionsError(f"Open position request failed: %s" % e)

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
            raise PositionsError(f"Invalid open positions response: %s" % e)
        except requests.RequestException as e:
            raise PositionsError(f"Open positions request failed: %s" % e)

    def create_position(self, create: CreatePosition) -> DealReference:
        """Create a new position for the authenticated account.
        :param create: CreatePosition. The position to create.
        :return: DealReference e.g: {'dealReference': 'DIAAAABBBCCC123'}
        """

        url = f"{self.base_url}/gateway/deal/positions/otc"
        try:
            response = requests.post(
                url, headers=self.headers, json=create.model_dump()
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise PositionsError(
                    "Create position request failed with status code %s: %s"
                    % (response.status_code, response.text)
                )
        except requests.RequestException as e:
            raise PositionsError(f"Create position request failed: %s" % e)

    def close_position(self, close: ClosePosition) -> DealReference:
        """Close a position for the authenticated account.
        :return: DealReference e.g: {'dealReference': 'DIAAAABBBCCC123'}
        """

        url = f"{self.base_url}/gateway/deal/positions/otc"
        try:
            response = requests.post(url, headers=self.headers, json=close.model_dump())
            if response.status_code == 200:
                return response.json()
            else:
                raise PositionsError(
                    "Close position request failed with status code %s: %s"
                    % (response.status_code, response.text)
                )
        except requests.RequestException as e:
            raise PositionsError(f"Close position request failed: %s" % e)

    def update_position(self, deal_id: str, update: UpdatePosition) -> DealReference:
        """Update a position for the authenticated account.
        :param deal_id: str. The deal ID of the position to update.
        :return: DealReference e.g: {'dealReference': 'DIAAAABBBCCC123'}
        """

        url = f"{self.base_url}/gateway/deal/positions/otc/{deal_id}"
        try:
            response = requests.put(url, headers=self.headers, json=update.model_dump())
            if response.status_code == 200:
                return response.json()
            else:
                raise PositionsError(
                    "Update position request failed with status code %s: %s"
                    % (response.status_code, response.text)
                )
        except requests.RequestException as e:
            raise PositionsError(f"Update position request failed: %s" % e)
