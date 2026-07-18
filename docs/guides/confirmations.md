# Confirmations

Mutations can return a provider deal reference. That reference is the correlation value to retain while IG finalises or rejects the deal.

## Read by deal reference

`client.confirms.get("/DEAL_REFERENCE")` uses the typed v1 confirmation resource and returns an `IGModel` with normalised keys. The provider controls its fields and lifecycle, so inspect the returned payload rather than assuming a confirmation is automatically final.

```python
with IGClient(config) as client:
    confirmation = client.confirms.get(f"/{deal_reference}")
    print(confirmation.deal_status)
```

## Resolve an uncertain mutation

`AmbiguousExecutionError` means a network failure occurred after IG may have received a mutation. Do not issue the mutation again based only on that error. Use the retained deal reference, a confirmation, or a relevant read operation to establish the outcome first.

The [confirmation recipe](../recipes/index.md#confirmation-handling) provides tested synchronous and asynchronous helpers for this lookup.
