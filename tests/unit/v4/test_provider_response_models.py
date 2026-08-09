from decimal import Decimal

from ig_trading_lib.operations.dealing import PositionsResponse, WorkingOrdersResponse
from ig_trading_lib.operations.markets import PricesResponse
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
