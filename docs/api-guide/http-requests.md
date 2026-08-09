# HTTP requests stay private

`IG` and `AsyncIG` own authentication, headers, timeouts, safe-read retries, rate-limit handling,
correlation IDs, and redacted diagnostics.

Application code calls `ig.operations.<resource>.<operation>()`. The private operation manifest
binds that method to one HTTP method, path template, and provider protocol version. Arbitrary
paths, suffixes, and version selectors are intentionally absent from the public API.

Safe reads may retry within `IGConfig.max_retries`. Mutations are never blindly retried after an
indeterminate network failure; they raise `AmbiguousExecutionError`.
