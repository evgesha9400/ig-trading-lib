# Migrating from v2 to v3

v3 is a clean major release. The old `authentication`, `trading`, `account`, and `markets` packages are intentionally removed; there are no runtime compatibility aliases.

| v2 concept | v3 replacement |
| --- | --- |
| `AuthenticationService` | `IGConfig` with `SessionCredentials` or `OAuthCredentials` |
| Legacy HTTP client | `IGClient` or `AsyncIGClient` |
| Camel-case request models | Plain mappings at the version facade or canonical snake-case response models |
| Cached local tokens | Client-lifetime, in-memory tokens with OAuth refresh single-flight |
| Direct order service calls | `client.positions`, `client.working_orders`, or explicit `client.v1`–`client.v4` facades |
| Implicit live access | `Environment.LIVE` plus `TradingPermit()` |

## Authentication

```python
# v2: AuthenticationService(...).authenticate()

# v3
config = IGConfig(
    environment=Environment.DEMO,
    credentials=SessionCredentials(api_key="…", identifier="…", password="…"),
)
client = IGClient(config)
```

Use `OAuthCredentials` for session v3. Refresh tokens stay in memory and are refreshed once for concurrent callers.

## Operations

```python
# v2: position_service.get_open_positions()
positions = client.positions.list()

# v2: position_service.create_position(payload)
result = client.positions.create({"epic": "…", "direction": "BUY", "size": "1"})

# Historical provider contract required
raw = client.v2.prices.get("/EPIC/MINUTE/10")
```

Check `IGError` subclasses rather than matching provider error strings. On `AmbiguousExecutionError`, query confirmations or the relevant deal reference; never submit a blind duplicate mutation.
