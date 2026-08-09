"""Typed API-application operations."""

from __future__ import annotations

from pydantic import Field

from ig_trading_lib._protocol.executor import AsyncExecutor, SyncExecutor
from ig_trading_lib.models import IGModel, IGRequest


class Application(IGModel):
    api_key: str | None = None
    name: str | None = None
    status: str | None = None
    allowance_account_overall: int | None = None
    allowance_account_trading: int | None = None
    allowance_application_overall: int | None = None


class ApplicationsResponse(IGModel):
    applications: tuple[Application, ...] = ()


class UpdateApplicationRequest(IGRequest):
    api_key: str = Field(min_length=1)
    status: str
    allowance_account_overall: int | None = Field(default=None, ge=0)
    allowance_account_trading: int | None = Field(default=None, ge=0)
    allowance_application_overall: int | None = Field(default=None, ge=0)


class DisableApplicationRequest(IGRequest):
    api_key: str = Field(min_length=1)


class ApplicationMutationResponse(IGModel):
    status: str | None = None


class ApplicationsOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def list(self) -> ApplicationsResponse:
        return self._executor.execute("applications.list", ApplicationsResponse)

    def update(self, request: UpdateApplicationRequest) -> ApplicationMutationResponse:
        return self._executor.execute(
            "applications.update", ApplicationMutationResponse, body=request.to_wire()
        )

    def disable(self, request: DisableApplicationRequest) -> ApplicationMutationResponse:
        return self._executor.execute(
            "applications.disable", ApplicationMutationResponse, body=request.to_wire()
        )


class AsyncApplicationsOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def list(self) -> ApplicationsResponse:
        return await self._executor.execute("applications.list", ApplicationsResponse)

    async def update(self, request: UpdateApplicationRequest) -> ApplicationMutationResponse:
        return await self._executor.execute(
            "applications.update", ApplicationMutationResponse, body=request.to_wire()
        )

    async def disable(self, request: DisableApplicationRequest) -> ApplicationMutationResponse:
        return await self._executor.execute(
            "applications.disable", ApplicationMutationResponse, body=request.to_wire()
        )
