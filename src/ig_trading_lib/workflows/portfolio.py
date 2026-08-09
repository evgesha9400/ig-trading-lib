"""Portfolio snapshot workflows."""

from __future__ import annotations

from dataclasses import dataclass

from ig_trading_lib.models import IGModel
from ig_trading_lib.operations.accounts import (
    AccountsOperations,
    AccountsResponse,
    AsyncAccountsOperations,
)
from ig_trading_lib.operations.dealing import (
    AsyncPositionsOperations,
    AsyncWorkingOrdersOperations,
    PositionsOperations,
    PositionsResponse,
    WorkingOrdersOperations,
    WorkingOrdersResponse,
)


class PortfolioSnapshot(IGModel):
    accounts: AccountsResponse
    positions: PositionsResponse
    working_orders: WorkingOrdersResponse


@dataclass(frozen=True, slots=True)
class PortfolioWorkflow:
    accounts: AccountsOperations
    positions: PositionsOperations
    working_orders: WorkingOrdersOperations

    def snapshot(self) -> PortfolioSnapshot:
        return PortfolioSnapshot(
            accounts=self.accounts.list(),
            positions=self.positions.list(),
            working_orders=self.working_orders.list(),
        )


@dataclass(frozen=True, slots=True)
class AsyncPortfolioWorkflow:
    accounts: AsyncAccountsOperations
    positions: AsyncPositionsOperations
    working_orders: AsyncWorkingOrdersOperations

    async def snapshot(self) -> PortfolioSnapshot:
        return PortfolioSnapshot(
            accounts=await self.accounts.list(),
            positions=await self.positions.list(),
            working_orders=await self.working_orders.list(),
        )
