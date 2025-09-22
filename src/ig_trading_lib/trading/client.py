from typing import Any, Mapping, Optional, Protocol

import requests


class TradingClient(Protocol):
    def build_headers(self, *, override_version: Optional[str] = None, extra: Optional[dict] = None) -> dict: ...

    def get(
        self, path: str, params: Optional[Mapping[str, Any]] = None, headers: Optional[dict] = None
    ) -> requests.Response: ...

    def post(self, path: str, json: Optional[Any] = None, headers: Optional[dict] = None) -> requests.Response: ...

    def put(self, path: str, json: Optional[Any] = None, headers: Optional[dict] = None) -> requests.Response: ...

    def delete(self, path: str, headers: Optional[dict] = None) -> requests.Response: ...


class IGClient:
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        tokens,
        http: Optional[requests.sessions.Session] = None,
        default_version: str = "2",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.tokens = tokens
        self.http = http or requests
        self.default_version = default_version

    def build_headers(self, *, override_version: Optional[str] = None, extra: Optional[dict] = None) -> dict:
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json; charset=utf-8",
            "Version": override_version or self.default_version,
            "X-IG-API-KEY": self.api_key,
            "X-SECURITY-TOKEN": self.tokens.x_security_token,
            "CST": self.tokens.cst_token,
        }
        if extra:
            headers.update(extra)
        return headers

    def _url(self, path: str) -> str:
        if not path.startswith("/"):
            path = "/" + path
        return f"{self.base_url}{path}"

    def get(
        self,
        path: str,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[dict] = None,
    ) -> requests.Response:
        merged = self.build_headers()
        if headers:
            merged.update(headers)
        return self.http.get(self._url(path), headers=merged, params=params)

    def post(self, path: str, json: Optional[Any] = None, headers: Optional[dict] = None) -> requests.Response:
        merged = self.build_headers()
        if headers:
            merged.update(headers)
        return self.http.post(self._url(path), headers=merged, json=json)

    def put(self, path: str, json: Optional[Any] = None, headers: Optional[dict] = None) -> requests.Response:
        merged = self.build_headers()
        if headers:
            merged.update(headers)
        return self.http.put(self._url(path), headers=merged, json=json)

    def delete(self, path: str, headers: Optional[dict] = None) -> requests.Response:
        merged = self.build_headers()
        if headers:
            merged.update(headers)
        return self.http.delete(self._url(path), headers=merged)
