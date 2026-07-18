# Credentials and environments

Create one immutable `IGConfig` for each IG environment and account context. The library does not persist credentials, session tokens, or refresh tokens to disk.

## Select an authentication flow

| Credential object | Session version | Use when |
| --- | --- | --- |
| `SessionCredentials` | v2 | Your IG application uses the legacy session flow. |
| `OAuthCredentials` | v3 | Your IG application uses the OAuth session flow. |

Both objects require `api_key`, `identifier`, and `password`. Their representations redact those values, but application code must still keep them in a secret manager or environment variables and must never commit them.

## Select an environment explicitly

`Environment.DEMO` targets IG's demo gateway and is the intended place to build and validate an integration. `Environment.LIVE` targets the live gateway. `IGConfig.account_id` is optional configuration carried by the client; confirm the active account through IG before relying on a mutation.

```python
from ig_trading_lib import Environment, IGConfig, OAuthCredentials

config = IGConfig(
    environment=Environment.DEMO,
    credentials=OAuthCredentials(
        api_key="from-secret-store",
        identifier="from-secret-store",
        password="from-secret-store",
    ),
    account_id="ABC123",
)
```

Close clients with a context manager so caller-owned network resources are released. Read [live permits](safety.md) before constructing a live client with a mutation permit.
