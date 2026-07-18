"""Stable, provider-aware failures exposed by the v3 API."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

_SENSITIVE_KEYS = {
    "accesstoken",
    "apikey",
    "authorization",
    "cst",
    "password",
    "refreshtoken",
    "securitytoken",
}


class IGError(RuntimeError):
    """Base error containing safe diagnostics for a failed IG request."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        error_code: str | None = None,
        request_id: str | None = None,
        operation_id: str | None = None,
        retry_after_seconds: float | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.request_id = request_id
        self.operation_id = operation_id
        self.retry_after_seconds = retry_after_seconds
        self.details = _redact_details(details or {})


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


class StreamingSubscriptionError(IGError):
    """IG rejected a Lightstreamer subscription."""


class StreamingDataLossError(IGError):
    """A streaming subscription lost updates or exhausted its local buffer."""


def _redact_details(value: Mapping[str, Any]) -> dict[str, Any]:
    """Remove credential values from provider diagnostics before retaining them."""
    return {key: _redact_value(key, item) for key, item in value.items()}


def _redact_value(key: str, value: Any) -> Any:
    normalized_key = "".join(character for character in key.lower() if character.isalnum())
    if normalized_key in _SENSITIVE_KEYS:
        return "[REDACTED]"
    if isinstance(value, Mapping):
        return _redact_details(value)
    if isinstance(value, list):
        return [_redact_value(key, item) for item in value]
    return value
