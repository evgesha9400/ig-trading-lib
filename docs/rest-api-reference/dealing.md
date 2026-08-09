# Dealing operations

Dealing requests are typed. The faithful layer exposes positions, working orders, confirmations,
and repeat-dealing windows. The workflow layer composes mutations with confirmation reads.

```python
with IG(config, trading_permit=TradingPermit()) as ig:
    result = ig.operations.positions.create(request)
    confirmation = ig.operations.confirmations.get(result.deal_reference)
```

The equivalent journey is `ig.workflows.positions.open_and_confirm(request)`. After
`AmbiguousExecutionError`, reconcile using the deal reference or account state before another
mutation.

--8<-- "docs/rest-api-reference/.dealing-endpoints.md"
