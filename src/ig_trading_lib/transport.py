"""Resilient, authenticated HTTP transports for IG REST services."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from threading import RLock
from typing import Any
from uuid import uuid4

import httpx

from ig_trading_lib.core import (
    IGConfig,
    OAuthCredentials,
    SessionCredentials,
    StreamingSession,
)
from ig_trading_lib.errors import (
    AmbiguousExecutionError,
    AuthenticationError,
    AuthorizationError,
    IGError,
    ProviderRejectionError,
    RateLimitError,
    ResourceNotFoundError,
    TransportError,
)

logger = logging.getLogger(__name__)
_SAFE_METHODS = frozenset({"GET", "HEAD"})
_RETRY_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


@dataclass(frozen=True, slots=True)
class SessionTokens:
    """Authenticated material retained in memory for one client instance."""

    cst: str | None = field(default=None, repr=False)
    security_token: str | None = field(default=None, repr=False)
    access_token: str | None = field(default=None, repr=False)
    refresh_token: str | None = field(default=None, repr=False)
    expires_at: float | None = None
    account_id: str | None = None
    lightstreamer_endpoint: str | None = None

    @property
    def needs_refresh(self) -> bool:
        return (
            self.refresh_token is not None
            and self.expires_at is not None
            and time.monotonic() >= self.expires_at
        )


class SyncTransport:
    """Authenticated synchronous transport with conservative retry semantics."""

    def __init__(self, config: IGConfig, *, http_client: httpx.Client | None = None) -> None:
        self._config = config
        self._http = http_client or httpx.Client(timeout=config.timeout_seconds)
        self._owns_http_client = http_client is None
        self._tokens: SessionTokens | None = None
        self._token_lock = RLock()

    def close(self) -> None:
        """Close the owned HTTP client."""
        if self._owns_http_client:
            self._http.close()

    def invalidate_session(self) -> None:
        """Discard local authentication after a successful remote logout."""
        self._tokens = None

    def request(
        self,
        method: str,
        path: str,
        *,
        version: int,
        params: Mapping[str, Any] | None = None,
        json: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        """Send an authenticated request without retrying a possible mutation."""
        normalized_method = method.upper()
        operation_id = str(uuid4())
        self._ensure_authenticated()
        attempts = 1 + self._config.max_retries if normalized_method in _SAFE_METHODS else 1
        refresh_attempted = False
        for attempt in range(attempts):
            try:
                response = self._send(
                    normalized_method,
                    path,
                    version=version,
                    params=params,
                    json=json,
                    operation_id=operation_id,
                )
            except httpx.RequestError as error:
                if normalized_method not in _SAFE_METHODS:
                    raise AmbiguousExecutionError(
                        "IG may have accepted the mutation before the network failure.",
                        operation_id=operation_id,
                    ) from error
                if attempt + 1 < attempts:
                    self._wait_for_retry(None, attempt)
                    continue
                raise TransportError(
                    "A network failure prevented IG from answering the request.",
                    operation_id=operation_id,
                ) from error

            if response.status_code < 400:
                self._log_response(response, normalized_method, path, attempt, operation_id)
                return response
            if self._can_refresh_after_unauthorized(response, normalized_method, refresh_attempted):
                self._refresh_oauth_tokens(
                    expected_access_token=_access_token_from_headers(response.request.headers)
                )
                refresh_attempted = True
                continue
            if self._should_retry(response, attempt, attempts):
                self._wait_for_retry(response, attempt)
                continue
            self._raise_for_response(response, operation_id=operation_id)
        raise AssertionError("Retry loop must return or raise.")

    def streaming_session(self) -> StreamingSession:
        """Return the CST/XST session that IG requires for Lightstreamer."""
        self._ensure_authenticated()
        tokens = self._tokens
        if tokens is None:
            raise AuthenticationError("No authenticated IG session is available.")
        if tokens.cst and tokens.security_token:
            return self._build_streaming_session(tokens)

        response = self.request("GET", "/session", version=1, params={"fetchSessionTokens": "true"})
        cst = response.headers.get("CST")
        security_token = response.headers.get("X-SECURITY-TOKEN")
        if not cst or not security_token:
            raise AuthenticationError("IG did not return CST/XST tokens for streaming.")
        payload = _payload(response)
        self._tokens = SessionTokens(
            cst=cst,
            security_token=security_token,
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            expires_at=tokens.expires_at,
            account_id=payload.get("accountId") or tokens.account_id,
            lightstreamer_endpoint=payload.get("lightstreamerEndpoint")
            or tokens.lightstreamer_endpoint,
        )
        return self._build_streaming_session(self._tokens)

    def refresh_streaming_session(self) -> StreamingSession:
        """Create a fresh IG session before a terminal streaming reconnection."""
        with self._token_lock:
            self._tokens = None
            self._create_session()
        return self.streaming_session()

    def _ensure_authenticated(self) -> None:
        tokens = self._tokens
        if tokens is not None and not tokens.needs_refresh:
            return
        with self._token_lock:
            tokens = self._tokens
            if tokens is not None and not tokens.needs_refresh:
                return
            if isinstance(self._config.credentials, OAuthCredentials) and tokens is not None:
                self._refresh_oauth_tokens()
                return
            self._create_session()
            if self._tokens is not None and self._tokens.needs_refresh:
                self._refresh_oauth_tokens()

    def _create_session(self) -> None:
        credentials = self._config.credentials
        try:
            response = self._http.post(
                self._url("/session"),
                json={"identifier": credentials.identifier, "password": credentials.password},
                headers=self._anonymous_headers(_authentication_version(credentials)),
            )
        except httpx.RequestError as error:
            raise TransportError(
                "A network failure prevented IG session authentication."
            ) from error
        if response.status_code >= 400:
            self._raise_for_response(response, error_type=AuthenticationError)
        self._tokens = self._tokens_from_session_response(response)

    def _refresh_oauth_tokens(self, *, expected_access_token: str | None = None) -> None:
        tokens = self._tokens
        if tokens is None or not tokens.refresh_token:
            raise AuthenticationError("IG OAuth refresh requires a refresh token.")
        if expected_access_token is not None and tokens.access_token != expected_access_token:
            return
        try:
            response = self._http.post(
                self._url("/session/refresh-token"),
                json={"refresh_token": tokens.refresh_token},
                headers=self._anonymous_headers(version=1),
            )
        except httpx.RequestError as error:
            raise AuthenticationError("A network failure prevented OAuth token refresh.") from error
        if response.status_code >= 400:
            self._raise_for_response(response, AuthenticationError)
        self._tokens = self._tokens_from_oauth_payload(_payload(response), tokens)

    def _tokens_from_session_response(self, response: httpx.Response) -> SessionTokens:
        credentials = self._config.credentials
        payload = _payload(response)
        if isinstance(credentials, SessionCredentials):
            cst = response.headers.get("CST")
            security_token = response.headers.get("X-SECURITY-TOKEN")
            if not cst or not security_token:
                raise AuthenticationError(
                    "IG session response did not include both security tokens."
                )
            return SessionTokens(
                cst=cst,
                security_token=security_token,
                account_id=payload.get("currentAccountId") or payload.get("accountId"),
                lightstreamer_endpoint=payload.get("lightstreamerEndpoint"),
            )
        if isinstance(credentials, OAuthCredentials):
            oauth_token = payload.get("oauthToken")
            if not isinstance(oauth_token, Mapping):
                raise AuthenticationError("IG OAuth response did not include token details.")
            return self._tokens_from_oauth_payload(
                oauth_token,
                SessionTokens(
                    account_id=payload.get("currentAccountId") or payload.get("accountId"),
                    lightstreamer_endpoint=payload.get("lightstreamerEndpoint"),
                ),
            )
        raise AuthenticationError("Unsupported credentials type.")

    @staticmethod
    def _tokens_from_oauth_payload(
        payload: Mapping[str, Any], previous: SessionTokens
    ) -> SessionTokens:
        access_token = payload.get("access_token")
        refresh_token = payload.get("refresh_token")
        if not isinstance(access_token, str) or not isinstance(refresh_token, str):
            raise AuthenticationError(
                "IG OAuth response did not include both access and refresh tokens."
            )
        expires_in = payload.get("expires_in")
        if expires_in is None:
            raise AuthenticationError("IG OAuth response did not include a token expiry.")
        try:
            expires_after = max(float(expires_in) - 30.0, 0.0)
        except (TypeError, ValueError):
            raise AuthenticationError(
                "IG OAuth response contained an invalid token expiry."
            ) from None
        return SessionTokens(
            cst=previous.cst,
            security_token=previous.security_token,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=time.monotonic() + expires_after,
            account_id=previous.account_id,
            lightstreamer_endpoint=previous.lightstreamer_endpoint,
        )

    def _build_streaming_session(self, tokens: SessionTokens) -> StreamingSession:
        endpoint = tokens.lightstreamer_endpoint
        account_id = self._config.account_id or tokens.account_id
        if not endpoint or not account_id or not tokens.cst or not tokens.security_token:
            raise AuthenticationError(
                "IG session does not contain the values required for streaming."
            )
        return StreamingSession(endpoint, account_id, tokens.cst, tokens.security_token)

    def _send(
        self,
        method: str,
        path: str,
        *,
        version: int,
        params: Mapping[str, Any] | None,
        json: Mapping[str, Any] | None,
        operation_id: str,
    ) -> httpx.Response:
        return self._http.request(
            method,
            self._url(path),
            params=params,
            json=json,
            headers=self._headers(version, operation_id),
        )

    def _headers(self, version: int, operation_id: str) -> dict[str, str]:
        headers = self._anonymous_headers(version)
        headers["X-CORRELATION-ID"] = operation_id
        tokens = self._tokens
        if tokens is None:
            return headers
        if tokens.access_token:
            headers["Authorization"] = f"Bearer {tokens.access_token}"
            if self._config.account_id:
                headers["IG-ACCOUNT-ID"] = self._config.account_id
            return headers
        headers["CST"] = tokens.cst or ""
        headers["X-SECURITY-TOKEN"] = tokens.security_token or ""
        return headers

    def _anonymous_headers(self, version: int) -> dict[str, str]:
        return {
            "Accept": "application/json; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8",
            "Version": str(version),
            "X-IG-API-KEY": self._config.credentials.api_key,
            "X-CORRELATION-ID": str(uuid4()),
        }

    def _url(self, path: str) -> str:
        return f"{self._config.base_url}{path if path.startswith('/') else f'/{path}'}"

    def _can_refresh_after_unauthorized(
        self, response: httpx.Response, method: str, refresh_attempted: bool
    ) -> bool:
        return (
            response.status_code == 401
            and method in _SAFE_METHODS
            and not refresh_attempted
            and isinstance(self._config.credentials, OAuthCredentials)
        )

    @staticmethod
    def _should_retry(response: httpx.Response, attempt: int, attempts: int) -> bool:
        return attempt + 1 < attempts and response.status_code in _RETRY_STATUS_CODES

    @staticmethod
    def _wait_for_retry(response: httpx.Response | None, attempt: int) -> None:
        delay = _retry_delay(response, attempt)
        time.sleep(delay)

    def _raise_for_response(
        self,
        response: httpx.Response,
        error_type: type[IGError] | None = None,
        *,
        operation_id: str | None = None,
    ) -> None:
        _raise_for_response(response, error_type=error_type, operation_id=operation_id)

    @staticmethod
    def _log_response(
        response: httpx.Response, method: str, path: str, attempt: int, operation_id: str
    ) -> None:
        _log_response(response, method, path, attempt, operation_id)


class AsyncTransport:
    """Authenticated asynchronous transport matching :class:`SyncTransport`."""

    def __init__(self, config: IGConfig, *, http_client: httpx.AsyncClient | None = None) -> None:
        self._config = config
        self._http = http_client or httpx.AsyncClient(timeout=config.timeout_seconds)
        self._owns_http_client = http_client is None
        self._tokens: SessionTokens | None = None
        self._token_lock = asyncio.Lock()

    async def close(self) -> None:
        """Close the owned asynchronous HTTP client."""
        if self._owns_http_client:
            await self._http.aclose()

    def invalidate_session(self) -> None:
        """Discard local authentication after a successful remote logout."""
        self._tokens = None

    async def request(
        self,
        method: str,
        path: str,
        *,
        version: int,
        params: Mapping[str, Any] | None = None,
        json: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        """Send an authenticated request without retrying a possible mutation."""
        normalized_method = method.upper()
        operation_id = str(uuid4())
        await self._ensure_authenticated()
        attempts = 1 + self._config.max_retries if normalized_method in _SAFE_METHODS else 1
        refresh_attempted = False
        for attempt in range(attempts):
            try:
                headers = self._headers(version, operation_id)
                response = await self._http.request(
                    normalized_method,
                    self._url(path),
                    params=params,
                    json=json,
                    headers=headers,
                )
            except httpx.RequestError as error:
                if normalized_method not in _SAFE_METHODS:
                    raise AmbiguousExecutionError(
                        "IG may have accepted the mutation before the network failure.",
                        operation_id=operation_id,
                    ) from error
                if attempt + 1 < attempts:
                    await asyncio.sleep(_retry_delay(None, attempt))
                    continue
                raise TransportError(
                    "A network failure prevented IG from answering the request.",
                    operation_id=operation_id,
                ) from error
            if response.status_code < 400:
                _log_response(response, normalized_method, path, attempt, operation_id)
                return response
            if self._can_refresh_after_unauthorized(response, normalized_method, refresh_attempted):
                await self._refresh_oauth_tokens(
                    expected_access_token=_access_token_from_headers(headers)
                )
                refresh_attempted = True
                continue
            if self._should_retry(response, attempt, attempts):
                await asyncio.sleep(_retry_delay(response, attempt))
                continue
            _raise_for_response(response, operation_id=operation_id)
        raise AssertionError("Retry loop must return or raise.")

    async def streaming_session(self) -> StreamingSession:
        """Return the CST/XST session that IG requires for Lightstreamer."""
        await self._ensure_authenticated()
        tokens = self._tokens
        if tokens is None:
            raise AuthenticationError("No authenticated IG session is available.")
        if tokens.cst and tokens.security_token:
            return _build_streaming_session(self._config, tokens)
        response = await self.request(
            "GET", "/session", version=1, params={"fetchSessionTokens": "true"}
        )
        cst = response.headers.get("CST")
        security_token = response.headers.get("X-SECURITY-TOKEN")
        if not cst or not security_token:
            raise AuthenticationError("IG did not return CST/XST tokens for streaming.")
        payload = _payload(response)
        self._tokens = SessionTokens(
            cst=cst,
            security_token=security_token,
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            expires_at=tokens.expires_at,
            account_id=payload.get("accountId") or tokens.account_id,
            lightstreamer_endpoint=payload.get("lightstreamerEndpoint")
            or tokens.lightstreamer_endpoint,
        )
        return _build_streaming_session(self._config, self._tokens)

    async def refresh_streaming_session(self) -> StreamingSession:
        """Create a fresh IG session before a terminal streaming reconnection."""
        async with self._token_lock:
            self._tokens = None
            await self._create_session()
        return await self.streaming_session()

    async def _ensure_authenticated(self) -> None:
        tokens = self._tokens
        if tokens is not None and not tokens.needs_refresh:
            return
        async with self._token_lock:
            tokens = self._tokens
            if tokens is not None and not tokens.needs_refresh:
                return
            if isinstance(self._config.credentials, OAuthCredentials) and tokens is not None:
                await self._refresh_oauth_tokens_locked()
                return
            await self._create_session()
            if self._tokens is not None and self._tokens.needs_refresh:
                await self._refresh_oauth_tokens_locked()

    async def _create_session(self) -> None:
        credentials = self._config.credentials
        try:
            response = await self._http.post(
                self._url("/session"),
                json={"identifier": credentials.identifier, "password": credentials.password},
                headers=self._anonymous_headers(_authentication_version(credentials)),
            )
        except httpx.RequestError as error:
            raise TransportError(
                "A network failure prevented IG session authentication."
            ) from error
        if response.status_code >= 400:
            _raise_for_response(response, error_type=AuthenticationError)
        self._tokens = _tokens_from_session_response(self._config, response)

    async def _refresh_oauth_tokens(self, *, expected_access_token: str | None = None) -> None:
        async with self._token_lock:
            tokens = self._tokens
            if (
                tokens is not None
                and expected_access_token is not None
                and tokens.access_token != expected_access_token
            ):
                return
            if tokens is not None and expected_access_token is None and not tokens.needs_refresh:
                return
            await self._refresh_oauth_tokens_locked()

    async def _refresh_oauth_tokens_locked(self) -> None:
        tokens = self._tokens
        if tokens is None or not tokens.refresh_token:
            raise AuthenticationError("IG OAuth refresh requires a refresh token.")
        try:
            response = await self._http.post(
                self._url("/session/refresh-token"),
                json={"refresh_token": tokens.refresh_token},
                headers=self._anonymous_headers(version=1),
            )
        except httpx.RequestError as error:
            raise AuthenticationError("A network failure prevented OAuth token refresh.") from error
        if response.status_code >= 400:
            _raise_for_response(response, AuthenticationError)
        self._tokens = _tokens_from_oauth_payload(_payload(response), tokens)

    def _headers(self, version: int, operation_id: str) -> dict[str, str]:
        return _headers(self._config, self._tokens, version, operation_id)

    def _anonymous_headers(self, version: int) -> dict[str, str]:
        return _anonymous_headers(self._config, version)

    def _url(self, path: str) -> str:
        return _url(self._config, path)

    def _can_refresh_after_unauthorized(
        self, response: httpx.Response, method: str, refresh_attempted: bool
    ) -> bool:
        return (
            response.status_code == 401
            and method in _SAFE_METHODS
            and not refresh_attempted
            and isinstance(self._config.credentials, OAuthCredentials)
        )

    @staticmethod
    def _should_retry(response: httpx.Response, attempt: int, attempts: int) -> bool:
        return attempt + 1 < attempts and response.status_code in _RETRY_STATUS_CODES


def _tokens_from_session_response(config: IGConfig, response: httpx.Response) -> SessionTokens:
    payload = _payload(response)
    credentials = config.credentials
    if isinstance(credentials, SessionCredentials):
        cst = response.headers.get("CST")
        security_token = response.headers.get("X-SECURITY-TOKEN")
        if not cst or not security_token:
            raise AuthenticationError("IG session response did not include both security tokens.")
        return SessionTokens(
            cst=cst,
            security_token=security_token,
            account_id=payload.get("currentAccountId") or payload.get("accountId"),
            lightstreamer_endpoint=payload.get("lightstreamerEndpoint"),
        )
    if isinstance(credentials, OAuthCredentials):
        oauth_token = payload.get("oauthToken")
        if not isinstance(oauth_token, Mapping):
            raise AuthenticationError("IG OAuth response did not include token details.")
        return _tokens_from_oauth_payload(
            oauth_token,
            SessionTokens(
                account_id=payload.get("currentAccountId") or payload.get("accountId"),
                lightstreamer_endpoint=payload.get("lightstreamerEndpoint"),
            ),
        )
    raise AuthenticationError("Unsupported credentials type.")


def _tokens_from_oauth_payload(
    payload: Mapping[str, Any], previous: SessionTokens
) -> SessionTokens:
    access_token = payload.get("access_token")
    refresh_token = payload.get("refresh_token")
    if not isinstance(access_token, str) or not isinstance(refresh_token, str):
        raise AuthenticationError(
            "IG OAuth response did not include both access and refresh tokens."
        )
    expires_in = payload.get("expires_in")
    if expires_in is None:
        raise AuthenticationError("IG OAuth response did not include a token expiry.")
    try:
        expires_after = max(float(expires_in) - 30.0, 0.0)
    except (TypeError, ValueError):
        raise AuthenticationError("IG OAuth response contained an invalid token expiry.") from None
    return SessionTokens(
        cst=previous.cst,
        security_token=previous.security_token,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=time.monotonic() + expires_after,
        account_id=previous.account_id,
        lightstreamer_endpoint=previous.lightstreamer_endpoint,
    )


def _build_streaming_session(config: IGConfig, tokens: SessionTokens) -> StreamingSession:
    endpoint = tokens.lightstreamer_endpoint
    account_id = config.account_id or tokens.account_id
    if not endpoint or not account_id or not tokens.cst or not tokens.security_token:
        raise AuthenticationError("IG session does not contain the values required for streaming.")
    return StreamingSession(endpoint, account_id, tokens.cst, tokens.security_token)


def _headers(
    config: IGConfig, tokens: SessionTokens | None, version: int, operation_id: str
) -> dict[str, str]:
    headers = _anonymous_headers(config, version)
    headers["X-CORRELATION-ID"] = operation_id
    if tokens is None:
        return headers
    if tokens.access_token:
        headers["Authorization"] = f"Bearer {tokens.access_token}"
        if config.account_id:
            headers["IG-ACCOUNT-ID"] = config.account_id
        return headers
    headers["CST"] = tokens.cst or ""
    headers["X-SECURITY-TOKEN"] = tokens.security_token or ""
    return headers


def _anonymous_headers(config: IGConfig, version: int) -> dict[str, str]:
    return {
        "Accept": "application/json; charset=utf-8",
        "Content-Type": "application/json; charset=utf-8",
        "Version": str(version),
        "X-IG-API-KEY": config.credentials.api_key,
        "X-CORRELATION-ID": str(uuid4()),
    }


def _authentication_version(credentials: SessionCredentials | OAuthCredentials) -> int:
    return 3 if isinstance(credentials, OAuthCredentials) else 2


def _url(config: IGConfig, path: str) -> str:
    return f"{config.base_url}{path if path.startswith('/') else f'/{path}'}"


def _access_token_from_headers(headers: Mapping[str, str]) -> str | None:
    authorization = headers.get("Authorization")
    if authorization is None:
        return None
    return authorization.removeprefix("Bearer ")


def _retry_delay(response: httpx.Response | None, attempt: int) -> float:
    retry_after = _retry_after(response) if response is not None else None
    return retry_after if retry_after is not None else min(0.1 * 2**attempt, 2.0)


def _retry_after(response: httpx.Response) -> float | None:
    value = response.headers.get("Retry-After")
    try:
        return max(float(value), 0.0) if value is not None else None
    except ValueError:
        return None


def _raise_for_response(
    response: httpx.Response,
    error_type: type[IGError] | None = None,
    *,
    operation_id: str | None = None,
) -> None:
    payload = _payload(response)
    common = {
        "status_code": response.status_code,
        "error_code": payload.get("errorCode"),
        "request_id": response.headers.get("X-REQUEST-ID"),
        "operation_id": operation_id,
        "retry_after_seconds": _retry_after(response),
        "details": payload,
    }
    if error_type is not None:
        raise error_type("IG authentication request failed.", **common)
    if response.status_code == 401:
        raise AuthenticationError("IG rejected the session credentials.", **common)
    if response.status_code == 403:
        raise AuthorizationError("IG denied access to the resource.", **common)
    if response.status_code == 404:
        raise ResourceNotFoundError("IG resource was not found.", **common)
    if response.status_code == 429:
        raise RateLimitError("IG rate limit exceeded.", **common)
    raise ProviderRejectionError("IG rejected the request.", **common)


def _payload(response: httpx.Response) -> dict[str, Any]:
    try:
        payload = response.json()
    except ValueError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _log_response(
    response: httpx.Response, method: str, path: str, attempt: int, operation_id: str
) -> None:
    logger.info(
        "ig.http.response",
        extra={
            "ig_event": "http_response",
            "ig_method": method,
            "ig_path": path,
            "ig_status_code": response.status_code,
            "ig_request_id": response.headers.get("X-REQUEST-ID"),
            "ig_operation_id": operation_id,
            "ig_retry_count": attempt,
        },
    )
