"""Exact provider-compatible endpoint facades for every REST API version."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ig_trading_lib.core import TradingGuard
from ig_trading_lib.transport import AsyncTransport, SyncTransport


class VersionedResource:
    """Raw IG endpoint operations for one explicit API version."""

    def __init__(
        self,
        transport: SyncTransport,
        guard: TradingGuard,
        version: int,
        path: str,
    ) -> None:
        self._transport = transport
        self._guard = guard
        self._version = version
        self._path = path

    def get(self, suffix: str = "", *, params: Mapping[str, Any] | None = None) -> Any:
        """Return the untouched provider payload from an explicit-version GET."""
        return self._transport.request(
            "GET", f"{self._path}{suffix}", version=self._version, params=params
        ).json()

    def create(self, body: Mapping[str, Any], suffix: str = "") -> Any:
        """POST an untouched body after enforcing live-dealing permission."""
        return self._mutate("POST", body, suffix)

    def update(self, body: Mapping[str, Any], suffix: str = "") -> Any:
        """PUT an untouched body after enforcing live-dealing permission."""
        return self._mutate("PUT", body, suffix)

    def delete(self, suffix: str = "", *, params: Mapping[str, Any] | None = None) -> Any:
        """DELETE after enforcing live-dealing permission."""
        self._guard.require_mutation_permission()
        return self._transport.request(
            "DELETE", f"{self._path}{suffix}", version=self._version, params=params
        ).json()

    def _mutate(self, method: str, body: Mapping[str, Any], suffix: str) -> Any:
        self._guard.require_mutation_permission()
        return self._transport.request(
            method, f"{self._path}{suffix}", version=self._version, json=body
        ).json()


class VersionFacade:
    """Namespace of raw endpoint resources for one documented IG API version."""

    def __init__(self, transport: SyncTransport, guard: TradingGuard, version: int) -> None:
        self._transport = transport
        self._guard = guard
        self.version = version
        self.accounts = VersionedResource(transport, guard, version, "/accounts")
        self.activity = VersionedResource(transport, guard, version, "/history/activity")
        self.transactions = VersionedResource(transport, guard, version, "/history/transactions")
        self.confirms = VersionedResource(transport, guard, version, "/confirms")
        self.positions = VersionedResource(transport, guard, version, "/positions")
        self.working_orders = VersionedResource(transport, guard, version, "/working-orders")
        self.repeat_dealing_window = VersionedResource(
            transport, guard, version, "/repeat-dealing-window"
        )
        self.categories = VersionedResource(transport, guard, version, "/categories")
        self.markets = VersionedResource(transport, guard, version, "/markets")
        self.prices = VersionedResource(transport, guard, version, "/prices")
        self.watchlists = VersionedResource(transport, guard, version, "/watchlists")
        self.sentiment = VersionedResource(transport, guard, version, "/client-sentiment")
        self.session = VersionedResource(transport, guard, version, "/session")
        self.costs = VersionedResource(transport, guard, version, "/indicativecostsandcharges")
        self.applications = VersionedResource(transport, guard, version, "/operations/application")

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Mapping[str, Any] | None = None,
    ) -> Any:
        """Call an explicitly-versioned IG path when no resource helper fits."""
        if method.upper() in {"DELETE", "POST", "PUT"}:
            self._guard.require_mutation_permission()
        return self._transport.request(
            method,
            path,
            version=self.version,
            params=params,
            json=json,
        ).json()


class AsyncVersionedResource:
    """Async counterpart to :class:`VersionedResource`."""

    def __init__(
        self,
        transport: AsyncTransport,
        guard: TradingGuard,
        version: int,
        path: str,
    ) -> None:
        self._transport = transport
        self._guard = guard
        self._version = version
        self._path = path

    async def get(self, suffix: str = "", *, params: Mapping[str, Any] | None = None) -> Any:
        """Return the untouched provider payload from an explicit-version GET."""
        response = await self._transport.request(
            "GET", f"{self._path}{suffix}", version=self._version, params=params
        )
        return response.json()

    async def create(self, body: Mapping[str, Any], suffix: str = "") -> Any:
        """POST an untouched body after enforcing live-dealing permission."""
        return await self._mutate("POST", body, suffix)

    async def update(self, body: Mapping[str, Any], suffix: str = "") -> Any:
        """PUT an untouched body after enforcing live-dealing permission."""
        return await self._mutate("PUT", body, suffix)

    async def delete(self, suffix: str = "", *, params: Mapping[str, Any] | None = None) -> Any:
        """DELETE after enforcing live-dealing permission."""
        self._guard.require_mutation_permission()
        response = await self._transport.request(
            "DELETE", f"{self._path}{suffix}", version=self._version, params=params
        )
        return response.json()

    async def _mutate(self, method: str, body: Mapping[str, Any], suffix: str) -> Any:
        self._guard.require_mutation_permission()
        response = await self._transport.request(
            method, f"{self._path}{suffix}", version=self._version, json=body
        )
        return response.json()


class AsyncVersionFacade:
    """Namespace of async raw endpoint resources for one IG API version."""

    def __init__(self, transport: AsyncTransport, guard: TradingGuard, version: int) -> None:
        self._transport = transport
        self._guard = guard
        self.version = version
        self.accounts = AsyncVersionedResource(transport, guard, version, "/accounts")
        self.activity = AsyncVersionedResource(transport, guard, version, "/history/activity")
        self.transactions = AsyncVersionedResource(
            transport, guard, version, "/history/transactions"
        )
        self.confirms = AsyncVersionedResource(transport, guard, version, "/confirms")
        self.positions = AsyncVersionedResource(transport, guard, version, "/positions")
        self.working_orders = AsyncVersionedResource(transport, guard, version, "/working-orders")
        self.repeat_dealing_window = AsyncVersionedResource(
            transport, guard, version, "/repeat-dealing-window"
        )
        self.categories = AsyncVersionedResource(transport, guard, version, "/categories")
        self.markets = AsyncVersionedResource(transport, guard, version, "/markets")
        self.prices = AsyncVersionedResource(transport, guard, version, "/prices")
        self.watchlists = AsyncVersionedResource(transport, guard, version, "/watchlists")
        self.sentiment = AsyncVersionedResource(transport, guard, version, "/client-sentiment")
        self.session = AsyncVersionedResource(transport, guard, version, "/session")
        self.costs = AsyncVersionedResource(transport, guard, version, "/indicativecostsandcharges")
        self.applications = AsyncVersionedResource(
            transport, guard, version, "/operations/application"
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Mapping[str, Any] | None = None,
    ) -> Any:
        """Call an explicitly-versioned IG path when no resource helper fits."""
        if method.upper() in {"DELETE", "POST", "PUT"}:
            self._guard.require_mutation_permission()
        response = await self._transport.request(
            method,
            path,
            version=self.version,
            params=params,
            json=json,
        )
        return response.json()
