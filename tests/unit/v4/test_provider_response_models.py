from decimal import Decimal

import httpx

from ig_trading_lib import IG, Environment, IGConfig, SessionCredentials
from ig_trading_lib.operations.accounts import (
    Activity,
    ActivityAction,
    ActivityDetails,
    Transaction,
)
from ig_trading_lib.operations.dealing import (
    DealConfirmationResponse,
    DealingMarket,
    Position,
    PositionsResponse,
    WorkingOrdersResponse,
)
from ig_trading_lib.operations.markets import (
    CategoriesResponse,
    CategoryInstrumentsQuery,
    CategoryInstrumentsResponse,
    MarketDealingRules,
    MarketGetResponse,
    MarketInstrument,
    MarketSnapshot,
    PricePoint,
    PricesQuery,
    PricesResponse,
)
from ig_trading_lib.operations.session import SwitchAccountResponse
from ig_trading_lib.operations.watchlists import WatchlistResponse


def test_positions_response_matches_the_official_nested_shape() -> None:
    response = PositionsResponse.model_validate(
        {
            "positions": [
                {
                    "position": {
                        "dealId": "position-id",
                        "dealReference": "position-reference",
                        "direction": "BUY",
                        "size": 1.5,
                    },
                    "market": {
                        "epic": "CS.D.EURUSD.CFD.IP",
                        "instrumentName": "EUR/USD",
                        "bid": 1.08,
                    },
                }
            ]
        }
    )

    item = response.positions[0]
    assert item.position.deal_id == "position-id"
    assert item.position.size == Decimal("1.5")
    assert item.market.epic == "CS.D.EURUSD.CFD.IP"
    assert item.market.instrument_name == "EUR/USD"


def test_working_orders_response_matches_the_official_nested_shape() -> None:
    response = WorkingOrdersResponse.model_validate(
        {
            "workingOrders": [
                {
                    "workingOrderData": {
                        "dealId": "order-id",
                        "epic": "CS.D.EURUSD.CFD.IP",
                        "direction": "SELL",
                        "orderSize": 2,
                    },
                    "marketData": {
                        "epic": "CS.D.EURUSD.CFD.IP",
                        "instrumentName": "EUR/USD",
                        "offer": 1.09,
                    },
                }
            ]
        }
    )

    item = response.working_orders[0]
    assert item.working_order_data.deal_id == "order-id"
    assert item.working_order_data.order_size == Decimal("2")
    assert item.market_data.epic == "CS.D.EURUSD.CFD.IP"


def test_price_and_watchlist_nested_fields_remain_typed() -> None:
    prices = PricesResponse.model_validate(
        {
            "prices": [
                {
                    "snapshotTime": "2026/08/09 12:00:00",
                    "openPrice": {"bid": 1.08, "ask": 1.09},
                }
            ]
        }
    )
    watchlist = WatchlistResponse.model_validate(
        {
            "id": "watchlist-id",
            "markets": [{"epic": "CS.D.EURUSD.CFD.IP", "instrumentName": "EUR/USD"}],
        }
    )

    assert prices.prices[0].open_price is not None
    assert prices.prices[0].open_price.bid == Decimal("1.08")
    assert watchlist.markets[0].epic == "CS.D.EURUSD.CFD.IP"


def test_price_history_v3_exposes_the_complete_query_and_response_schema() -> None:
    assert set(PricesQuery.model_fields) == {
        "resolution",
        "from_date",
        "to_date",
        "max_points",
        "page_size",
        "page_number",
    }
    assert set(PricePoint.model_fields) == {
        "snapshot_time",
        "snapshot_time_utc",
        "open_price",
        "close_price",
        "high_price",
        "low_price",
        "last_traded_volume",
    }

    response = PricesResponse.model_validate(
        {
            "instrumentType": "CURRENCIES",
            "metadata": {
                "pageData": {"pageNumber": 2, "pageSize": 25, "totalPages": 3},
                "size": 1,
                "allowance": {
                    "allowanceExpiry": 60,
                    "remainingAllowance": 999,
                    "totalAllowance": 1000,
                },
            },
            "prices": [
                {
                    "snapshotTime": "2026/08/09 12:00:00",
                    "snapshotTimeUTC": "2026-08-09T11:00:00",
                    "closePrice": {"bid": 1.08, "ask": 1.09, "lastTraded": 1.085},
                }
            ],
        }
    )

    assert response.metadata is not None
    assert response.metadata.page_data is not None
    assert response.metadata.page_data.total_pages == 3
    assert response.metadata.allowance is not None
    assert response.metadata.allowance.remaining_allowance == 999
    assert response.prices[0].snapshot_time_utc == "2026-08-09T11:00:00"


def test_core_dealing_and_history_models_type_every_documented_field() -> None:
    assert set(DealConfirmationResponse.model_fields) == {
        "affected_deals",
        "date",
        "deal_id",
        "deal_reference",
        "deal_status",
        "direction",
        "epic",
        "expiry",
        "guaranteed_stop",
        "level",
        "limit_distance",
        "limit_level",
        "profit",
        "profit_currency",
        "reason",
        "size",
        "status",
        "stop_distance",
        "stop_level",
        "trailing_stop",
    }
    assert set(Position.model_fields) == {
        "contract_size",
        "controlled_risk",
        "created_date",
        "created_date_utc",
        "currency",
        "deal_id",
        "deal_reference",
        "direction",
        "level",
        "limit_level",
        "limited_risk_premium",
        "size",
        "stop_level",
        "trailing_step",
        "trailing_stop_distance",
    }
    assert set(DealingMarket.model_fields) == {
        "bid",
        "delay_time",
        "epic",
        "expiry",
        "high",
        "instrument_name",
        "instrument_type",
        "lot_size",
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
    assert set(Activity.model_fields) == {
        "action_status",
        "activity",
        "activity_history_id",
        "channel",
        "currency",
        "date",
        "deal_id",
        "description",
        "details",
        "epic",
        "level",
        "limit",
        "market_name",
        "result",
        "size",
        "stop",
        "stop_type",
        "time",
    }
    assert set(ActivityDetails.model_fields) == {
        "actions",
        "epic",
        "period",
        "status",
        "type",
    }
    assert set(ActivityAction.model_fields) == {
        "action_type",
        "affected_deal_id",
        "currency",
        "deal_reference",
        "direction",
        "good_till_date",
        "guaranteed_stop",
        "level",
        "limit_distance",
        "limit_level",
        "market_name",
        "size",
        "stop_distance",
        "stop_level",
        "trailing_step",
        "trailing_stop_distance",
    }
    assert set(Transaction.model_fields) == {
        "cash_transaction",
        "close_level",
        "currency",
        "date",
        "date_utc",
        "instrument_name",
        "open_date_utc",
        "open_level",
        "period",
        "profit_and_loss",
        "reference",
        "size",
        "transaction_type",
    }


def test_switch_account_response_uses_the_official_fields() -> None:
    response = SwitchAccountResponse.model_validate(
        {
            "dealingEnabled": True,
            "hasActiveDemoAccounts": True,
            "hasActiveLiveAccounts": False,
            "trailingStopsEnabled": True,
        }
    )

    assert response.dealing_enabled is True
    assert response.has_active_demo_accounts is True
    assert response.has_active_live_accounts is False


def test_category_responses_match_the_official_wire_shape_and_query() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(
                200,
                headers={"CST": "cst", "X-SECURITY-TOKEN": "security"},
            )
        if request.url.path == "/gateway/deal/categories":
            return httpx.Response(
                200,
                json={"categories": [{"code": "FX", "nonTradeable": False}]},
            )
        return httpx.Response(
            200,
            json={
                "instruments": [
                    {
                        "epic": "CS.D.EURUSD.CFD.IP",
                        "instrumentName": "EUR/USD",
                        "expiry": "DFB",
                        "instrumentType": "CURRENCIES",
                        "lotSize": 1,
                        "otcTradeable": True,
                        "marketStatus": "TRADEABLE",
                        "delayTime": 0,
                        "bid": 1.08,
                        "offer": 1.09,
                        "high": 1.10,
                        "low": 1.07,
                        "netChange": 0.01,
                        "percentageChange": 0.9,
                        "updateTime": "12:00:00",
                        "scalingFactor": 1,
                    }
                ],
                "metadata": {"pageNumber": 2, "pageSize": 25},
            },
        )

    config = IGConfig(
        environment=Environment.DEMO,
        credentials=SessionCredentials(api_key="key", identifier="user", password="pass"),
    )
    with IG(config, http_client=httpx.Client(transport=httpx.MockTransport(handler))) as ig:
        categories = ig.operations.categories.list()
        instruments = ig.operations.categories.list_instruments(
            "FX",
            CategoryInstrumentsQuery(
                page_number=2,
                page_size=25,
                reference_epic="CS.D.EURUSD.CFD.IP",
                maturity_type="DAILY",
            ),
        )

    assert isinstance(categories, CategoriesResponse)
    assert categories.categories[0].code == "FX"
    assert categories.categories[0].non_tradeable is False
    assert isinstance(instruments, CategoryInstrumentsResponse)
    assert instruments.instruments[0].instrument_type == "CURRENCIES"
    assert instruments.instruments[0].bid == Decimal("1.08")
    assert instruments.metadata.page_number == 2
    assert dict(requests[-1].url.params) == {
        "pageNumber": "2",
        "pageSize": "25",
        "referenceEpic": "CS.D.EURUSD.CFD.IP",
        "maturityType": "DAILY",
    }


def test_market_details_type_every_documented_v4_response_field() -> None:
    assert set(MarketDealingRules.model_fields) == {
        "controlled_risk_spacing",
        "max_stop_or_limit_distance",
        "min_controlled_risk_stop_distance",
        "min_deal_size",
        "min_normal_stop_or_limit_distance",
        "min_step_distance",
        "trailing_stops_preference",
    }
    assert set(MarketInstrument.model_fields) == {
        "chart_code",
        "contract_size",
        "country",
        "currencies",
        "epic",
        "expiry",
        "limited_risk_premium",
        "lot_size",
        "market_id",
        "name",
        "news_code",
        "streaming_prices_available",
        "limit_allowed",
        "stop_allowed",
        "type",
        "unit",
        "value_of_one_pip",
    }
    assert set(MarketSnapshot.model_fields) == {
        "decimal_places_factor",
        "delay_time",
        "high",
        "low",
        "market_status",
        "net_change",
        "percentage_change",
        "scaling_factor",
        "update_timestamp_utc",
        "price_ladder",
        "currency_ladders",
    }

    response = MarketGetResponse.model_validate(
        {
            "dealingRules": {
                "controlledRiskSpacing": {"unit": "POINTS", "value": 2},
                "maxStopOrLimitDistance": {"unit": "PERCENTAGE", "value": 90},
                "minControlledRiskStopDistance": {"unit": "POINTS", "value": 5},
                "minDealSize": {"unit": "POINTS", "value": 0.5},
                "minNormalStopOrLimitDistance": {"unit": "POINTS", "value": 1},
                "minStepDistance": {"unit": "POINTS", "value": 0.1},
                "trailingStopsPreference": "AVAILABLE",
            },
            "instrument": {
                "chartCode": "EURUSD",
                "contractSize": "1",
                "country": "GB",
                "currencies": [
                    {
                        "baseExchangeRate": 1,
                        "code": "GBP",
                        "exchangeRate": 1,
                        "isDefault": True,
                        "symbol": "GBP",
                    }
                ],
                "epic": "CS.D.EURUSD.CFD.IP",
                "expiry": "DFB",
                "limitedRiskPremium": {"unit": "POINTS", "value": 0.5},
                "lotSize": 1,
                "marketId": "EURUSD",
                "name": "EUR/USD",
                "newsCode": "EURUSD",
                "streamingPricesAvailable": True,
                "limitAllowed": True,
                "stopAllowed": True,
                "type": "CURRENCIES",
                "unit": "CONTRACTS",
                "valueOfOnePip": "1",
            },
            "snapshot": {
                "decimalPlacesFactor": 5,
                "delayTime": 0,
                "high": 1.10,
                "low": 1.07,
                "marketStatus": "TRADEABLE",
                "netChange": 0.01,
                "percentageChange": 0.9,
                "scalingFactor": 1,
                "updateTimestampUTC": 1786276800000,
                "priceLadder": [{"bid": "1.08", "ask": "1.09"}],
                "currencyLadders": [{"currency": "GBP", "bidSizes": [1, 2], "askSizes": [3, 4]}],
            },
        }
    )

    assert response.dealing_rules is not None
    assert response.dealing_rules.min_deal_size.value == Decimal("0.5")
    assert response.instrument.currencies[0].code == "GBP"
    assert response.instrument.limited_risk_premium is not None
    assert response.instrument.limited_risk_premium.value == Decimal("0.5")
    assert response.snapshot is not None
    assert response.snapshot.update_timestamp_utc == 1786276800000
    assert response.snapshot.price_ladder[0].bid == Decimal("1.08")
    assert response.snapshot.currency_ladders[0].ask_sizes == (Decimal("3"), Decimal("4"))
