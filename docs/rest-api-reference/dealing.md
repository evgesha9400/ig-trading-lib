# Dealing

Position methods are typed convenience operations. Working orders use the generic typed `ResourceClient` surface. In both cases, order bodies are IG provider-defined mappings, so validate business constraints before sending one.

## Positions

`positions.list()` and `positions.get(deal_id)` are reads. `positions.create(request)`, `positions.update(deal_id, request)`, and `positions.close(request)` are guarded mutations. A live mutation needs a client constructed with `TradingPermit()`.

```python
with IGClient(config, trading_permit=TradingPermit()) as client:
    response = client.positions.create(
        {"epic": "CS.D.EURUSD.TODAY.IP", "direction": "BUY", "size": "1"}
    )
    deal_reference = response.deal_reference
```

The example body is only a provider mapping shape, not a claim that those fields are sufficient for every IG market or account. Preserve the returned deal reference and read a confirmation before treating a mutation as final.

## Working orders

`client.working_orders` is guarded on the built-in client. Its generic `create`, `update`, and `delete` methods accept a caller-selected suffix, so an OTC request can be explicit:

```python
with IGClient(config, trading_permit=TradingPermit()) as client:
    response = client.working_orders.create(provider_request, suffix="/otc")
```

Do not generalise this guard to every `ResourceClient`: only selected typed client attributes install a guard. The exact scope is documented in [trading safety](../api-guide/trading-safety.md).

## Confirmations and repeat-dealing windows

`client.confirms.get(f"/{deal_reference}")` reads a deal confirmation when a stream confirmation was not received. Retain the deal reference from every mutation; it is the correlation value used to establish an uncertain outcome.

`client.repeat_dealing_window.get()` reads the active repeat-dealing status. Provider response fields remain IG-controlled mappings.

After `AmbiguousExecutionError`, do not send the dealing request again. Use the deal reference, a confirmation, or a relevant read to establish the result. The [confirmation recipe](../recipes/index.md#confirmation-handling) is tested for this recovery path.

--8<-- "docs/rest-api-reference/.dealing-endpoints.md"
