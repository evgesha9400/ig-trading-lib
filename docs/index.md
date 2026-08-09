# Trading code should speak IG, not HTTP

IG Trading Library gives Python applications typed operations and safe workflows for IG's REST
and streaming APIs.

## Why use it?

- One method name maps to one maintained IG operation.
- Typed request models reject invalid shapes before network I/O.
- Typed responses expose documented fields and preserve provider additions.
- Authentication, provider protocol versions, retries, redaction, and streaming recovery are shared.
- Live mutations require an explicit `TradingPermit`.
- Uncertain mutation outcomes raise `AmbiguousExecutionError` instead of being retried blindly.

## Two layers, no competing API

```text
IG or AsyncIG
├── operations   faithful IG calls
└── workflows    safe journeys composed from operations
```

Start with [Getting started](getting-started.md), then use the REST reference to translate an IG
concept directly into `ig.operations.<resource>.<operation>()`.

Library v4 is the Python package version. Provider protocol versions are private manifest details,
not user-selectable interfaces.
