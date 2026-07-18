"""Resilient HTTP transport shared by all synchronous REST services."""

from __future__ import annotations

import logging
import time
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import httpx

from ig_trading_lib.core import IGConfig, OAuthCredentials, SessionCredentials
from ig_trading_lib.errors import (
    AuthenticationError,
    AuthorizationError,
    IGError,
    ProviderRejectionError,
    RateLimitError,
    ResourceNotFoundError,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class SessionTokens:
    """Authenticated tokens held only for the lifetime of one client instance."""

    cst: str | None = None
    security_token: str | None = None
    access_token: str | None = None


class SyncTransport:
    """Authenticated transport with bounded retries for safe requests only."""

    def __init__(self, config: IGConfig, *, http_client: httpx.Client | None = None) -> None:
        self._config = config
        self._http = http_client or httpx.Client(timeout=config.timeout_seconds)
        self._owns_http_client = http_client is None
        self._tokens: SessionTokens | None = None

    def close(self) -> None:
        if self._owns_http_client:
            self._http.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        version: int,
        params: Mapping[str, Any] | None = None,
        json: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        """Send one authenticated request and retry only idempotent operations."""
        self._ensure_authenticated()
        attempts = 1 + self._config.max_retries if method.upper() in {"GET", "HEAD"} else 1
        for attempt in range(attempts):
            response = self._send(method, path, version=version, params=params, json=json)
            if response.status_code < 400:
                self._log_response(response, method, path, attempt)
                return response
            if self._should_retry(response, attempt, attempts):
                self._wait_for_retry(response)
                continue
            self._raise_for_response(response)
        raise AssertionError("Retry loop must return or raise.")

    def _ensure_authenticated(self) -> None:
        if self._tokens is not None:
            return
        credentials = self._config.credentials
        response = self._http.post(
            self._url("/session"),
            json={"identifier": credentials.identifier, "password": credentials.password},
            headers={
                "Accept": "application/json; charset=utf-8",
                "Content-Type": "application/json; charset=utf-8",
                "Version": str(credentials.version),
                "X-IG-API-KEY": credentials.api_key,
            },
        )
        if response.status_code >= 400:
            self._raise_for_response(response, AuthenticationError)

        if isinstance(credentials, SessionCredentials):
            cst = response.headers.get("CST")
            security_token = response.headers.get("X-SECURITY-TOKEN")
            if not cst or not security_token:
                raise AuthenticationError(
                    "IG session response did not include both security tokens."
                )
            self._tokens = SessionTokens(cst=cst, security_token=security_token)
            return

        if isinstance(credentials, OAuthCredentials):
            access_token = response.json().get("oauthToken", {}).get("access_token")
            if not access_token:
                raise AuthenticationError("IG OAuth response did not include an access token.")
            self._tokens = SessionTokens(access_token=access_token)
            return

        raise AuthenticationError("Unsupported credentials type.")

    def _send(
        self,
        method: str,
        path: str,
        *,
        version: int,
        params: Mapping[str, Any] | None,
        json: Mapping[str, Any] | None,
    ) -> httpx.Response:
        return self._http.request(
            method,
            self._url(path),
            params=params,
            json=json,
            headers=self._headers(version),
        )

    def _headers(self, version: int) -> dict[str, str]:
        credentials = self._config.credentials
        headers = {
            "Accept": "application/json; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8",
            "Version": str(version),
            "X-IG-API-KEY": credentials.api_key,
        }
        if self._tokens is None:
            return headers
        if self._tokens.access_token:
            headers["Authorization"] = f"Bearer {self._tokens.access_token}"
            if self._config.account_id:
                headers["IG-ACCOUNT-ID"] = self._config.account_id
        else:
            headers["CST"] = self._tokens.cst or ""
            headers["X-SECURITY-TOKEN"] = self._tokens.security_token or ""
        return headers

    def _url(self, path: str) -> str:
        return f"{self._config.base_url}{path if path.startswith('/') else f'/{path}'}"

    @staticmethod
    def _should_retry(response: httpx.Response, attempt: int, attempts: int) -> bool:
        return attempt + 1 < attempts and response.status_code in {429, 500, 502, 503, 504}

    @staticmethod
    def _wait_for_retry(response: httpx.Response) -> None:
        retry_after = response.headers.get("Retry-After")
        delay = float(retry_after) if retry_after and retry_after.isdigit() else 0.1
        time.sleep(delay)

    def _raise_for_response(
        self,
        response: httpx.Response,
        error_type: type[IGError] | None = None,
    ) -> None:
        payload = self._error_payload(response)
        error_code = payload.get("errorCode")
        common = {
            "status_code": response.status_code,
            "error_code": error_code,
            "request_id": response.headers.get("X-REQUEST-ID"),
            "retry_after_seconds": self._retry_after(response),
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

    @staticmethod
    def _error_payload(response: httpx.Response) -> dict[str, Any]:
        try:
            payload = response.json()
        except ValueError:
            return {}
        return payload if isinstance(payload, dict) else {}

    @staticmethod
    def _retry_after(response: httpx.Response) -> float | None:
        value = response.headers.get("Retry-After")
        return float(value) if value and value.isdigit() else None

    @staticmethod
    def _log_response(response: httpx.Response, method: str, path: str, attempt: int) -> None:
        logger.info(
            "ig.http.response",
            extra={
                "ig_event": "http_response",
                "ig_method": method,
                "ig_path": path,
                "ig_status_code": response.status_code,
                "ig_request_id": response.headers.get("X-REQUEST-ID"),
                "ig_retry_count": attempt,
            },
        )
