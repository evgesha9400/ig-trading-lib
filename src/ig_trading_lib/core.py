"""Configuration and safety primitives for the public v3 API."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Environment(StrEnum):
    """IG environments supported by the library."""

    DEMO = "demo"
    LIVE = "live"


@dataclass(frozen=True, slots=True)
class SessionCredentials:
    """Credentials for IG's legacy v1/v2 session authentication."""

    api_key: str
    identifier: str
    password: str
    version: int = 2


@dataclass(frozen=True, slots=True)
class OAuthCredentials:
    """Credentials for IG's OAuth v3 session authentication."""

    api_key: str
    identifier: str
    password: str
    version: int = 3


Credentials = SessionCredentials | OAuthCredentials


@dataclass(frozen=True, slots=True)
class TradingPermit:
    """An explicit acknowledgement that permits live account mutations."""

    acknowledged: bool = True


@dataclass(frozen=True, slots=True)
class IGConfig:
    """Immutable configuration for one IG client instance."""

    environment: Environment
    credentials: Credentials
    timeout_seconds: float = 10.0
    max_retries: int = 2
    account_id: str | None = None

    @property
    def base_url(self) -> str:
        if self.environment is Environment.DEMO:
            return "https://demo-api.ig.com/gateway/deal"
        return "https://api.ig.com/gateway/deal"


class LiveTradingPermissionError(PermissionError):
    """Raised when a live mutation has not been explicitly permitted."""


class TradingGuard:
    """Enforces the minimal non-bypassable live-dealing boundary."""

    def __init__(self, config: IGConfig, permit: TradingPermit | None) -> None:
        self._config = config
        self._permit = permit

    def require_mutation_permission(self) -> None:
        if self._config.environment is Environment.LIVE and not (
            self._permit and self._permit.acknowledged
        ):
            raise LiveTradingPermissionError("Live trading requires an explicit TradingPermit.")
