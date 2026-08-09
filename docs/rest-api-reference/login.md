# Session operations

The transport authenticates lazily from `IGConfig` and owns token refresh. Use
`ig.operations.session` only for explicit session reads, account switching, encryption keys, or
refresh-token operations. Never log provider credentials or tokens.

--8<-- "docs/rest-api-reference/.login-endpoints.md"
