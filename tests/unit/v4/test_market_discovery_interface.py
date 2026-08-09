import inspect

import httpx
import pytest

from ig_trading_lib import (
    IG,
    AsyncIG,
    Environment,
    IGConfig,
    MarketGetResponse,
    MarketSearchResponse,
    ResourceNotFoundError,
    SessionCredentials,
    TradingPermit,
)


def test_sync_market_operations_are_typed_and_preserve_provider_fields() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(
                200,
                headers={"CST": "cst", "X-SECURITY-TOKEN": "security"},
                json={"currentAccountId": "ABC123"},
            )
        if request.url.params.get("searchTerm"):
            return httpx.Response(
                200,
                json={
                    "markets": [
                        {
                            "epic": "CS.D.EURUSD.TODAY.IP",
                            "instrumentName": "EUR/USD",
                            "marketStatus": "TRADEABLE",
                            "providerSearchField": "preserved",
                        }
                    ],
                    "providerSearchMetadata": {"source": "IG"},
                },
            )
        return httpx.Response(
            200,
            json={
                "instrument": {
                    "epic": "CS.D.EURUSD.TODAY.IP",
                    "name": "EUR/USD",
                    "providerInstrumentField": "preserved",
                },
                "snapshot": {"marketStatus": "TRADEABLE", "bid": 1.0812},
                "dealingRules": {"marketOrderPreference": "AVAILABLE_DEFAULT_OFF"},
                "providerDetailField": {"source": "IG"},
            },
        )

    with IG(_config(), http_client=httpx.Client(transport=httpx.MockTransport(handler))) as ig:
        search = ig.operations.markets.search(search_term="EURUSD")
        details = ig.operations.markets.get(epic="CS.D.EURUSD.TODAY.IP")

        assert not hasattr(ig, "markets")
        assert not hasattr(ig, "request")
        assert not hasattr(ig, "v1")
        assert {name for name in vars(ig) if not name.startswith("_")} == {
            "operations",
            "workflows",
        }

    assert isinstance(search, MarketSearchResponse)
    assert search.markets[0].epic == "CS.D.EURUSD.TODAY.IP"
    assert search.markets[0].instrument_name == "EUR/USD"
    assert search.markets[0].provider_search_field == "preserved"
    assert search.provider_search_metadata == {"source": "IG"}
    assert isinstance(details, MarketGetResponse)
    assert details.instrument.epic == "CS.D.EURUSD.TODAY.IP"
    assert details.instrument.provider_instrument_field == "preserved"
    assert details.snapshot is not None
    assert details.snapshot.market_status == "TRADEABLE"
    assert details.provider_detail_field == {"source": "IG"}
    assert [request.headers["Version"] for request in requests] == ["2", "1", "4"]
    assert [request.url.path for request in requests] == [
        "/gateway/deal/session",
        "/gateway/deal/markets",
        "/gateway/deal/markets/CS.D.EURUSD.TODAY.IP",
    ]


def test_sync_and_async_roots_share_the_same_safety_bearing_constructor_shape() -> None:
    sync_parameters = inspect.signature(IG).parameters
    async_parameters = inspect.signature(AsyncIG).parameters

    assert tuple(sync_parameters) == ("config", "trading_permit", "http_client")
    assert tuple(async_parameters) == tuple(sync_parameters)
    assert sync_parameters["trading_permit"].default is None
    assert async_parameters["trading_permit"].default is None

    IG(_config(), trading_permit=TradingPermit()).close()


def test_discovery_selects_an_exact_epic_before_retrieving_details() -> None:
    requested_paths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requested_paths.append(request.url.path)
        if request.url.path == "/gateway/deal/session":
            return _session_response()
        if request.url.path == "/gateway/deal/markets":
            return httpx.Response(
                200,
                json={
                    "markets": [
                        {"epic": "CS.D.EURUSD.CFD.IP"},
                        {"epic": "CS.D.EURUSD.TODAY.IP"},
                    ]
                },
            )
        return _market_response()

    with IG(_config(), http_client=httpx.Client(transport=httpx.MockTransport(handler))) as ig:
        market = ig.workflows.discovery.find_market(
            search_term="EURUSD",
            epic="CS.D.EURUSD.TODAY.IP",
        )

    assert isinstance(market, MarketGetResponse)
    assert market.instrument.epic == "CS.D.EURUSD.TODAY.IP"
    assert requested_paths == [
        "/gateway/deal/session",
        "/gateway/deal/markets",
        "/gateway/deal/markets/CS.D.EURUSD.TODAY.IP",
    ]


def test_discovery_rejects_search_results_without_the_exact_epic() -> None:
    requested_paths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requested_paths.append(request.url.path)
        if request.url.path == "/gateway/deal/session":
            return _session_response()
        return httpx.Response(200, json={"markets": [{"epic": "CS.D.EURUSD.CFD.IP"}]})

    with (
        IG(_config(), http_client=httpx.Client(transport=httpx.MockTransport(handler))) as ig,
        pytest.raises(ResourceNotFoundError, match="exact epic"),
    ):
        ig.workflows.discovery.find_market(
            search_term="EURUSD",
            epic="CS.D.EURUSD.TODAY.IP",
        )

    assert requested_paths == ["/gateway/deal/session", "/gateway/deal/markets"]


@pytest.mark.asyncio
async def test_async_market_interface_matches_sync_with_awaiting_as_the_only_difference() -> None:
    requested_paths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requested_paths.append(request.url.path)
        if request.url.path == "/gateway/deal/session":
            return _session_response()
        if request.url.path == "/gateway/deal/markets":
            return httpx.Response(200, json={"markets": [{"epic": "CS.D.EURUSD.TODAY.IP"}]})
        return _market_response()

    async with AsyncIG(
        _config(),
        trading_permit=TradingPermit(),
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    ) as ig:
        search = await ig.operations.markets.search(search_term="EURUSD")
        details = await ig.operations.markets.get(epic="CS.D.EURUSD.TODAY.IP")
        discovered = await ig.workflows.discovery.find_market(
            search_term="EURUSD",
            epic="CS.D.EURUSD.TODAY.IP",
        )

        assert {name for name in vars(ig) if not name.startswith("_")} == {
            "operations",
            "workflows",
        }

    assert isinstance(search, MarketSearchResponse)
    assert isinstance(details, MarketGetResponse)
    assert isinstance(discovered, MarketGetResponse)
    assert details == discovered
    assert requested_paths == [
        "/gateway/deal/session",
        "/gateway/deal/markets",
        "/gateway/deal/markets/CS.D.EURUSD.TODAY.IP",
        "/gateway/deal/markets",
        "/gateway/deal/markets/CS.D.EURUSD.TODAY.IP",
    ]


def _session_response() -> httpx.Response:
    return httpx.Response(
        200,
        headers={"CST": "cst", "X-SECURITY-TOKEN": "security"},
        json={"currentAccountId": "ABC123"},
    )


def _market_response() -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "instrument": {"epic": "CS.D.EURUSD.TODAY.IP", "name": "EUR/USD"},
            "snapshot": {"marketStatus": "TRADEABLE", "bid": 1.0812},
            "dealingRules": {"marketOrderPreference": "AVAILABLE_DEFAULT_OFF"},
        },
    )


def _config() -> IGConfig:
    return IGConfig(
        environment=Environment.DEMO,
        credentials=SessionCredentials(
            api_key="api-key",
            identifier="identifier",
            password="password",
        ),
    )
