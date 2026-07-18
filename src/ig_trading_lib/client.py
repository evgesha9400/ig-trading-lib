"""Simple synchronous v3 client facade."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

from ig_trading_lib.core import IGConfig, TradingGuard, TradingPermit
from ig_trading_lib.models import IGModel
from ig_trading_lib.services import AccountsClient, MarketsClient, ResourceClient
from ig_trading_lib.transport import SyncTransport


class PositionsClient:
    """Position operations exposed by :class:`IGClient`."""

    def __init__(self, guard: TradingGuard, transport: SyncTransport) -> None:
        self._guard = guard
        self._transport = transport

    def create(self, request: Mapping[str, Any]) -> IGModel:
        """Create an OTC position after enforcing live-dealing permission."""
        self._guard.require_mutation_permission()
        response = self._transport.request("POST", "/positions/otc", version=2, json=request)
        return IGModel.model_validate(response.json())


class IGClient:
    """Synchronous entry point for the production v3 API."""

    def __init__(
        self,
        config: IGConfig,
        *,
        trading_permit: TradingPermit | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.config = config
        self._guard = TradingGuard(config, trading_permit)
        self._transport = SyncTransport(config, http_client=http_client)
        self.positions = PositionsClient(self._guard, self._transport)
        self.markets = MarketsClient(self._transport)
        self.accounts = AccountsClient(self._transport)
        self.activity = ResourceClient(self._transport, "/history/activity", version=3)
        self.transactions = ResourceClient(self._transport, "/history/transactions", version=2)
        self.watchlists = ResourceClient(self._transport, "/watchlists", version=1)
        self.sentiment = ResourceClient(self._transport, "/clientsentiment", version=1)
        self.costs = ResourceClient(self._transport, "/indicativecostsandcharges", version=1)
        self.applications = ResourceClient(self._transport, "/operations/application", version=1)
        self.market_navigation = ResourceClient(self._transport, "/marketnavigation", version=1)
        self.prices = ResourceClient(self._transport, "/prices", version=3)

    def close(self) -> None:
        """Close resources owned by the client."""
        self._transport.close()

    def __enter__(self) -> IGClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
