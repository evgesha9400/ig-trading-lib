# Sync and async recipes

Every recipe below is source-included from `examples/recipes/` and verified with local mocked
provider responses. They never contact IG.

## Market discovery

```python title="examples/recipes/market_discovery.py"
--8<-- "examples/recipes/market_discovery.py"
```

## Activity history

```python title="examples/recipes/historical_pagination.py"
--8<-- "examples/recipes/historical_pagination.py"
```

## Safe mutations

Supply a validated `CreatePositionRequest`. For live accounts, create the root with an explicit
`TradingPermit()`; the workflow does not bypass the guard.

```python title="examples/recipes/safe_mutations.py"
--8<-- "examples/recipes/safe_mutations.py"
```

## Confirmation handling

```python title="examples/recipes/confirmation_handling.py"
--8<-- "examples/recipes/confirmation_handling.py"
```

## Streaming

```python title="examples/recipes/streaming.py"
--8<-- "examples/recipes/streaming.py"
```

## Error recovery

The retry callback only receives a safe read-retry decision. It deliberately does not retry a mutation or handle `AmbiguousExecutionError`.

```python title="examples/recipes/error_recovery.py"
--8<-- "examples/recipes/error_recovery.py"
```

## LLM and agent discovery

Load the generated index, select only an existing operation, then consult the linked public contract and conceptual guide. The helper does not create endpoints or payload schemas.

```python title="examples/recipes/agent_discovery.py"
--8<-- "examples/recipes/agent_discovery.py"
```
