"""Stable, provider-aware failures exposed by the v3 API."""

from __future__ import annotations

from typing import Any


class IGError(RuntimeError):
    """Base error containing safe diagnostics for a failed IG request."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        error_code: str | None = None,
        request_id: str | None = None,
        retry_after_seconds: float | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.request_id = request_id
        self.retry_after_seconds = retry_after_seconds
        self.details = details or {}


class AuthenticationError(IGError):
    """Authentication or token-refresh failure."""


class AuthorizationError(IGError):
    """Credential does not grant access to the requested resource."""


class RateLimitError(IGError):
    """IG has rejected a request because a quota was exceeded."""


class ProviderRejectionError(IGError):
    """IG has rejected an otherwise well-formed request."""


class ResourceNotFoundError(IGError):
    """The requested IG resource does not exist or is inaccessible."""


class TransportError(IGError):
    """A network or timeout failure prevented a completed request."""


class AmbiguousExecutionError(IGError):
    """A mutation may have reached IG but its outcome cannot be known safely."""
