"""Asynchronous REST services mirroring the synchronous v3 facade."""

from __future__ import annotations

from collections.abc import AsyncIterator, Mapping
from typing import Any

from ig_trading_lib.core import TradingGuard
from ig_trading_lib.models import IGModel, Page
from ig_trading_lib.transport import AsyncTransport


class AsyncResourceClient:
    """Asynchronous versioned REST facade with consistent page handling."""

    def __init__(
        self,
        transport: AsyncTransport,
        path: str,
        version: int,
        guard: TradingGuard | None = None,
    ) -> None:
        self._transport = transport
        self._path = path
        self._version = version
        self._guard = guard

    async def get(self, suffix: str = "", *, params: Mapping[str, Any] | None = None) -> IGModel:
        """Retrieve one resource or provider response object."""
        response = await self._transport.request(
            "GET", f"{self._path}{suffix}", version=self._version, params=params
        )
        return IGModel.model_validate(response.json())

    async def list(
        self,
        *,
        params: Mapping[str, Any] | None = None,
        item_key: str | None = None,
    ) -> Page[IGModel]:
        """Retrieve one typed page, preserving IG's continuation path."""
        response = await self._transport.request(
            "GET", self._path, version=self._version, params=params
        )
        return self._to_page(response.json(), item_key)

    async def iter_pages(
        self,
        *,
        params: Mapping[str, Any] | None = None,
        item_key: str | None = None,
    ) -> AsyncIterator[IGModel]:
        """Yield every item from IG's linked pages lazily."""
        page = await self.list(params=params, item_key=item_key)
        while True:
            for item in page.items:
                yield item
            if not page.next_path:
                return
            response = await self._transport.request("GET", page.next_path, version=self._version)
            page = self._to_page(response.json(), item_key)

    async def create(self, body: Mapping[str, Any], suffix: str = "") -> IGModel:
        """Create a provider resource after enforcing live-dealing permission."""
        return await self._mutation("POST", body, suffix)

    async def update(self, body: Mapping[str, Any], suffix: str = "") -> IGModel:
        """Update a provider resource after enforcing live-dealing permission."""
        return await self._mutation("PUT", body, suffix)

    async def delete(self, suffix: str = "") -> IGModel:
        """Delete a provider resource after enforcing live-dealing permission."""
        return await self._mutation("DELETE", None, suffix)

    async def _mutation(self, method: str, body: Mapping[str, Any] | None, suffix: str) -> IGModel:
        if self._guard is not None:
            self._guard.require_mutation_permission()
        response = await self._transport.request(
            method, f"{self._path}{suffix}", version=self._version, json=body
        )
        return IGModel.model_validate(response.json())

    @staticmethod
    def _to_page(payload: Any, item_key: str | None) -> Page[IGModel]:
        if isinstance(payload, list):
            return Page(items=tuple(IGModel.model_validate(item) for item in payload))
        if not isinstance(payload, dict):
            return Page(items=())
        items = payload.get(item_key, []) if item_key else payload.get("items", [])
        if not isinstance(items, list):
            items = []
        next_path = payload.get("metadata", {}).get("paging", {}).get("next")
        return Page(
            items=tuple(IGModel.model_validate(item) for item in items),
            next_path=next_path,
        )


class AsyncAccountsClient(AsyncResourceClient):
    """Asynchronous account list and preference operations."""

    def __init__(self, transport: AsyncTransport, guard: TradingGuard) -> None:
        super().__init__(transport, "/accounts", version=1, guard=guard)

    async def list(self) -> Page[IGModel]:
        """List accounts available to the authenticated client."""
        return await super().list(item_key="accounts")

    async def preferences(self) -> IGModel:
        """Return active account preferences."""
        return await self.get("/preferences")

    async def update_preferences(self, body: Mapping[str, Any]) -> IGModel:
        """Update active account preferences."""
        return await self.update(body, "/preferences")


class AsyncMarketsClient(AsyncResourceClient):
    """Asynchronous market discovery, snapshots, and versioned data."""

    def __init__(self, transport: AsyncTransport) -> None:
        super().__init__(transport, "/markets", version=4)

    async def search(self, search_term: str) -> Page[IGModel]:
        """Return markets matching a human-friendly search term."""
        response = await self._transport.request(
            "GET", "/markets", version=1, params={"searchTerm": search_term}
        )
        return self._to_page(response.json(), "markets")
