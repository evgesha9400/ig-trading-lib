<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Discovery workflows

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.workflows.discovery.find_market()`

Search for an exact epic and then retrieve its market details.

Official IG reference: [https://labs.ig.com/reference/markets-searchterm.html](https://labs.ig.com/reference/markets-searchterm.html)

### Signatures

- Sync: `(search_term: 'str', epic: 'str') -> 'MarketGetResponse'`
- Async: `(search_term: 'str', epic: 'str') -> 'MarketGetResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `search_term` | `str` | required | - | Text matched against IG market names and identifiers. |
| `epic` | `str` | required | - | IG market epic. |

### Sync example

```python
result = ig.workflows.discovery.find_market(search_term="EUR/USD", epic="CS.D.EURUSD.CFD.IP")
```

### Async example

```python
result = await ig.workflows.discovery.find_market(search_term="EUR/USD", epic="CS.D.EURUSD.CFD.IP")
```

### Response shape: `MarketGetResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `instrument` | `MarketInstrument` | required |
| `instrument.chart_code` | `str | None` | default: `None` |
| `instrument.contract_size` | `str | None` | default: `None` |
| `instrument.country` | `str | None` | default: `None` |
| `instrument.currencies[]` | `tuple[MarketCurrency, ...]` | default: `()` |
| `instrument.currencies[].base_exchange_rate` | `Decimal | None` | default: `None` |
| `instrument.currencies[].code` | `str` | required |
| `instrument.currencies[].exchange_rate` | `Decimal | None` | default: `None` |
| `instrument.currencies[].is_default` | `bool | None` | default: `None` |
| `instrument.currencies[].symbol` | `str | None` | default: `None` |
| `instrument.epic` | `str` | required |
| `instrument.expiry` | `str | None` | default: `None` |
| `instrument.limited_risk_premium` | `MarketDistanceRule | None` | default: `None` |
| `instrument.limited_risk_premium.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `instrument.limited_risk_premium.value` | `Decimal` | required |
| `instrument.lot_size` | `Decimal | None` | default: `None` |
| `instrument.market_id` | `str | None` | default: `None` |
| `instrument.name` | `str | None` | default: `None` |
| `instrument.news_code` | `str | None` | default: `None` |
| `instrument.streaming_prices_available` | `bool | None` | default: `None` |
| `instrument.limit_allowed` | `bool | None` | default: `None` |
| `instrument.stop_allowed` | `bool | None` | default: `None` |
| `instrument.type` | `str | None` | default: `None` |
| `instrument.unit` | `str | None` | default: `None` |
| `instrument.value_of_one_pip` | `str | None` | default: `None` |
| `snapshot` | `MarketSnapshot | None` | default: `None` |
| `snapshot.decimal_places_factor` | `int | None` | default: `None` |
| `snapshot.delay_time` | `int | None` | default: `None` |
| `snapshot.high` | `Decimal | None` | default: `None` |
| `snapshot.low` | `Decimal | None` | default: `None` |
| `snapshot.market_status` | `str | None` | default: `None` |
| `snapshot.net_change` | `Decimal | None` | default: `None` |
| `snapshot.percentage_change` | `Decimal | None` | default: `None` |
| `snapshot.scaling_factor` | `Decimal | None` | default: `None` |
| `snapshot.update_timestamp_utc` | `int | None` | default: `None` |
| `snapshot.price_ladder[]` | `tuple[MarketPriceLadderEntry, ...]` | default: `()` |
| `snapshot.price_ladder[].bid` | `Decimal` | required |
| `snapshot.price_ladder[].ask` | `Decimal` | required |
| `snapshot.currency_ladders[]` | `tuple[MarketCurrencyLadder, ...]` | default: `()` |
| `snapshot.currency_ladders[].currency` | `str` | required |
| `snapshot.currency_ladders[].bid_sizes[]` | `tuple[Decimal, ...]` | default: `()` |
| `snapshot.currency_ladders[].ask_sizes[]` | `tuple[Decimal, ...]` | default: `()` |
| `dealing_rules` | `MarketDealingRules | None` | default: `None` |
| `dealing_rules.controlled_risk_spacing` | `MarketDistanceRule | None` | default: `None` |
| `dealing_rules.controlled_risk_spacing.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `dealing_rules.controlled_risk_spacing.value` | `Decimal` | required |
| `dealing_rules.max_stop_or_limit_distance` | `MarketDistanceRule | None` | default: `None` |
| `dealing_rules.max_stop_or_limit_distance.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `dealing_rules.max_stop_or_limit_distance.value` | `Decimal` | required |
| `dealing_rules.min_controlled_risk_stop_distance` | `MarketDistanceRule | None` | default: `None` |
| `dealing_rules.min_controlled_risk_stop_distance.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `dealing_rules.min_controlled_risk_stop_distance.value` | `Decimal` | required |
| `dealing_rules.min_deal_size` | `MarketDistanceRule | None` | default: `None` |
| `dealing_rules.min_deal_size.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `dealing_rules.min_deal_size.value` | `Decimal` | required |
| `dealing_rules.min_normal_stop_or_limit_distance` | `MarketDistanceRule | None` | default: `None` |
| `dealing_rules.min_normal_stop_or_limit_distance.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `dealing_rules.min_normal_stop_or_limit_distance.value` | `Decimal` | required |
| `dealing_rules.min_step_distance` | `MarketDistanceRule | None` | default: `None` |
| `dealing_rules.min_step_distance.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `dealing_rules.min_step_distance.value` | `Decimal` | required |
| `dealing_rules.trailing_stops_preference` | `str | None` | default: `None` |

### Response example

```json
{
  "instrument": {
    "chart_code": "example",
    "contract_size": "example",
    "country": "example",
    "currencies": [
      {
        "base_exchange_rate": "1.0",
        "code": "example",
        "exchange_rate": "1.0",
        "is_default": true,
        "symbol": "example"
      }
    ],
    "epic": "CS.D.EURUSD.CFD.IP",
    "expiry": "-",
    "limited_risk_premium": {
      "unit": "PERCENTAGE",
      "value": "1.0"
    },
    "lot_size": "1.0",
    "market_id": "EURUSD",
    "name": "Example",
    "news_code": "example",
    "streaming_prices_available": true,
    "limit_allowed": true,
    "stop_allowed": true,
    "type": "example",
    "unit": "example",
    "value_of_one_pip": "example"
  },
  "snapshot": {
    "decimal_places_factor": 1,
    "delay_time": 1,
    "high": "1.0",
    "low": "1.0",
    "market_status": "TRADEABLE",
    "net_change": "1.0",
    "percentage_change": "1.0",
    "scaling_factor": "1.0",
    "update_timestamp_utc": 1,
    "price_ladder": [
      {
        "bid": "1.0",
        "ask": "1.0"
      }
    ],
    "currency_ladders": [
      {
        "currency": "GBP",
        "bid_sizes": [
          "1.0"
        ],
        "ask_sizes": [
          "1.0"
        ]
      }
    ]
  },
  "dealing_rules": {
    "controlled_risk_spacing": {
      "unit": "PERCENTAGE",
      "value": "1.0"
    },
    "max_stop_or_limit_distance": {
      "unit": "PERCENTAGE",
      "value": "1.0"
    },
    "min_controlled_risk_stop_distance": {
      "unit": "PERCENTAGE",
      "value": "1.0"
    },
    "min_deal_size": {
      "unit": "PERCENTAGE",
      "value": "1.0"
    },
    "min_normal_stop_or_limit_distance": {
      "unit": "PERCENTAGE",
      "value": "1.0"
    },
    "min_step_distance": {
      "unit": "PERCENTAGE",
      "value": "1.0"
    },
    "trailing_stops_preference": "example"
  }
}
```

### Limitations

- A workflow performs multiple IG requests and does not provide a transactional snapshot.
- Returned resources depend on the active account and may change between requests.
- The exact epic must appear in the search results before details are fetched.

### Exceptions

| Exception | Trigger | Recovery |
| --- | --- | --- |
| `AuthenticationError` | IG rejected the credentials, required session values were absent, or refresh failed. | Re-authenticate with valid credentials before retrying. |
| `AuthorizationError` | The active account cannot access the requested resource or action. | Switch to an entitled account or request the required IG permission. |
| `RateLimitError` | IG rejected the request because an allowance was exhausted. | Wait for `retry_after_seconds` when present, then retry with bounded backoff. |
| `ProviderRejectionError` | IG rejected an otherwise well-formed request. | Inspect `error_code` and correct the provider-specific input or account state. |
| `ResourceNotFoundError` | Search completed but did not contain the requested exact `epic`. | Verify the identifier and active account before retrying. |
| `TransportError` | A network or timeout failure prevented a completed read request. | Retry the idempotent read with bounded backoff. |
| `ValidationError` | Request construction failed or an IG response did not match the declared model. | Correct invalid request fields; report provider response drift with redacted diagnostics. |
