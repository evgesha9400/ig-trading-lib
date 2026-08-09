"""Composition roots for the operation- and workflow-oriented interface."""

from __future__ import annotations

from dataclasses import dataclass

import httpx

from ig_trading_lib.core import IGConfig, TradingGuard, TradingPermit
from ig_trading_lib.operations.markets import AsyncMarketOperations, MarketOperations
from ig_trading_lib.transport import AsyncTransport, SyncTransport
from ig_trading_lib.workflows.discovery import (
    AsyncMarketDiscoveryWorkflow,
    MarketDiscoveryWorkflow,
)


@dataclass(frozen=True, slots=True)
class Operations:
    """Synchronous operation namespaces."""

    markets: MarketOperations


@dataclass(frozen=True, slots=True)
class Workflows:
    """Synchronous workflow namespaces."""

    discovery: MarketDiscoveryWorkflow


@dataclass(frozen=True, slots=True)
class AsyncOperations:
    """Asynchronous operation namespaces."""

    markets: AsyncMarketOperations


@dataclass(frozen=True, slots=True)
class AsyncWorkflows:
    """Asynchronous workflow namespaces."""

    discovery: AsyncMarketDiscoveryWorkflow


class IG:
    """Synchronous composition root exposing operations and workflows."""

    def __init__(
        self,
        config: IGConfig,
        *,
        trading_permit: TradingPermit | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._guard = TradingGuard(config, trading_permit)
        self._transport = SyncTransport(config, http_client=http_client)
        markets = MarketOperations(self._transport)
        self.operations = Operations(markets=markets)
        self.workflows = Workflows(discovery=MarketDiscoveryWorkflow(markets))

    def close(self) -> None:
        """Close resources owned by this root."""
        self._transport.close()

    def __enter__(self) -> IG:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class AsyncIG:
    """Asynchronous composition root exposing operations and workflows."""

    def __init__(
        self,
        config: IGConfig,
        *,
        trading_permit: TradingPermit | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._guard = TradingGuard(config, trading_permit)
        self._transport = AsyncTransport(config, http_client=http_client)
        markets = AsyncMarketOperations(self._transport)
        self.operations = AsyncOperations(markets=markets)
        self.workflows = AsyncWorkflows(discovery=AsyncMarketDiscoveryWorkflow(markets))

    async def close(self) -> None:
        """Close resources owned by this root."""
        await self._transport.close()

    async def __aenter__(self) -> AsyncIG:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()
