from __future__ import annotations

from decimal import Decimal

import httpx

from ig_trading_lib import IG, Environment, IGConfig, SessionCredentials
from ig_trading_lib.operations.accounts import Account, AccountBalance
from ig_trading_lib.operations.applications import Application, UpdateApplicationRequest
from ig_trading_lib.operations.costs import (
    ClosingIndicativeCost,
    DurableMediumResponse,
    EditIndicativeCostResponse,
    IndicativeCostHistoryEntry,
    IndicativeCostHistoryPagination,
    IndicativeCostHistoryResponse,
    OpenIndicativeCostResponse,
)
from ig_trading_lib.operations.dealing import (
    RepeatDealingCurrency,
    RepeatDealingEntry,
    RepeatDealingExecution,
    RepeatDealingWindowResponse,
    WorkingOrderData,
)
from ig_trading_lib.operations.markets import (
    DetailedMarketDealingRules,
    DetailedMarketInstrument,
    DetailedMarketSnapshot,
    MarketsResponse,
    MarketSummary,
)
from ig_trading_lib.operations.session import SessionResponse
from ig_trading_lib.operations.watchlists import Watchlist, WatchlistMarket


def _config() -> IGConfig:
    return IGConfig(
        environment=Environment.DEMO,
        credentials=SessionCredentials("key", "identifier", "password"),
    )


def test_market_operations_match_the_complete_search_and_list_contracts() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(
                200,
                headers={"CST": "cst", "X-SECURITY-TOKEN": "security"},
            )
        return httpx.Response(
            200,
            json={
                "marketDetails": [
                    {
                        "instrument": {
                            "epic": "CS.D.EURUSD.CFD.IP",
                            "type": "CURRENCIES",
                            "expiryDetails": {"lastDealingDate": "-", "settlementInfo": "-"},
                            "marginDepositBands": [
                                {"currency": "GBP", "margin": 5, "min": 0, "max": 1000}
                            ],
                            "openingHours": {
                                "marketTimes": [{"openTime": "00:00", "closeTime": "23:59"}]
                            },
                        },
                        "dealingRules": {"marketOrderPreference": "AVAILABLE_DEFAULT_ON"},
                        "snapshot": {"bid": 1.08, "offer": 1.09, "updateTime": "12:00:00"},
                    }
                ]
            },
        )

    with IG(_config(), http_client=httpx.Client(transport=httpx.MockTransport(handler))) as ig:
        response = ig.operations.markets.list(("CS.D.EURUSD.CFD.IP",), filter="SNAPSHOT_ONLY")

    assert isinstance(response, MarketsResponse)
    assert response.market_details[0].instrument.expiry_details is not None
    assert response.market_details[0].instrument.margin_deposit_bands[0].margin == Decimal("5")
    assert response.market_details[0].dealing_rules.market_order_preference == (
        "AVAILABLE_DEFAULT_ON"
    )
    assert response.market_details[0].snapshot.bid == Decimal("1.08")
    assert dict(requests[1].url.params) == {
        "epics": "CS.D.EURUSD.CFD.IP",
        "filter": "SNAPSHOT_ONLY",
    }

    assert set(MarketSummary.model_fields) == {
        "bid",
        "delay_time",
        "epic",
        "expiry",
        "high",
        "instrument_name",
        "instrument_type",
        "low",
        "market_status",
        "net_change",
        "offer",
        "percentage_change",
        "scaling_factor",
        "streaming_prices_available",
        "update_time",
        "update_time_utc",
    }
    assert "controlled_risk_allowed" in DetailedMarketInstrument.model_fields
    assert "market_order_preference" in DetailedMarketDealingRules.model_fields
    assert "controlled_risk_extra_spread" in DetailedMarketSnapshot.model_fields


def test_account_session_working_order_and_watchlist_models_are_complete() -> None:
    assert set(AccountBalance.model_fields) == {
        "available",
        "balance",
        "deposit",
        "profit_loss",
    }
    assert set(Account.model_fields) == {
        "account_alias",
        "account_id",
        "account_name",
        "account_type",
        "balance",
        "can_transfer_from",
        "can_transfer_to",
        "currency",
        "preferred",
        "status",
    }
    assert set(SessionResponse.model_fields) == {
        "account_id",
        "client_id",
        "currency",
        "lightstreamer_endpoint",
        "locale",
        "timezone_offset",
    }
    assert set(WorkingOrderData.model_fields) == {
        "created_date",
        "created_date_utc",
        "currency_code",
        "deal_id",
        "direction",
        "dma",
        "epic",
        "good_till_date",
        "good_till_date_iso",
        "guaranteed_stop",
        "limit_distance",
        "limited_risk_premium",
        "order_level",
        "order_size",
        "order_type",
        "stop_distance",
        "time_in_force",
    }
    assert set(Watchlist.model_fields) == {
        "default_system_watchlist",
        "deleteable",
        "editable",
        "id",
        "name",
    }
    assert set(WatchlistMarket.model_fields) == set(MarketSummary.model_fields) | {"lot_size"}


def test_repeat_dealing_window_exposes_the_complete_typed_shape_and_filter() -> None:
    assert set(RepeatDealingExecution.model_fields) == {"size", "expiry"}
    assert set(RepeatDealingCurrency.model_fields) == {"currency", "buy", "sell"}
    assert set(RepeatDealingEntry.model_fields) == {
        "instrument_source",
        "instrument_value",
        "currency_list",
    }
    assert set(RepeatDealingWindowResponse.model_fields) == {
        "account_id",
        "request_start_time",
        "repeat_dealing_entry_list",
    }

    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(
                200,
                headers={"CST": "cst", "X-SECURITY-TOKEN": "security"},
            )
        return httpx.Response(
            200,
            json={
                "accountId": "account",
                "requestStartTime": 123,
                "repeatDealingEntryList": [],
            },
        )

    with IG(_config(), http_client=httpx.Client(transport=httpx.MockTransport(handler))) as ig:
        response = ig.operations.repeat_dealing_window.get(epic="CS.D.EURUSD.CFD.IP")

    assert response.account_id == "account"
    assert dict(requests[1].url.params) == {"epic": "CS.D.EURUSD.CFD.IP"}


def test_application_and_indicative_cost_responses_are_complete() -> None:
    assert set(Application.model_fields) == {
        "allow_equities",
        "allow_quote_orders",
        "allowance_account_historical_data",
        "allowance_account_overall",
        "allowance_account_trading",
        "allowance_application_overall",
        "api_key",
        "concurrent_subscriptions_limit",
        "created_date",
        "name",
        "status",
    }
    assert set(OpenIndicativeCostResponse.model_fields) == {
        "borrowing_charge",
        "closing_commission",
        "closing_fx_fee",
        "closing_iftt",
        "closing_spread",
        "currency_code_iso",
        "daily_running_fx_fee",
        "etp_entry_cost",
        "etp_exit_cost",
        "etp_ongoing_cost",
        "guaranteed_stop_deposit",
        "guaranteed_stop_return",
        "indicative_quote_reference",
        "inducements",
        "knockout_premium_deposit",
        "knockout_premium_return",
        "notional_value",
        "notional_value_in_user_currency",
        "opening_commission",
        "opening_fx_fee",
        "opening_iftt",
        "opening_spread",
        "overnight_funding_fee",
    }
    assert set(ClosingIndicativeCost.model_fields) == {
        "closing_commission",
        "closing_fx_fee",
        "closing_iftt",
        "closing_spread",
        "etp_exit_cost",
        "guaranteed_stop_return",
        "indicative_quote_reference",
        "knockout_premium_return",
        "notional_value",
        "notional_value_in_user_currency",
    }
    assert set(EditIndicativeCostResponse.model_fields) == {"currency_code_iso", "limit", "stop"}
    assert set(IndicativeCostHistoryEntry.model_fields) == {
        "created_timestamp",
        "direction",
        "indicative_quote_reference",
        "instrument_name",
        "type",
    }
    assert set(IndicativeCostHistoryPagination.model_fields) == {
        "page_number",
        "page_size",
        "total_elements",
        "total_pages",
    }
    assert set(IndicativeCostHistoryResponse.model_fields) == {
        "costs_and_charges_history",
        "pagination",
    }


def test_application_mutations_and_durable_medium_match_the_provider_wire_contract() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(
                200,
                headers={"CST": "cst", "X-SECURITY-TOKEN": "security"},
            )
        if request.url.path.endswith("/durablemedium/quote-reference"):
            return httpx.Response(
                200,
                content=b"%PDF-1.7\n",
                headers={"Content-Type": "application/pdf"},
            )
        return httpx.Response(200, json={"apiKey": "key", "status": "ENABLED"})

    with IG(_config(), http_client=httpx.Client(transport=httpx.MockTransport(handler))) as ig:
        updated = ig.operations.applications.update(
            UpdateApplicationRequest(
                api_key="key",
                status="ENABLED",
                allowance_account_overall=60,
                allowance_account_trading=30,
            )
        )
        disabled = ig.operations.applications.disable()
        durable = ig.operations.indicative_costs.get_durable_medium("quote-reference")

    assert isinstance(updated, Application)
    assert isinstance(disabled, Application)
    assert isinstance(durable, DurableMediumResponse)
    assert durable.content == b"%PDF-1.7\n"
    assert durable.content_type == "application/pdf"
    assert requests[2].content == b""
