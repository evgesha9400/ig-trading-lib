from __future__ import annotations

import httpx

from ig_trading_lib import IG, Environment, IGConfig, SessionCredentials
from ig_trading_lib.operations.accounts import ActivityQuery, TransactionsQuery


def _config() -> IGConfig:
    return IGConfig(
        environment=Environment.DEMO,
        credentials=SessionCredentials("key", "identifier", "password"),
    )


def test_activity_cursor_can_be_replayed_without_exposing_raw_requests() -> None:
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
                "activities": [],
                "metadata": {
                    "paging": {
                        "next": "/history/activity?from=2026-08-01T00%3A00%3A00"
                        "&to=2026-08-02T00%3A00%3A00&detailed=true&pageSize=10&version=3"
                    }
                },
            },
        )

    with IG(_config(), http_client=httpx.Client(transport=httpx.MockTransport(handler))) as ig:
        first = ig.operations.activity.list(ActivityQuery(page_size=10))
        next_query = first.next_query()
        assert next_query is not None
        second = ig.operations.activity.list(next_query)

    assert second.activities == ()
    assert dict(requests[1].url.params) == {"pageSize": "10"}
    assert dict(requests[2].url.params) == {
        "from": "2026-08-01T00:00:00",
        "to": "2026-08-02T00:00:00",
        "detailed": "true",
        "pageSize": "10",
    }


def test_transaction_page_controls_map_to_the_official_query() -> None:
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
                "transactions": [],
                "metadata": {
                    "pageData": {"pageNumber": 2, "pageSize": 50, "totalPages": 3},
                    "size": 0,
                },
            },
        )

    query = TransactionsQuery(
        transaction_type="ALL_DEAL",
        page_number=2,
        page_size=50,
    )
    with IG(_config(), http_client=httpx.Client(transport=httpx.MockTransport(handler))) as ig:
        response = ig.operations.transactions.list(query)

    assert response.metadata is not None
    assert response.metadata.page_data.page_number == 2
    assert dict(requests[1].url.params) == {
        "type": "ALL_DEAL",
        "pageNumber": "2",
        "pageSize": "50",
    }
