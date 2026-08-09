"""Typed account, activity, and transaction operations."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Literal
from urllib.parse import parse_qs, urlsplit

from pydantic import Field

from ig_trading_lib._protocol.executor import AsyncExecutor, SyncExecutor
from ig_trading_lib.models import IGModel, IGRequest


class AccountBalance(IGModel):
    available: Decimal | None = None
    balance: Decimal | None = None
    deposit: Decimal | None = None
    profit_loss: Decimal | None = None


class Account(IGModel):
    account_alias: str | None = None
    account_id: str
    account_name: str | None = None
    account_type: str | None = None
    balance: AccountBalance | None = None
    can_transfer_from: bool | None = None
    can_transfer_to: bool | None = None
    currency: str | None = None
    preferred: bool | None = None
    status: str | None = None


class AccountsResponse(IGModel):
    accounts: tuple[Account, ...]


class AccountPreferencesResponse(IGModel):
    trailing_stops_enabled: bool | None = None
    hedging_mode: str | None = None


class UpdateAccountPreferencesRequest(IGRequest):
    trailing_stops_enabled: bool | None = None
    hedging_mode: str | None = None


class UpdateAccountPreferencesResponse(AccountPreferencesResponse):
    pass


class ActivityAction(IGModel):
    action_type: str | None = None
    affected_deal_id: str | None = None
    currency: str | None = None
    deal_reference: str | None = None
    direction: Literal["BUY", "SELL"] | None = None
    good_till_date: str | None = None
    guaranteed_stop: bool | None = None
    level: Decimal | None = None
    limit_distance: Decimal | None = None
    limit_level: Decimal | None = None
    market_name: str | None = None
    size: Decimal | None = None
    stop_distance: Decimal | None = None
    stop_level: Decimal | None = None
    trailing_step: Decimal | None = None
    trailing_stop_distance: Decimal | None = None


class ActivityDetails(IGModel):
    actions: tuple[ActivityAction, ...] = ()
    epic: str | None = None
    period: str | None = None
    status: str | None = None
    type: str | None = None


class Activity(IGModel):
    action_status: str | None = None
    activity: str | None = None
    activity_history_id: str | None = None
    channel: str | None = None
    currency: str | None = None
    date: str | None = None
    deal_id: str | None = None
    description: str | None = None
    details: ActivityDetails | None = None
    epic: str | None = None
    level: Decimal | str | None = None
    limit: Decimal | str | None = None
    market_name: str | None = None
    period: str | None = None
    result: str | None = None
    size: Decimal | str | None = None
    stop: Decimal | str | None = None
    stop_type: str | None = None
    time: str | None = None


class CursorPaging(IGModel):
    next: str | None = None
    size: int | None = None


class CursorMetadata(IGModel):
    paging: CursorPaging


class ActivityQuery(IGRequest):
    from_date: date | datetime | str | None = Field(default=None, alias="from")
    to_date: date | datetime | str | None = Field(default=None, alias="to")
    detailed: bool | None = None
    deal_id: str | None = None
    filter: str | None = None
    page_size: int | None = Field(default=None, ge=10, le=500)

    @classmethod
    def from_next_url(cls, url: str) -> ActivityQuery:
        values = {key: items[-1] for key, items in parse_qs(urlsplit(url).query).items()}
        aliases = {field.alias for field in cls.model_fields.values()}
        return cls.model_validate({key: value for key, value in values.items() if key in aliases})


class ActivityResponse(IGModel):
    activities: tuple[Activity, ...] = ()
    metadata: CursorMetadata | None = None

    def next_query(self) -> ActivityQuery | None:
        if self.metadata is None or self.metadata.paging.next is None:
            return None
        return ActivityQuery.from_next_url(self.metadata.paging.next)


class Transaction(IGModel):
    cash_transaction: bool | None = None
    close_level: str | None = None
    currency: str | None = None
    date: str | None = None
    date_utc: str | None = None
    instrument_name: str | None = None
    open_date_utc: str | None = None
    open_level: str | None = None
    period: str | None = None
    profit_and_loss: str | None = None
    reference: str | None = None
    size: str | None = None
    transaction_type: str | None = None


class PageData(IGModel):
    page_number: int
    page_size: int
    total_pages: int


class NumberedPageMetadata(IGModel):
    page_data: PageData
    size: int | None = None


TransactionType = Literal["ALL", "ALL_DEAL", "DEPOSIT", "WITHDRAWAL"]


class TransactionsQuery(IGRequest):
    transaction_type: TransactionType = Field(default="ALL", alias="type")
    from_date: date | datetime | str | None = Field(default=None, alias="from")
    to_date: date | datetime | str | None = Field(default=None, alias="to")
    max_span_seconds: int | None = Field(default=None, ge=0)
    page_size: int | None = Field(default=None, ge=0)
    page_number: int | None = Field(default=None, ge=1)


class TransactionsResponse(IGModel):
    transactions: tuple[Transaction, ...] = ()
    metadata: NumberedPageMetadata | None = None


class AccountsOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def list(self) -> AccountsResponse:
        return self._executor.execute("accounts.list", AccountsResponse)

    def get_preferences(self) -> AccountPreferencesResponse:
        return self._executor.execute("accounts.get_preferences", AccountPreferencesResponse)

    def update_preferences(
        self, request: UpdateAccountPreferencesRequest
    ) -> UpdateAccountPreferencesResponse:
        return self._executor.execute(
            "accounts.update_preferences",
            UpdateAccountPreferencesResponse,
            body=request.to_wire(),
        )


class AsyncAccountsOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def list(self) -> AccountsResponse:
        return await self._executor.execute("accounts.list", AccountsResponse)

    async def get_preferences(self) -> AccountPreferencesResponse:
        return await self._executor.execute("accounts.get_preferences", AccountPreferencesResponse)

    async def update_preferences(
        self, request: UpdateAccountPreferencesRequest
    ) -> UpdateAccountPreferencesResponse:
        return await self._executor.execute(
            "accounts.update_preferences",
            UpdateAccountPreferencesResponse,
            body=request.to_wire(),
        )


def _time(value: date | datetime | str) -> str:
    return value.isoformat() if isinstance(value, date) else value


class ActivityOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def list(self, query: ActivityQuery | None = None) -> ActivityResponse:
        return self._executor.execute(
            "activity.list", ActivityResponse, query=query.to_wire() if query else None
        )

    def list_by_date_range(
        self, from_date: date | datetime | str, to_date: date | datetime | str
    ) -> ActivityResponse:
        return self._executor.execute(
            "activity.list_by_date_range",
            ActivityResponse,
            path={"from_date": _time(from_date), "to_date": _time(to_date)},
        )

    def list_by_period(self, period: str) -> ActivityResponse:
        return self._executor.execute(
            "activity.list_by_period", ActivityResponse, path={"period": period}
        )


class AsyncActivityOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def list(self, query: ActivityQuery | None = None) -> ActivityResponse:
        return await self._executor.execute(
            "activity.list", ActivityResponse, query=query.to_wire() if query else None
        )

    async def list_by_date_range(
        self, from_date: date | datetime | str, to_date: date | datetime | str
    ) -> ActivityResponse:
        return await self._executor.execute(
            "activity.list_by_date_range",
            ActivityResponse,
            path={"from_date": _time(from_date), "to_date": _time(to_date)},
        )

    async def list_by_period(self, period: str) -> ActivityResponse:
        return await self._executor.execute(
            "activity.list_by_period", ActivityResponse, path={"period": period}
        )


class TransactionsOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def list(self, query: TransactionsQuery | None = None) -> TransactionsResponse:
        return self._executor.execute(
            "transactions.list",
            TransactionsResponse,
            query=query.to_wire() if query else None,
        )

    def list_by_date_range(
        self,
        transaction_type: TransactionType,
        from_date: date | datetime | str,
        to_date: date | datetime | str,
    ) -> TransactionsResponse:
        return self._executor.execute(
            "transactions.list_by_date_range",
            TransactionsResponse,
            path={
                "transaction_type": transaction_type,
                "from_date": _time(from_date),
                "to_date": _time(to_date),
            },
        )

    def list_by_period(
        self, transaction_type: TransactionType, period: str
    ) -> TransactionsResponse:
        return self._executor.execute(
            "transactions.list_by_period",
            TransactionsResponse,
            path={"transaction_type": transaction_type, "period": period},
        )


class AsyncTransactionsOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def list(self, query: TransactionsQuery | None = None) -> TransactionsResponse:
        return await self._executor.execute(
            "transactions.list",
            TransactionsResponse,
            query=query.to_wire() if query else None,
        )

    async def list_by_date_range(
        self,
        transaction_type: TransactionType,
        from_date: date | datetime | str,
        to_date: date | datetime | str,
    ) -> TransactionsResponse:
        return await self._executor.execute(
            "transactions.list_by_date_range",
            TransactionsResponse,
            path={
                "transaction_type": transaction_type,
                "from_date": _time(from_date),
                "to_date": _time(to_date),
            },
        )

    async def list_by_period(
        self, transaction_type: TransactionType, period: str
    ) -> TransactionsResponse:
        return await self._executor.execute(
            "transactions.list_by_period",
            TransactionsResponse,
            path={"transaction_type": transaction_type, "period": period},
        )
