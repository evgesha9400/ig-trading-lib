"""High-level REST services with consistent request and pagination behaviour."""

from __future__ import annotations

from ig_trading_lib.models import IGModel, Page
from ig_trading_lib.transport import SyncTransport


class MarketsClient:
    """Market discovery and snapshot operations."""

    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def search(self, search_term: str) -> Page[IGModel]:
        """Return markets matching a human-friendly search term."""
        response = self._transport.request(
            "GET",
            "/markets",
            version=1,
            params={"searchTerm": search_term},
        )
        payload = response.json()
        items = tuple(IGModel.model_validate(item) for item in payload.get("markets", []))
        next_path = payload.get("metadata", {}).get("paging", {}).get("next")
        return Page(items=items, next_path=next_path)
