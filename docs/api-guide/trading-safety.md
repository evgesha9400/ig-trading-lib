# Trading safety

`Environment.DEMO` is the default place to develop an integration. Credentials and token values are redacted from supported diagnostic representations.

## Live-trading permit

`TradingPermit()` is an explicit acknowledgement for a live account; it is not required for demo work.

Guarded typed mutations are positions.create, positions.update, positions.close, accounts.update_preferences, and create, update, or delete on watchlists, working_orders, costs, and applications.

Do not infer that every ResourceClient mutation is guarded: guards are installed only for the typed client attributes named above.

## Incomplete mutation outcomes

Network failure during a mutation can raise `AmbiguousExecutionError`, because IG may have received the request even though the client cannot prove its outcome.

After AmbiguousExecutionError, verify the outcome with a confirmation or relevant deal reference before considering another mutation.

## Error hierarchy

`IGError` is the base class for provider, authentication, transport, rate-limit, streaming, and ambiguous-execution errors. `LiveTradingPermissionError` is a separate `PermissionError`; it is not an `IGError` subclass.
