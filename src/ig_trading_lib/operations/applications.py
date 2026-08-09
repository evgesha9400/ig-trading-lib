"""Typed API-application operations."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from ig_trading_lib._protocol.executor import AsyncExecutor, SyncExecutor
from ig_trading_lib.models import IGModel, IGRequest


class Application(IGModel):
    allow_equities: bool | None = None
    allow_quote_orders: bool | None = None
    allowance_account_historical_data: int | None = None
    allowance_account_overall: int | None = None
    allowance_account_trading: int | None = None
    allowance_application_overall: int | None = None
    api_key: str | None = None
    concurrent_subscriptions_limit: int | None = None
    created_date: str | None = None
    name: str | None = None
    status: str | None = None


class ApplicationsResponse(IGModel):
    applications: tuple[Application, ...] = ()


class UpdateApplicationRequest(IGRequest):
    api_key: str = Field(min_length=1)
    status: Literal["DISABLED", "ENABLED", "REVOKED"]
    allowance_account_overall: int = Field(ge=0)
    allowance_account_trading: int = Field(ge=0)


class ApplicationsOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def list(self) -> ApplicationsResponse:
        return self._executor.execute("applications.list", ApplicationsResponse)

    def update(self, request: UpdateApplicationRequest) -> Application:
        return self._executor.execute("applications.update", Application, body=request.to_wire())

    def disable(self) -> Application:
        return self._executor.execute("applications.disable", Application)


class AsyncApplicationsOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def list(self) -> ApplicationsResponse:
        return await self._executor.execute("applications.list", ApplicationsResponse)

    async def update(self, request: UpdateApplicationRequest) -> Application:
        return await self._executor.execute(
            "applications.update", Application, body=request.to_wire()
        )

    async def disable(self) -> Application:
        return await self._executor.execute("applications.disable", Application)
