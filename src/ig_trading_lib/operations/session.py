"""Typed IG session operations."""

from __future__ import annotations

from pydantic import Field

from ig_trading_lib._protocol.executor import AsyncExecutor, SyncExecutor
from ig_trading_lib.models import IGModel, IGRequest


class SessionResponse(IGModel):
    account_id: str | None = None
    client_id: str | None = None
    currency: str | None = None
    lightstreamer_endpoint: str | None = None
    locale: str | None = None
    timezone_offset: int | None = None
    cst: str | None = None
    security_token: str | None = None


class SwitchAccountRequest(IGRequest):
    account_id: str = Field(min_length=1)
    default_account: bool = False


class SwitchAccountResponse(IGModel):
    dealing_enabled: bool | None = None
    has_active_demo_accounts: bool | None = None
    has_active_live_accounts: bool | None = None
    trailing_stops_enabled: bool | None = None


class DeleteSessionResponse(IGModel):
    status: str | None = None


class EncryptionKeyResponse(IGModel):
    encryption_key: str
    time_stamp: int


class SessionOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def get(self, *, fetch_session_tokens: bool = False) -> SessionResponse:
        return self._executor.execute(
            "session.get",
            SessionResponse,
            query={"fetchSessionTokens": "true"} if fetch_session_tokens else None,
        )

    def switch_account(self, request: SwitchAccountRequest) -> SwitchAccountResponse:
        return self._executor.execute(
            "session.switch_account", SwitchAccountResponse, body=request.to_wire()
        )

    def delete(self) -> DeleteSessionResponse:
        return self._executor.execute("session.delete", DeleteSessionResponse)

    def get_encryption_key(self) -> EncryptionKeyResponse:
        return self._executor.execute("session.get_encryption_key", EncryptionKeyResponse)


class AsyncSessionOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def get(self, *, fetch_session_tokens: bool = False) -> SessionResponse:
        return await self._executor.execute(
            "session.get",
            SessionResponse,
            query={"fetchSessionTokens": "true"} if fetch_session_tokens else None,
        )

    async def switch_account(self, request: SwitchAccountRequest) -> SwitchAccountResponse:
        return await self._executor.execute(
            "session.switch_account", SwitchAccountResponse, body=request.to_wire()
        )

    async def delete(self) -> DeleteSessionResponse:
        return await self._executor.execute("session.delete", DeleteSessionResponse)

    async def get_encryption_key(self) -> EncryptionKeyResponse:
        return await self._executor.execute("session.get_encryption_key", EncryptionKeyResponse)
