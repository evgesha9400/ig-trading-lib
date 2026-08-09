# Market operations

```python
with IG(config) as ig:
    matches = ig.operations.markets.search("EUR/USD")
    market = ig.operations.markets.get(matches.markets[0].epic)
    prices = ig.operations.prices.list_points(market.instrument.epic, "MINUTE", 60)
```

Categories, discovery, details, and prices are separate faithful namespaces. The discovery
workflow adds exact-epic selection without duplicating protocol knowledge.

--8<-- "docs/rest-api-reference/.markets-endpoints.md"
