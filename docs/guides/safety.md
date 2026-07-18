# Safety

`Environment.DEMO` is the default place to develop an integration. Credentials and token values are redacted from supported diagnostic representations.

## Live-trading permit

`TradingPermit()` is an explicit acknowledgement for a live account; it is not required for demo work.

Guarded typed mutations are positions.create, positions.update, positions.close, accounts.update_preferences, and create, update, or delete on watchlists, working_orders, costs, and applications.

Do not infer that every ResourceClient mutation is guarded: guards are installed only for the typed client attributes named above.

## Explicit-version access

Use `client.v1` through `client.v4` when an IG operation needs an exact provider version or path that is not represented by a high-level helper. `request()` is a generic path entry point; it does not claim to provide a separate helper for every documented operation.

Every POST, PUT, or DELETE through a v1, v2, v3, or v4 VersionFacade or VersionedResource requires TradingPermit on a live account.

## Incomplete mutation outcomes

Network failure during a mutation can raise `AmbiguousExecutionError`, because IG may have received the request even though the client cannot prove its outcome.

After AmbiguousExecutionError, verify the outcome with a confirmation or relevant deal reference before considering another mutation.

## Error hierarchy

`IGError` is the base class for provider, authentication, transport, rate-limit, streaming, and ambiguous-execution errors. `LiveTradingPermissionError` is a separate `PermissionError`; it is not an `IGError` subclass.
