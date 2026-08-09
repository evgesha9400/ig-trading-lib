<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Markets operations

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.markets.list()`

Retrieve details for up to 50 market epics.

Official IG reference: [https://labs.ig.com/reference/markets.html](https://labs.ig.com/reference/markets.html)

### Signatures

- Sync: `(epics: 'tuple[str, ...]', *, filter: "Literal['ALL', 'SNAPSHOT_ONLY']" = 'ALL') -> 'MarketsResponse'`
- Async: `(epics: 'tuple[str, ...]', *, filter: "Literal['ALL', 'SNAPSHOT_ONLY']" = 'ALL') -> 'MarketsResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `epics` | `tuple[str, ...]` | required | - | Ordered collection of IG market epics. |
| `filter` | `Literal['ALL', 'SNAPSHOT_ONLY']` | 'ALL' | - | Provider filter controlling the records or market detail returned. |

### Sync example

```python
result = ig.operations.markets.list(epics=("CS.D.EURUSD.CFD.IP",), filter="ALL")
```

### Async example

```python
result = await ig.operations.markets.list(epics=("CS.D.EURUSD.CFD.IP",), filter="ALL")
```

### Response shape: `MarketsResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `market_details[]` | `tuple[MarketDetails, ...]` | default: `()` |
| `market_details[].dealing_rules` | `DetailedMarketDealingRules` | required |
| `market_details[].dealing_rules.controlled_risk_spacing` | `MarketDistanceRule | None` | default: `None` |
| `market_details[].dealing_rules.controlled_risk_spacing.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `market_details[].dealing_rules.controlled_risk_spacing.value` | `Decimal` | required |
| `market_details[].dealing_rules.max_stop_or_limit_distance` | `MarketDistanceRule | None` | default: `None` |
| `market_details[].dealing_rules.max_stop_or_limit_distance.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `market_details[].dealing_rules.max_stop_or_limit_distance.value` | `Decimal` | required |
| `market_details[].dealing_rules.min_controlled_risk_stop_distance` | `MarketDistanceRule | None` | default: `None` |
| `market_details[].dealing_rules.min_controlled_risk_stop_distance.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `market_details[].dealing_rules.min_controlled_risk_stop_distance.value` | `Decimal` | required |
| `market_details[].dealing_rules.min_deal_size` | `MarketDistanceRule | None` | default: `None` |
| `market_details[].dealing_rules.min_deal_size.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `market_details[].dealing_rules.min_deal_size.value` | `Decimal` | required |
| `market_details[].dealing_rules.min_normal_stop_or_limit_distance` | `MarketDistanceRule | None` | default: `None` |
| `market_details[].dealing_rules.min_normal_stop_or_limit_distance.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `market_details[].dealing_rules.min_normal_stop_or_limit_distance.value` | `Decimal` | required |
| `market_details[].dealing_rules.min_step_distance` | `MarketDistanceRule | None` | default: `None` |
| `market_details[].dealing_rules.min_step_distance.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `market_details[].dealing_rules.min_step_distance.value` | `Decimal` | required |
| `market_details[].dealing_rules.trailing_stops_preference` | `str | None` | default: `None` |
| `market_details[].dealing_rules.market_order_preference` | `str | None` | default: `None` |
| `market_details[].instrument` | `DetailedMarketInstrument` | required |
| `market_details[].instrument.chart_code` | `str | None` | default: `None` |
| `market_details[].instrument.contract_size` | `str | None` | default: `None` |
| `market_details[].instrument.country` | `str | None` | default: `None` |
| `market_details[].instrument.currencies[]` | `tuple[MarketCurrency, ...]` | default: `()` |
| `market_details[].instrument.currencies[].base_exchange_rate` | `Decimal | None` | default: `None` |
| `market_details[].instrument.currencies[].code` | `str` | required |
| `market_details[].instrument.currencies[].exchange_rate` | `Decimal | None` | default: `None` |
| `market_details[].instrument.currencies[].is_default` | `bool | None` | default: `None` |
| `market_details[].instrument.currencies[].symbol` | `str | None` | default: `None` |
| `market_details[].instrument.epic` | `str` | required |
| `market_details[].instrument.expiry` | `str | None` | default: `None` |
| `market_details[].instrument.limited_risk_premium` | `MarketDistanceRule | None` | default: `None` |
| `market_details[].instrument.limited_risk_premium.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `market_details[].instrument.limited_risk_premium.value` | `Decimal` | required |
| `market_details[].instrument.lot_size` | `Decimal | None` | default: `None` |
| `market_details[].instrument.market_id` | `str | None` | default: `None` |
| `market_details[].instrument.name` | `str | None` | default: `None` |
| `market_details[].instrument.news_code` | `str | None` | default: `None` |
| `market_details[].instrument.streaming_prices_available` | `bool | None` | default: `None` |
| `market_details[].instrument.limit_allowed` | `bool | None` | default: `None` |
| `market_details[].instrument.stop_allowed` | `bool | None` | default: `None` |
| `market_details[].instrument.type` | `str | None` | default: `None` |
| `market_details[].instrument.unit` | `str | None` | default: `None` |
| `market_details[].instrument.value_of_one_pip` | `str | None` | default: `None` |
| `market_details[].instrument.controlled_risk_allowed` | `bool | None` | default: `None` |
| `market_details[].instrument.expiry_details` | `MarketExpiryDetails | None` | default: `None` |
| `market_details[].instrument.expiry_details.last_dealing_date` | `str | None` | default: `None` |
| `market_details[].instrument.expiry_details.settlement_info` | `str | None` | default: `None` |
| `market_details[].instrument.force_open_allowed` | `bool | None` | default: `None` |
| `market_details[].instrument.margin_deposit_bands[]` | `tuple[MarketMarginDepositBand, ...]` | default: `()` |
| `market_details[].instrument.margin_deposit_bands[].currency` | `str | None` | default: `None` |
| `market_details[].instrument.margin_deposit_bands[].margin` | `Decimal | None` | default: `None` |
| `market_details[].instrument.margin_deposit_bands[].max` | `Decimal | None` | default: `None` |
| `market_details[].instrument.margin_deposit_bands[].min` | `Decimal | None` | default: `None` |
| `market_details[].instrument.margin_factor` | `Decimal | None` | default: `None` |
| `market_details[].instrument.margin_factor_unit` | `Literal['PERCENTAGE', 'POINTS'] | None` | default: `None` |
| `market_details[].instrument.one_pip_means` | `str | None` | default: `None` |
| `market_details[].instrument.opening_hours` | `MarketOpeningHours | None` | default: `None` |
| `market_details[].instrument.opening_hours.market_times[]` | `tuple[MarketTime, ...]` | default: `()` |
| `market_details[].instrument.opening_hours.market_times[].close_time` | `str | None` | default: `None` |
| `market_details[].instrument.opening_hours.market_times[].open_time` | `str | None` | default: `None` |
| `market_details[].instrument.rollover_details` | `MarketRolloverDetails | None` | default: `None` |
| `market_details[].instrument.rollover_details.last_rollover_time` | `str | None` | default: `None` |
| `market_details[].instrument.rollover_details.rollover_info` | `str | None` | default: `None` |
| `market_details[].instrument.slippage_factor` | `MarketDistanceRule | None` | default: `None` |
| `market_details[].instrument.slippage_factor.unit` | `Literal['PERCENTAGE', 'POINTS']` | required |
| `market_details[].instrument.slippage_factor.value` | `Decimal` | required |
| `market_details[].instrument.special_info[]` | `tuple[str, ...]` | default: `()` |
| `market_details[].instrument.sprint_markets_maximum_expiry_time` | `int | None` | default: `None` |
| `market_details[].instrument.sprint_markets_minimum_expiry_time` | `int | None` | default: `None` |
| `market_details[].instrument.stops_limits_allowed` | `bool | None` | default: `None` |
| `market_details[].snapshot` | `DetailedMarketSnapshot` | required |
| `market_details[].snapshot.decimal_places_factor` | `int | None` | default: `None` |
| `market_details[].snapshot.delay_time` | `int | None` | default: `None` |
| `market_details[].snapshot.high` | `Decimal | None` | default: `None` |
| `market_details[].snapshot.low` | `Decimal | None` | default: `None` |
| `market_details[].snapshot.market_status` | `str | None` | default: `None` |
| `market_details[].snapshot.net_change` | `Decimal | None` | default: `None` |
| `market_details[].snapshot.percentage_change` | `Decimal | None` | default: `None` |
| `market_details[].snapshot.scaling_factor` | `Decimal | None` | default: `None` |
| `market_details[].snapshot.update_timestamp_utc` | `int | None` | default: `None` |
| `market_details[].snapshot.price_ladder[]` | `tuple[MarketPriceLadderEntry, ...]` | default: `()` |
| `market_details[].snapshot.price_ladder[].bid` | `Decimal` | required |
| `market_details[].snapshot.price_ladder[].ask` | `Decimal` | required |
| `market_details[].snapshot.currency_ladders[]` | `tuple[MarketCurrencyLadder, ...]` | default: `()` |
| `market_details[].snapshot.currency_ladders[].currency` | `str` | required |
| `market_details[].snapshot.currency_ladders[].bid_sizes[]` | `tuple[Decimal, ...]` | default: `()` |
| `market_details[].snapshot.currency_ladders[].ask_sizes[]` | `tuple[Decimal, ...]` | default: `()` |
| `market_details[].snapshot.bid` | `Decimal | None` | default: `None` |
| `market_details[].snapshot.binary_odds` | `Decimal | None` | default: `None` |
| `market_details[].snapshot.controlled_risk_extra_spread` | `Decimal | None` | default: `None` |
| `market_details[].snapshot.offer` | `Decimal | None` | default: `None` |
| `market_details[].snapshot.update_time` | `str | None` | default: `None` |

### Response example

```json
{
  "market_details": [
    {
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
        "trailing_stops_preference": "example",
        "market_order_preference": "example"
      },
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
        "value_of_one_pip": "example",
        "controlled_risk_allowed": true,
        "expiry_details": {
          "last_dealing_date": "example",
          "settlement_info": "example"
        },
        "force_open_allowed": true,
        "margin_deposit_bands": [
          {
            "currency": "GBP",
            "margin": "1.0",
            "max": "1.0",
            "min": "1.0"
          }
        ],
        "margin_factor": "1.0",
        "margin_factor_unit": "PERCENTAGE",
        "one_pip_means": "example",
        "opening_hours": {
          "market_times": [
            {
              "close_time": "example",
              "open_time": "example"
            }
          ]
        },
        "rollover_details": {
          "last_rollover_time": "example",
          "rollover_info": "example"
        },
        "slippage_factor": {
          "unit": "PERCENTAGE",
          "value": "1.0"
        },
        "special_info": [
          "example"
        ],
        "sprint_markets_maximum_expiry_time": 1,
        "sprint_markets_minimum_expiry_time": 1,
        "stops_limits_allowed": true
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
        ],
        "bid": "1.0",
        "binary_odds": "1.0",
        "controlled_risk_extra_spread": "1.0",
        "offer": "1.0",
        "update_time": "12:34:56"
      }
    }
  ]
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- `epics` must contain 1-50 non-empty identifiers; `SNAPSHOT_ONLY` returns reduced detail.

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
| `ValueError` | `epics` is empty, exceeds 50 items, or contains an empty identifier. | Correct the argument before calling IG again. |

## `ig.operations.markets.search()`

Search for markets by name or identifier.

Official IG reference: [https://labs.ig.com/reference/markets-searchterm.html](https://labs.ig.com/reference/markets-searchterm.html)

### Signatures

- Sync: `(search_term: 'str') -> 'MarketSearchResponse'`
- Async: `(search_term: 'str') -> 'MarketSearchResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `search_term` | `str` | required | - | Text matched against IG market names and identifiers. |

### Sync example

```python
result = ig.operations.markets.search(search_term="EUR/USD")
```

### Async example

```python
result = await ig.operations.markets.search(search_term="EUR/USD")
```

### Response shape: `MarketSearchResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `markets[]` | `tuple[MarketSummary, ...]` | required |
| `markets[].bid` | `Decimal | None` | default: `None` |
| `markets[].delay_time` | `int | None` | default: `None` |
| `markets[].epic` | `str` | required |
| `markets[].expiry` | `str | None` | default: `None` |
| `markets[].high` | `Decimal | None` | default: `None` |
| `markets[].instrument_name` | `str | None` | default: `None` |
| `markets[].instrument_type` | `str | None` | default: `None` |
| `markets[].low` | `Decimal | None` | default: `None` |
| `markets[].market_status` | `str | None` | default: `None` |
| `markets[].net_change` | `Decimal | None` | default: `None` |
| `markets[].offer` | `Decimal | None` | default: `None` |
| `markets[].percentage_change` | `Decimal | None` | default: `None` |
| `markets[].scaling_factor` | `Decimal | None` | default: `None` |
| `markets[].streaming_prices_available` | `bool | None` | default: `None` |
| `markets[].update_time` | `str | None` | default: `None` |
| `markets[].update_time_utc` | `str | None` | default: `None` |

### Response example

```json
{
  "markets": [
    {
      "epic": "CS.D.EURUSD.CFD.IP",
      "instrumentName": "EUR/USD",
      "marketStatus": "TRADEABLE",
      "bid": "1.08120",
      "offer": "1.08135"
    }
  ]
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- `search_term` must contain at least one non-whitespace character.

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
| `ValueError` | `search_term` is empty or contains only whitespace. | Correct the argument before calling IG again. |

## `ig.operations.markets.get()`

Retrieve details, snapshot, and dealing rules for one market epic.

Official IG reference: [https://labs.ig.com/reference/markets-epic.html](https://labs.ig.com/reference/markets-epic.html)

### Signatures

- Sync: `(epic: 'str') -> 'MarketGetResponse'`
- Async: `(epic: 'str') -> 'MarketGetResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `epic` | `str` | required | - | IG market epic. |

### Sync example

```python
result = ig.operations.markets.get(epic="CS.D.EURUSD.CFD.IP")
```

### Async example

```python
result = await ig.operations.markets.get(epic="CS.D.EURUSD.CFD.IP")
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

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- `epic` must contain at least one non-whitespace character.

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
| `ValueError` | `epic` is empty or contains only whitespace. | Correct the argument before calling IG again. |
