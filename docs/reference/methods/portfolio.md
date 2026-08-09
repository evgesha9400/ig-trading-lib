<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Portfolio methods

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.workflows.portfolio.snapshot()`

Read accounts, open positions, and working orders as one portfolio view.

Official IG reference: [https://labs.ig.com/reference/positions.html](https://labs.ig.com/reference/positions.html)

### Signatures

- Sync: `() -> 'PortfolioSnapshot'`
- Async: `() -> 'PortfolioSnapshot'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| None | - | - | - | This method accepts no parameters. |

### Sync example

```python
result = ig.workflows.portfolio.snapshot()
```

### Async example

```python
result = await ig.workflows.portfolio.snapshot()
```

### Response shape: `PortfolioSnapshot`

| Field | Type | Required/default |
| --- | --- | --- |
| `accounts` | `AccountsResponse` | required |
| `accounts.accounts[]` | `tuple[Account, ...]` | required |
| `accounts.accounts[].account_alias` | `str | None` | default: `None` |
| `accounts.accounts[].account_id` | `str` | required |
| `accounts.accounts[].account_name` | `str | None` | default: `None` |
| `accounts.accounts[].account_type` | `str | None` | default: `None` |
| `accounts.accounts[].balance` | `AccountBalance | None` | default: `None` |
| `accounts.accounts[].balance.available` | `Decimal | None` | default: `None` |
| `accounts.accounts[].balance.balance` | `Decimal | None` | default: `None` |
| `accounts.accounts[].balance.deposit` | `Decimal | None` | default: `None` |
| `accounts.accounts[].balance.profit_loss` | `Decimal | None` | default: `None` |
| `accounts.accounts[].can_transfer_from` | `bool | None` | default: `None` |
| `accounts.accounts[].can_transfer_to` | `bool | None` | default: `None` |
| `accounts.accounts[].currency` | `str | None` | default: `None` |
| `accounts.accounts[].preferred` | `bool | None` | default: `None` |
| `accounts.accounts[].status` | `str | None` | default: `None` |
| `positions` | `PositionsResponse` | required |
| `positions.positions[]` | `tuple[PositionSummary, ...]` | default: `()` |
| `positions.positions[].position` | `Position` | required |
| `positions.positions[].position.contract_size` | `Decimal | None` | default: `None` |
| `positions.positions[].position.controlled_risk` | `bool | None` | default: `None` |
| `positions.positions[].position.created_date` | `str | None` | default: `None` |
| `positions.positions[].position.created_date_utc` | `str | None` | default: `None` |
| `positions.positions[].position.currency` | `str | None` | default: `None` |
| `positions.positions[].position.deal_id` | `str` | required |
| `positions.positions[].position.deal_reference` | `str | None` | default: `None` |
| `positions.positions[].position.direction` | `Literal['BUY', 'SELL'] | None` | default: `None` |
| `positions.positions[].position.size` | `Decimal | None` | default: `None` |
| `positions.positions[].position.level` | `Decimal | None` | default: `None` |
| `positions.positions[].position.limit_level` | `Decimal | None` | default: `None` |
| `positions.positions[].position.limited_risk_premium` | `Decimal | None` | default: `None` |
| `positions.positions[].position.stop_level` | `Decimal | None` | default: `None` |
| `positions.positions[].position.trailing_step` | `Decimal | None` | default: `None` |
| `positions.positions[].position.trailing_stop_distance` | `Decimal | None` | default: `None` |
| `positions.positions[].market` | `DealingMarket` | required |
| `positions.positions[].market.bid` | `Decimal | None` | default: `None` |
| `positions.positions[].market.delay_time` | `int | None` | default: `None` |
| `positions.positions[].market.epic` | `str` | required |
| `positions.positions[].market.expiry` | `str | None` | default: `None` |
| `positions.positions[].market.high` | `Decimal | None` | default: `None` |
| `positions.positions[].market.instrument_name` | `str | None` | default: `None` |
| `positions.positions[].market.instrument_type` | `str | None` | default: `None` |
| `positions.positions[].market.low` | `Decimal | None` | default: `None` |
| `positions.positions[].market.market_status` | `str | None` | default: `None` |
| `positions.positions[].market.net_change` | `Decimal | None` | default: `None` |
| `positions.positions[].market.offer` | `Decimal | None` | default: `None` |
| `positions.positions[].market.percentage_change` | `Decimal | None` | default: `None` |
| `positions.positions[].market.scaling_factor` | `Decimal | None` | default: `None` |
| `positions.positions[].market.streaming_prices_available` | `bool | None` | default: `None` |
| `positions.positions[].market.update_time` | `str | None` | default: `None` |
| `positions.positions[].market.update_time_utc` | `str | None` | default: `None` |
| `positions.positions[].market.lot_size` | `Decimal | None` | default: `None` |
| `working_orders` | `WorkingOrdersResponse` | required |
| `working_orders.working_orders[]` | `tuple[WorkingOrderSummary, ...]` | default: `()` |
| `working_orders.working_orders[].working_order_data` | `WorkingOrderData` | required |
| `working_orders.working_orders[].working_order_data.created_date` | `str | None` | default: `None` |
| `working_orders.working_orders[].working_order_data.created_date_utc` | `str | None` | default: `None` |
| `working_orders.working_orders[].working_order_data.currency_code` | `str | None` | default: `None` |
| `working_orders.working_orders[].working_order_data.deal_id` | `str` | required |
| `working_orders.working_orders[].working_order_data.direction` | `Literal['BUY', 'SELL'] | None` | default: `None` |
| `working_orders.working_orders[].working_order_data.dma` | `bool | None` | default: `None` |
| `working_orders.working_orders[].working_order_data.epic` | `str` | required |
| `working_orders.working_orders[].working_order_data.good_till_date` | `str | None` | default: `None` |
| `working_orders.working_orders[].working_order_data.good_till_date_iso` | `str | None` | default: `None` |
| `working_orders.working_orders[].working_order_data.guaranteed_stop` | `bool | None` | default: `None` |
| `working_orders.working_orders[].working_order_data.limit_distance` | `Decimal | None` | default: `None` |
| `working_orders.working_orders[].working_order_data.limited_risk_premium` | `Decimal | None` | default: `None` |
| `working_orders.working_orders[].working_order_data.order_level` | `Decimal | None` | default: `None` |
| `working_orders.working_orders[].working_order_data.order_size` | `Decimal | None` | default: `None` |
| `working_orders.working_orders[].working_order_data.order_type` | `str | None` | default: `None` |
| `working_orders.working_orders[].working_order_data.stop_distance` | `Decimal | None` | default: `None` |
| `working_orders.working_orders[].working_order_data.time_in_force` | `str | None` | default: `None` |
| `working_orders.working_orders[].market_data` | `WorkingOrderMarket` | required |
| `working_orders.working_orders[].market_data.bid` | `Decimal | None` | default: `None` |
| `working_orders.working_orders[].market_data.delay_time` | `int | None` | default: `None` |
| `working_orders.working_orders[].market_data.epic` | `str` | required |
| `working_orders.working_orders[].market_data.expiry` | `str | None` | default: `None` |
| `working_orders.working_orders[].market_data.high` | `Decimal | None` | default: `None` |
| `working_orders.working_orders[].market_data.instrument_name` | `str | None` | default: `None` |
| `working_orders.working_orders[].market_data.instrument_type` | `str | None` | default: `None` |
| `working_orders.working_orders[].market_data.low` | `Decimal | None` | default: `None` |
| `working_orders.working_orders[].market_data.market_status` | `str | None` | default: `None` |
| `working_orders.working_orders[].market_data.net_change` | `Decimal | None` | default: `None` |
| `working_orders.working_orders[].market_data.offer` | `Decimal | None` | default: `None` |
| `working_orders.working_orders[].market_data.percentage_change` | `Decimal | None` | default: `None` |
| `working_orders.working_orders[].market_data.scaling_factor` | `Decimal | None` | default: `None` |
| `working_orders.working_orders[].market_data.streaming_prices_available` | `bool | None` | default: `None` |
| `working_orders.working_orders[].market_data.update_time` | `str | None` | default: `None` |
| `working_orders.working_orders[].market_data.update_time_utc` | `str | None` | default: `None` |
| `working_orders.working_orders[].market_data.lot_size` | `Decimal | None` | default: `None` |
| `working_orders.working_orders[].market_data.exchange_id` | `str | None` | default: `None` |

### Response example

```json
{
  "accounts": {
    "accounts": [
      {
        "account_alias": "example",
        "account_id": "ABC123",
        "account_name": "example",
        "account_type": "example",
        "balance": {
          "available": "1.0",
          "balance": "1.0",
          "deposit": "1.0",
          "profit_loss": "1.0"
        },
        "can_transfer_from": true,
        "can_transfer_to": true,
        "currency": "GBP",
        "preferred": true,
        "status": "ENABLED"
      }
    ]
  },
  "positions": {
    "positions": [
      {
        "position": {
          "contract_size": "1.0",
          "controlled_risk": true,
          "created_date": "example",
          "created_date_utc": "example",
          "currency": "GBP",
          "deal_id": "DIAAAABBBCCC",
          "deal_reference": "ABC123",
          "direction": "BUY",
          "size": "1.0",
          "level": "1.0",
          "limit_level": "1.0",
          "limited_risk_premium": "1.0",
          "stop_level": "1.0",
          "trailing_step": "1.0",
          "trailing_stop_distance": "1.0"
        },
        "market": {
          "bid": "1.0",
          "delay_time": 1,
          "epic": "CS.D.EURUSD.CFD.IP",
          "expiry": "-",
          "high": "1.0",
          "instrument_name": "EUR/USD",
          "instrument_type": "example",
          "low": "1.0",
          "market_status": "TRADEABLE",
          "net_change": "1.0",
          "offer": "1.0",
          "percentage_change": "1.0",
          "scaling_factor": "1.0",
          "streaming_prices_available": true,
          "update_time": "12:34:56",
          "update_time_utc": "example",
          "lot_size": "1.0"
        }
      }
    ]
  },
  "working_orders": {
    "working_orders": [
      {
        "working_order_data": {
          "created_date": "example",
          "created_date_utc": "example",
          "currency_code": "GBP",
          "deal_id": "DIAAAABBBCCC",
          "direction": "BUY",
          "dma": true,
          "epic": "CS.D.EURUSD.CFD.IP",
          "good_till_date": "example",
          "good_till_date_iso": "example",
          "guaranteed_stop": true,
          "limit_distance": "1.0",
          "limited_risk_premium": "1.0",
          "order_level": "1.0",
          "order_size": "1.0",
          "order_type": "example",
          "stop_distance": "1.0",
          "time_in_force": "example"
        },
        "market_data": {
          "bid": "1.0",
          "delay_time": 1,
          "epic": "CS.D.EURUSD.CFD.IP",
          "expiry": "-",
          "high": "1.0",
          "instrument_name": "EUR/USD",
          "instrument_type": "example",
          "low": "1.0",
          "market_status": "TRADEABLE",
          "net_change": "1.0",
          "offer": "1.0",
          "percentage_change": "1.0",
          "scaling_factor": "1.0",
          "streaming_prices_available": true,
          "update_time": "12:34:56",
          "update_time_utc": "example",
          "lot_size": "1.0",
          "exchange_id": "example"
        }
      }
    ]
  }
}
```

### Limitations

- A workflow performs multiple IG requests and does not provide a transactional snapshot.
- Returned resources depend on the active account and may change between requests.
- The three reads are sequential and therefore not an atomic point-in-time snapshot.

### Exceptions

| Exception | Trigger | Recovery |
| --- | --- | --- |
| `AuthenticationError` | IG rejected the credentials, required session values were absent, or refresh failed. | Re-authenticate with valid credentials before retrying. |
| `AuthorizationError` | The active account cannot access the requested resource or action. | Switch to an entitled account or request the required IG permission. |
| `RateLimitError` | IG rejected the request because an allowance was exhausted. | Wait for `retry_after_seconds` when present, then retry with bounded backoff. |
| `ProviderRejectionError` | IG rejected an otherwise well-formed request. | Inspect `error_code` and correct the provider-specific input or account state. |
| `ResourceNotFoundError` | The requested provider resource does not exist or is inaccessible. | Verify the identifier and active account before retrying. |
| `TransportError` | A network or timeout failure prevented a completed read request. | Retry the idempotent read with bounded backoff. |
| `ValidationError` | Request construction failed or an IG response did not match the declared model. | Correct invalid request fields; report provider response drift with redacted diagnostics. |
