"""Typed watchlist operations."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from ig_trading_lib._protocol.executor import AsyncExecutor, SyncExecutor
from ig_trading_lib.models import IGModel, IGRequest
from ig_trading_lib.operations.markets import MarketSummary


class Watchlist(IGModel):
    default_system_watchlist: bool | None = None
    id: str
    name: str | None = None
    editable: bool | None = None
    deleteable: bool | None = None


class WatchlistsResponse(IGModel):
    watchlists: tuple[Watchlist, ...] = ()


class WatchlistMarket(MarketSummary):
    lot_size: Decimal | None = None


class WatchlistResponse(IGModel):
    id: str | None = None
    name: str | None = None
    markets: tuple[WatchlistMarket, ...] = ()


class CreateWatchlistRequest(IGRequest):
    name: str = Field(min_length=1)
    epics: tuple[str, ...] = ()


class CreateWatchlistResponse(IGModel):
    status: str | None = None
    watchlist_id: str | None = None


class UpdateWatchlistRequest(IGRequest):
    name: str | None = None
    epics: tuple[str, ...] | None = None


class WatchlistMutationResponse(IGModel):
    status: str | None = None


class WatchlistsOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def list(self) -> WatchlistsResponse:
        return self._executor.execute("watchlists.list", WatchlistsResponse)

    def create(self, request: CreateWatchlistRequest) -> CreateWatchlistResponse:
        return self._executor.execute(
            "watchlists.create", CreateWatchlistResponse, body=request.to_wire()
        )

    def get(self, watchlist_id: str) -> WatchlistResponse:
        return self._executor.execute(
            "watchlists.get", WatchlistResponse, path={"watchlist_id": watchlist_id}
        )

    def update(
        self, watchlist_id: str, request: UpdateWatchlistRequest
    ) -> WatchlistMutationResponse:
        return self._executor.execute(
            "watchlists.update",
            WatchlistMutationResponse,
            path={"watchlist_id": watchlist_id},
            body=request.to_wire(),
        )

    def delete(self, watchlist_id: str) -> WatchlistMutationResponse:
        return self._executor.execute(
            "watchlists.delete",
            WatchlistMutationResponse,
            path={"watchlist_id": watchlist_id},
        )

    def remove_market(self, watchlist_id: str, epic: str) -> WatchlistMutationResponse:
        return self._executor.execute(
            "watchlists.remove_market",
            WatchlistMutationResponse,
            path={"watchlist_id": watchlist_id, "epic": epic},
        )


class AsyncWatchlistsOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def list(self) -> WatchlistsResponse:
        return await self._executor.execute("watchlists.list", WatchlistsResponse)

    async def create(self, request: CreateWatchlistRequest) -> CreateWatchlistResponse:
        return await self._executor.execute(
            "watchlists.create", CreateWatchlistResponse, body=request.to_wire()
        )

    async def get(self, watchlist_id: str) -> WatchlistResponse:
        return await self._executor.execute(
            "watchlists.get", WatchlistResponse, path={"watchlist_id": watchlist_id}
        )

    async def update(
        self, watchlist_id: str, request: UpdateWatchlistRequest
    ) -> WatchlistMutationResponse:
        return await self._executor.execute(
            "watchlists.update",
            WatchlistMutationResponse,
            path={"watchlist_id": watchlist_id},
            body=request.to_wire(),
        )

    async def delete(self, watchlist_id: str) -> WatchlistMutationResponse:
        return await self._executor.execute(
            "watchlists.delete",
            WatchlistMutationResponse,
            path={"watchlist_id": watchlist_id},
        )

    async def remove_market(self, watchlist_id: str, epic: str) -> WatchlistMutationResponse:
        return await self._executor.execute(
            "watchlists.remove_market",
            WatchlistMutationResponse,
            path={"watchlist_id": watchlist_id, "epic": epic},
        )
