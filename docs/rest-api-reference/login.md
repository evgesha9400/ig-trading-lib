# Login

The client establishes and refreshes its session lazily from `IGConfig`. Use [Authentication and authorisation](../api-guide/authentication-and-authorisation.md) to choose the legacy session or OAuth credential flow; application code should not construct session headers or persist tokens itself.

## Session and active account operations

`client.session` gives typed access to provider session reads and account selection. The transport continues to own normal authentication and token refresh.

Do not log session tokens or raw provider credentials.

--8<-- "docs/rest-api-reference/.login-endpoints.md"
