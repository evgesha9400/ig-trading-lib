"""Simple synchronous v3 client facade."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ig_trading_lib.core import IGConfig, TradingGuard, TradingPermit


class PositionsClient:
    """Position operations exposed by :class:`IGClient`."""

    def __init__(self, guard: TradingGuard) -> None:
        self._guard = guard

    def create(self, request: Mapping[str, Any]) -> None:
        """Validate live-dealing permission before any position request."""
        self._guard.require_mutation_permission()
        raise NotImplementedError("Position transport is not configured yet.")


class IGClient:
    """Synchronous entry point for the production v3 API."""

    def __init__(self, config: IGConfig, *, trading_permit: TradingPermit | None = None) -> None:
        self.config = config
        self._guard = TradingGuard(config, trading_permit)
        self.positions = PositionsClient(self._guard)
