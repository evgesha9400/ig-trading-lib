from __future__ import annotations

import httpx
import pytest

from ig_trading_lib import (
    IG,
    AsyncIG,
    CreatePositionRequest,
    DealConfirmationError,
    Environment,
    IGConfig,
    SessionCredentials,
    TransportError,
)


def _config() -> IGConfig:
    return IGConfig(
        environment=Environment.DEMO,
        credentials=SessionCredentials("key", "identifier", "password"),
        max_retries=0,
    )


def _request() -> CreatePositionRequest:
    return CreatePositionRequest(
        epic="CS.D.EURUSD.CFD.IP",
        direction="BUY",
        size=1,
        order_type="MARKET",
        currency_code="GBP",
    )


def _handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/gateway/deal/session":
        return httpx.Response(
            200,
            headers={"CST": "cst", "X-SECURITY-TOKEN": "security"},
        )
    if request.url.path == "/gateway/deal/positions/otc":
        return httpx.Response(200, json={"dealReference": "deal-reference"})
    raise httpx.ReadTimeout("confirmation unavailable", request=request)


def test_sync_workflow_preserves_deal_reference_when_confirmation_fails() -> None:
    with (
        IG(_config(), http_client=httpx.Client(transport=httpx.MockTransport(_handler))) as ig,
        pytest.raises(DealConfirmationError) as raised,
    ):
        ig.workflows.positions.open_and_confirm(_request())

    assert raised.value.deal_reference == "deal-reference"
    assert raised.value.details == {"deal_reference": "deal-reference"}
    assert isinstance(raised.value.__cause__, TransportError)


@pytest.mark.asyncio
async def test_async_workflow_preserves_deal_reference_when_confirmation_fails() -> None:
    async with AsyncIG(
        _config(),
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(_handler)),
    ) as ig:
        with pytest.raises(DealConfirmationError) as raised:
            await ig.workflows.positions.open_and_confirm(_request())

    assert raised.value.deal_reference == "deal-reference"
    assert isinstance(raised.value.__cause__, TransportError)
