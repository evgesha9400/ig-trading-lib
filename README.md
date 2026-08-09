# IG Trading Library v3

Safe, typed synchronous and asynchronous IG REST and streaming clients.

[Documentation](https://evgesha9400.github.io/ig-trading-lib/latest/) ·
[Source](https://github.com/evgesha9400/ig-trading-lib) ·
[PyPI](https://pypi.org/project/ig-trading-lib/)

## Install

```bash
pip install ig-trading-lib
```

Python 3.11–3.13 is supported.

## Market operations and discovery

The new composition roots expose two behavioral namespaces: `operations` for one provider
operation and `workflows` for safe multi-operation composition.

```python
from ig_trading_lib import Environment, IG, IGConfig, SessionCredentials

config = IGConfig(
    environment=Environment.DEMO,
    credentials=SessionCredentials(
        api_key="…",
        identifier="…",
        password="…",
    ),
)

with IG(config) as ig:
    matches = ig.operations.markets.search(search_term="EURUSD")
    details = ig.operations.markets.get(epic=matches.markets[0].epic)
    selected = ig.workflows.discovery.find_market(
        search_term="EURUSD",
        epic="CS.D.EURUSD.TODAY.IP",
    )
```

`AsyncIG` has the same names, arguments, and result models; only the three calls are awaited.
Search and detail responses type known market fields while retaining additional provider fields.

## Start safely

Use a demo account while building an agent. Credentials are explicit, immutable objects and are redacted from representations and error diagnostics.

```python
from ig_trading_lib import Environment, IGClient, IGConfig, SessionCredentials

config = IGConfig(
    environment=Environment.DEMO,
    credentials=SessionCredentials(
        api_key="…",
        identifier="…",
        password="…",
    ),
)

with IGClient(config) as client:
    markets = client.markets.search("EURUSD")
    for market in markets.items:
        print(market.epic, market.market_status)
```

The synchronous and asynchronous clients expose matching service namespaces:

| Sync | Async |
| --- | --- |
| `IGClient(config)` | `AsyncIGClient(config)` |
| `client.markets.search("EURUSD")` | `await client.markets.search("EURUSD")` |
| `client.positions.list()` | `await client.positions.list()` |
| `client.positions.create(...)` | `await client.positions.create(...)` |

```python
from ig_trading_lib import AsyncIGClient

async with AsyncIGClient(config) as client:
    accounts = await client.accounts.list()
    print(accounts.items)
```

## Live-trading boundary

Guarded live mutations require an explicit permit in addition to `Environment.LIVE`. A missing permit fails before authentication or network I/O.

```python
from ig_trading_lib import Environment, IGClient, IGConfig, TradingPermit

live_config = IGConfig(environment=Environment.LIVE, credentials=config.credentials)
client = IGClient(live_config, trading_permit=TradingPermit())

# Position create, update, and close operations are guarded.
client.positions.create({"epic": "CS.D.EURUSD.TODAY.IP", "direction": "BUY", "size": "1"})
```

The guarded typed surfaces are `positions.create`, `positions.update`, `positions.close`, `accounts.update_preferences`, and mutation methods on `watchlists`, `working_orders`, `costs`, and `applications`. `ResourceClient` instances without a guard are not covered by this boundary.

Do not retry a failed mutation yourself. The client raises `AmbiguousExecutionError` when a network failure means IG may have accepted it; resolve that outcome with the deal reference or a confirmation before issuing another order.

## REST services

Canonical services normalise provider keys to `snake_case` and paginate with `Page` plus lazy `iter_pages` / async `iter_pages` methods.

```python
with IGClient(config) as client:
    for activity in client.activity.iter_pages(item_key="activities"):
        print(activity)

    position = client.positions.get("DEAL_ID")
    confirmation = client.confirms.get("/DEAL_REFERENCE")
```

The endpoint catalog is maintained in `ig_trading_lib.endpoint_catalog` and contract-tested against the maintained `DOCUMENTED_ENDPOINTS` catalog.

## Streaming

Streaming is lazy: no Lightstreamer session is opened until iteration begins. IG requires CST/XST security tokens even for OAuth users; the client obtains them when needed, preserves subscriptions during SDK recovery, and exposes terminal stream errors instead of silently dropping data.

```python
from ig_trading_lib import StreamSubscription

subscription = StreamSubscription(
    key="eurusd",
    mode="MERGE",
    items=("MARKET:CS.D.EURUSD.TODAY.IP",),
    fields=("BID", "OFFER", "UPDATE_TIME"),
)

with IGClient(config) as client:
    updates = client.streaming.iter_updates(subscription)
    try:
        for update in updates:
            print(update.item_name, update.changed_fields)
    finally:
        updates.close()
```

```python
async with AsyncIGClient(config) as client:
    async for update in client.streaming.aiter_updates(subscription):
        print(update.changed_fields)
```

## Errors and observability

Operational failures derive from `IGError`. Errors carry a safe provider request ID, a client operation ID, retry timing when supplied by IG, and redacted details. `LiveTradingPermissionError` is a separate `PermissionError` raised by the live-mutation guard.

```python
from ig_trading_lib import AmbiguousExecutionError, RateLimitError, TransportError

try:
    client.markets.search("EURUSD")
except RateLimitError as error:
    print(error.retry_after_seconds)
except TransportError as error:
    print(error.operation_id)
except AmbiguousExecutionError as error:
    print("Resolve the deal outcome before retrying", error.operation_id)
```

Successful requests emit `ig.http.response` through the `ig_trading_lib.transport` standard-library logger. The structured record includes method, path, status, retry count, provider request ID, and client operation ID; passwords and tokens are never logged.

## Tests and development

```bash
poetry sync --with dev
poetry run pytest tests/unit/v3
poetry run ruff format --check src tests scripts examples
poetry run ruff check src tests scripts examples
poetry run pyright
poetry run python scripts/check_documentation_contract.py
poetry run mkdocs build --strict
poetry run playwright install chromium
poetry export --only main --without-hashes --output /tmp/ig-trading-lib-requirements.txt
poetry run pip-audit --strict --requirement /tmp/ig-trading-lib-requirements.txt
poetry build
```

The default test suite is deterministic and has no IG network dependency. Demo integration runs are deliberately separate and must be invoked only with explicit credentials and opt-in approval. Never store credentials in the repository.

## Versioned releases

Documentation and packages are validated on pull requests, `main`, and `develop`, but those runs never publish release artifacts. Publishing is restricted to a pushed SemVer tag beginning with `v`.

| Tag | Published documentation | `latest` and root redirect |
| --- | --- | --- |
| `v3.0.0` | `https://evgesha9400.github.io/ig-trading-lib/3.0.0/` | Updated to `3.0.0` |
| `v3.1.0-rc.1` | `https://evgesha9400.github.io/ig-trading-lib/3.1.0-rc.1/` | Unchanged |

Each versioned site is immutable: a tagged workflow rejects an existing version before `mike` deploys it. Publish a corrected release under a new SemVer tag instead of changing published documentation.

If a tagged run partially succeeds, maintainers may use the manual `release_tag` recovery input. The workflow verifies documentation provenance, retains existing immutable Pages content, skips existing PyPI artifacts only during explicit recovery, and completes the remaining release steps.

```bash
git tag -a v3.0.1 -m "Release v3.0.1"
git push origin v3.0.1
```

The tagged workflow publishes immutable documentation, uploads the validated package to PyPI, creates the GitHub Release record, and dispatches `evgesha9400/evgesha9400.github.io`'s `rebuild-library-pages.yml` workflow. Configure `PYPI_API_TOKEN` for package publication and `LIBRARY_PORTAL_DISPATCH_TOKEN` for the portal hand-off.

## Disclaimer

This project is not affiliated with IG. Trading involves material risk. Review IG’s [REST reference](https://labs.ig.com/rest-trading-api-reference.html), [REST guide](https://labs.ig.com/rest-trading-api-guide.html), and [streaming guide](https://labs.ig.com/streaming-api-guide.html) before connecting an agent to an account.
