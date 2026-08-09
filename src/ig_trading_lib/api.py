"""Composition roots for the operation- and workflow-oriented interface."""

from __future__ import annotations

from dataclasses import dataclass

import httpx

from ig_trading_lib._protocol.executor import AsyncExecutor, SyncExecutor
from ig_trading_lib.core import IGConfig, TradingGuard, TradingPermit
from ig_trading_lib.operations.accounts import (
    AccountsOperations,
    ActivityOperations,
    AsyncAccountsOperations,
    AsyncActivityOperations,
    AsyncTransactionsOperations,
    TransactionsOperations,
)
from ig_trading_lib.operations.applications import (
    ApplicationsOperations,
    AsyncApplicationsOperations,
)
from ig_trading_lib.operations.costs import (
    AsyncIndicativeCostsOperations,
    IndicativeCostsOperations,
)
from ig_trading_lib.operations.dealing import (
    AsyncConfirmationsOperations,
    AsyncPositionsOperations,
    AsyncRepeatDealingWindowOperations,
    AsyncWorkingOrdersOperations,
    ConfirmationsOperations,
    PositionsOperations,
    RepeatDealingWindowOperations,
    WorkingOrdersOperations,
)
from ig_trading_lib.operations.markets import (
    AsyncCategoriesOperations,
    AsyncMarketOperations,
    AsyncPricesOperations,
    CategoriesOperations,
    MarketOperations,
    PricesOperations,
)
from ig_trading_lib.operations.sentiment import (
    AsyncClientSentimentOperations,
    ClientSentimentOperations,
)
from ig_trading_lib.operations.session import AsyncSessionOperations, SessionOperations
from ig_trading_lib.operations.streaming import AsyncStreamingOperations, StreamingOperations
from ig_trading_lib.operations.watchlists import AsyncWatchlistsOperations, WatchlistsOperations
from ig_trading_lib.streaming import AsyncStreamingClient, StreamingClient
from ig_trading_lib.transport import AsyncTransport, SyncTransport
from ig_trading_lib.workflows.dealing import (
    AsyncPositionWorkflow,
    AsyncWorkingOrderWorkflow,
    PositionWorkflow,
    WorkingOrderWorkflow,
)
from ig_trading_lib.workflows.discovery import (
    AsyncMarketDiscoveryWorkflow,
    MarketDiscoveryWorkflow,
)
from ig_trading_lib.workflows.portfolio import AsyncPortfolioWorkflow, PortfolioWorkflow


@dataclass(frozen=True, slots=True)
class Operations:
    """Synchronous namespaces that map directly to IG operations."""

    accounts: AccountsOperations
    activity: ActivityOperations
    applications: ApplicationsOperations
    categories: CategoriesOperations
    client_sentiment: ClientSentimentOperations
    confirmations: ConfirmationsOperations
    indicative_costs: IndicativeCostsOperations
    markets: MarketOperations
    positions: PositionsOperations
    prices: PricesOperations
    repeat_dealing_window: RepeatDealingWindowOperations
    session: SessionOperations
    streaming: StreamingOperations
    transactions: TransactionsOperations
    watchlists: WatchlistsOperations
    working_orders: WorkingOrdersOperations


@dataclass(frozen=True, slots=True)
class Workflows:
    """Synchronous multi-operation journeys."""

    discovery: MarketDiscoveryWorkflow
    portfolio: PortfolioWorkflow
    positions: PositionWorkflow
    working_orders: WorkingOrderWorkflow


@dataclass(frozen=True, slots=True)
class AsyncOperations:
    """Asynchronous namespaces matching :class:`Operations`."""

    accounts: AsyncAccountsOperations
    activity: AsyncActivityOperations
    applications: AsyncApplicationsOperations
    categories: AsyncCategoriesOperations
    client_sentiment: AsyncClientSentimentOperations
    confirmations: AsyncConfirmationsOperations
    indicative_costs: AsyncIndicativeCostsOperations
    markets: AsyncMarketOperations
    positions: AsyncPositionsOperations
    prices: AsyncPricesOperations
    repeat_dealing_window: AsyncRepeatDealingWindowOperations
    session: AsyncSessionOperations
    streaming: AsyncStreamingOperations
    transactions: AsyncTransactionsOperations
    watchlists: AsyncWatchlistsOperations
    working_orders: AsyncWorkingOrdersOperations


@dataclass(frozen=True, slots=True)
class AsyncWorkflows:
    """Asynchronous multi-operation journeys."""

    discovery: AsyncMarketDiscoveryWorkflow
    portfolio: AsyncPortfolioWorkflow
    positions: AsyncPositionWorkflow
    working_orders: AsyncWorkingOrderWorkflow


class IG:
    """Synchronous root exposing exactly ``operations`` and ``workflows``."""

    def __init__(
        self,
        config: IGConfig,
        *,
        trading_permit: TradingPermit | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        transport = SyncTransport(config, http_client=http_client)
        executor = SyncExecutor(transport, TradingGuard(config, trading_permit))
        streaming = StreamingOperations(
            StreamingClient(
                session_provider=transport.streaming_session,
                refresh_session_provider=transport.refresh_streaming_session,
            )
        )
        self._transport = transport
        self.operations = _sync_operations(executor, streaming)
        self.workflows = _sync_workflows(self.operations)

    def close(self) -> None:
        self.operations.streaming.close()
        self._transport.close()

    def __enter__(self) -> IG:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class AsyncIG:
    """Asynchronous composition root for operation and workflow namespaces."""

    def __init__(
        self,
        config: IGConfig,
        *,
        trading_permit: TradingPermit | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        transport = AsyncTransport(config, http_client=http_client)
        executor = AsyncExecutor(transport, TradingGuard(config, trading_permit))
        streaming = AsyncStreamingOperations(
            AsyncStreamingClient(
                session_provider=transport.streaming_session,
                refresh_session_provider=transport.refresh_streaming_session,
            )
        )
        self._transport = transport
        self.operations = _async_operations(executor, streaming)
        self.workflows = _async_workflows(self.operations)

    async def close(self) -> None:
        await self.operations.streaming.close()
        await self._transport.close()

    async def __aenter__(self) -> AsyncIG:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()


def _sync_operations(executor: SyncExecutor, streaming: StreamingOperations) -> Operations:
    return Operations(
        accounts=AccountsOperations(executor),
        activity=ActivityOperations(executor),
        applications=ApplicationsOperations(executor),
        categories=CategoriesOperations(executor),
        client_sentiment=ClientSentimentOperations(executor),
        confirmations=ConfirmationsOperations(executor),
        indicative_costs=IndicativeCostsOperations(executor),
        markets=MarketOperations(executor),
        positions=PositionsOperations(executor),
        prices=PricesOperations(executor),
        repeat_dealing_window=RepeatDealingWindowOperations(executor),
        session=SessionOperations(executor),
        streaming=streaming,
        transactions=TransactionsOperations(executor),
        watchlists=WatchlistsOperations(executor),
        working_orders=WorkingOrdersOperations(executor),
    )


def _async_operations(
    executor: AsyncExecutor, streaming: AsyncStreamingOperations
) -> AsyncOperations:
    return AsyncOperations(
        accounts=AsyncAccountsOperations(executor),
        activity=AsyncActivityOperations(executor),
        applications=AsyncApplicationsOperations(executor),
        categories=AsyncCategoriesOperations(executor),
        client_sentiment=AsyncClientSentimentOperations(executor),
        confirmations=AsyncConfirmationsOperations(executor),
        indicative_costs=AsyncIndicativeCostsOperations(executor),
        markets=AsyncMarketOperations(executor),
        positions=AsyncPositionsOperations(executor),
        prices=AsyncPricesOperations(executor),
        repeat_dealing_window=AsyncRepeatDealingWindowOperations(executor),
        session=AsyncSessionOperations(executor),
        streaming=streaming,
        transactions=AsyncTransactionsOperations(executor),
        watchlists=AsyncWatchlistsOperations(executor),
        working_orders=AsyncWorkingOrdersOperations(executor),
    )


def _sync_workflows(operations: Operations) -> Workflows:
    return Workflows(
        discovery=MarketDiscoveryWorkflow(operations.markets),
        portfolio=PortfolioWorkflow(
            operations.accounts, operations.positions, operations.working_orders
        ),
        positions=PositionWorkflow(operations.positions, operations.confirmations),
        working_orders=WorkingOrderWorkflow(operations.working_orders, operations.confirmations),
    )


def _async_workflows(operations: AsyncOperations) -> AsyncWorkflows:
    return AsyncWorkflows(
        discovery=AsyncMarketDiscoveryWorkflow(operations.markets),
        portfolio=AsyncPortfolioWorkflow(
            operations.accounts, operations.positions, operations.working_orders
        ),
        positions=AsyncPositionWorkflow(operations.positions, operations.confirmations),
        working_orders=AsyncWorkingOrderWorkflow(
            operations.working_orders, operations.confirmations
        ),
    )
