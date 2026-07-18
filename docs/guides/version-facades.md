# v1 through v4 façades

`client.v1`, `client.v2`, `client.v3`, and `client.v4` expose exact-version resource namespaces. Their asynchronous equivalents have the same raw request shape.

## What they provide

Each namespace provides generic resources such as `markets`, `prices`, `positions`, `confirms`, and `session`, plus `request(method, path, ...)`. They preserve the provider response payload instead of normalising it to `IGModel`.

```python
with IGClient(config) as client:
    market = client.v4.markets.get("/CS.D.EURUSD.TODAY.IP")
    prices = client.v2.prices.get("/CS.D.EURUSD.TODAY.IP/MINUTE/10")
```

## What they do not provide

These are generic route helpers, not separate semantic implementations for every endpoint catalog row. Do not infer a dedicated method, payload schema, parameter validation, or current provider availability from a facade attribute. Consult the [endpoint matrix](../reference/endpoint-matrix.md) for the maintained route/version catalog and IG's provider documentation for request bodies.

## Live boundary

Every `POST`, `PUT`, and `DELETE` through a version façade checks `TradingPermit` for a live account. This applies to `request()` and to generic resource mutations. It does not make a provider body safe or guarantee that IG accepted it.
