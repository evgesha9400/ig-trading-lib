# Requests and responses

Every operation and workflow page documents its complete parameter tree, recursive response shape,
copyable example, limitations, and exceptions. Start from the relevant
[operation](../operations/index.md) or [workflow](../workflows/index.md), not from a global model list.

## Convenience imports

The following frequently used dealing and discovery types are available directly from
`ig_trading_lib`:

| Type | Role | Primary reference |
| --- | --- | --- |
| `CreatePositionRequest` | Open-position request body. | [`positions.create`](../operations/positions.md) |
| `AmendPositionRequest` | Position-amendment request body. | [`positions.amend`](../operations/positions.md) |
| `ClosePositionRequest` | Position-close request body. | [`positions.close`](../operations/positions.md) |
| `CreateWorkingOrderRequest` | Working-order request body. | [`working_orders.create`](../operations/working_orders.md) |
| `AmendWorkingOrderRequest` | Working-order amendment body. | [`working_orders.amend`](../operations/working_orders.md) |
| `DealConfirmationResponse` | Confirmed dealing result. | [`confirmations.get`](../operations/confirmations.md) |
| `MarketSearchResponse` | Market-search result. | [`markets.search`](../operations/markets.md) |
| `MarketGetResponse` | Detailed market result. | [`markets.get`](../operations/markets.md) |

```python
from ig_trading_lib import CreatePositionRequest

request = CreatePositionRequest(
    epic="CS.D.EURUSD.CFD.IP",
    direction="BUY",
    size=1,
    order_type="MARKET",
    currency_code="GBP",
)
confirmation = ig.workflows.positions.open_and_confirm(request)
```

## Model behaviour

- Request models validate declared fields before transport.
- Response models normalise documented provider fields to `snake_case`.
- Provider-added response fields remain available for forward compatibility.
- Invalid request data or incompatible response data raises `pydantic.ValidationError`.
- Method pages are authoritative for defaults, constraints, nested shapes, and examples.

## Dealing requests

::: ig_trading_lib.operations.dealing.CreatePositionRequest

::: ig_trading_lib.operations.dealing.AmendPositionRequest

::: ig_trading_lib.operations.dealing.ClosePositionRequest

::: ig_trading_lib.operations.dealing.CreateWorkingOrderRequest

::: ig_trading_lib.operations.dealing.AmendWorkingOrderRequest

## Common responses

::: ig_trading_lib.operations.dealing.DealConfirmationResponse

::: ig_trading_lib.operations.markets.MarketSearchResponse

::: ig_trading_lib.operations.markets.MarketGetResponse
