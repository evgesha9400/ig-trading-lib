"""Offline checks for generated agent-facing documentation artifacts."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import ModuleType, SimpleNamespace

from playwright.sync_api import expect, sync_playwright
from pytest import MonkeyPatch

from scripts.generate_documentation_indexes import (
    API_INDEX_PATH,
    CLIENT_ENTRY_POINTS_PATH,
    LLMS_PATH,
    build_api_index,
    build_client_entry_points_document,
    build_llms_document,
    load_endpoint_index,
    load_public_contract,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
IG_THEME_STYLESHEET = PROJECT_ROOT / "docs" / "stylesheets" / "ig-theme.css"
LANDING_PAGE = PROJECT_ROOT / "docs" / "index.md"
GETTING_STARTED_PAGE = PROJECT_ROOT / "docs" / "getting-started.md"


class _QuietStaticHandler(SimpleHTTPRequestHandler):
    """Serve the rendered site without polluting deterministic test output."""

    def log_message(self, format: str, *args: object) -> None:
        """Suppress static-server access logs."""

        del format, args


@contextmanager
def _serve_static_site(site_dir: Path) -> Iterator[str]:
    """Serve a local MkDocs build for a real browser-navigation test."""
    handler = partial(_QuietStaticHandler, directory=site_dir)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = server.server_address
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


def _extract_python_fences(document: str) -> list[str]:
    """Return copyable Python examples in source order."""
    return re.findall(r"```python\n(.*?)```", document, flags=re.DOTALL)


def _fake_quick_start_module() -> ModuleType:
    """Provide an offline package double for copied quick-start examples."""

    class _Config:
        def __init__(self, **values: object) -> None:
            self.values = values

    class _Credentials:
        def __init__(self, **values: object) -> None:
            self.values = values

    class _Client:
        def __init__(self, config: _Config) -> None:
            del config
            self.markets = SimpleNamespace(
                search=lambda epic: SimpleNamespace(
                    items=(SimpleNamespace(epic=epic, market_status="TRADEABLE"),)
                )
            )

        def __enter__(self) -> _Client:
            return self

        def __exit__(self, *args: object) -> None:
            del args

    class _AsyncClient:
        def __init__(self, config: _Config) -> None:
            del config
            self.accounts = SimpleNamespace(
                list=self._list_accounts,
            )

        async def __aenter__(self) -> _AsyncClient:
            return self

        async def __aexit__(self, *args: object) -> None:
            del args

        @staticmethod
        async def _list_accounts() -> SimpleNamespace:
            return SimpleNamespace(items=())

    module = ModuleType("ig_trading_lib")
    module.Environment = SimpleNamespace(DEMO="demo")
    module.IGClient = _Client
    module.AsyncIGClient = _AsyncClient
    module.IGConfig = _Config
    module.SessionCredentials = _Credentials
    return module


def test_getting_started_examples_are_independently_copyable_and_offline_runnable() -> None:
    """Each introductory Python block must run without relying on another block."""
    getting_started = GETTING_STARTED_PAGE.read_text(encoding="utf-8")

    assert "Use Python 3.11, 3.12, or 3.13" in getting_started
    snippets = _extract_python_fences(getting_started)
    assert len(snippets) == 2

    fake_module = _fake_quick_start_module()
    monkeypatch = MonkeyPatch()
    monkeypatch.setitem(sys.modules, "ig_trading_lib", fake_module)
    try:
        for position, snippet in enumerate(snippets, start=1):
            exec(compile(snippet, f"quick-start-{position}", "exec"), {"__name__": "__main__"})
    finally:
        monkeypatch.undo()


def test_api_index_and_llms_are_exactly_generated_from_the_public_contract() -> None:
    """Committed agent artifacts must be a deterministic projection of canonical sources."""
    contract = load_public_contract(PROJECT_ROOT)
    endpoints = load_endpoint_index(PROJECT_ROOT)
    expected_index = build_api_index(PROJECT_ROOT, contract, endpoints)
    expected_llms = build_llms_document(expected_index, site_root=True)
    expected_entry_points = build_client_entry_points_document(expected_index)

    actual_index = json.loads((PROJECT_ROOT / API_INDEX_PATH).read_text(encoding="utf-8"))
    actual_llms = (PROJECT_ROOT / LLMS_PATH).read_text(encoding="utf-8")
    actual_entry_points = (PROJECT_ROOT / CLIENT_ENTRY_POINTS_PATH).read_text(encoding="utf-8")

    assert actual_index == expected_index
    assert actual_llms == expected_llms
    assert actual_entry_points == expected_entry_points
    assert (PROJECT_ROOT / "llms.txt").read_text(encoding="utf-8") == build_llms_document(
        expected_index,
        site_root=False,
    )
    assert actual_index["schema_version"] == 2
    assert actual_index["contract_schema_version"] == contract["schema_version"]
    assert actual_index["root_exports"] == contract["root_exports"]
    assert actual_index["endpoints"] == endpoints
    assert actual_index["complete_reference"] == {
        "classes": contract["classes"],
        "functions": contract["functions"],
        "exceptions": contract["exceptions"],
        "pydantic_fields": contract["pydantic_fields"],
    }


def test_generated_index_declares_its_canonical_sources() -> None:
    """Agents can identify the files to re-read when the generated index drifts."""
    index = json.loads((PROJECT_ROOT / API_INDEX_PATH).read_text(encoding="utf-8"))

    assert index["generated_from"] == {
        "contract": "docs/contracts/public-api.yml",
        "endpoint_catalog": "src/ig_trading_lib/endpoint_catalog.py",
        "client_source": "src/ig_trading_lib/client.py",
    }
    assert set(index["entry_points"]) == {"IGClient", "AsyncIGClient"}
    assert index["entry_points"]["IGClient"]["import"] == "from ig_trading_lib import IGClient"
    assert index["entry_points"]["IGClient"]["constructor"]["parameters"] == [
        {
            "name": "config",
            "type": "IGConfig",
            "description": (
                "Immutable environment, credentials, timeout, retry, and account configuration."
            ),
        },
        {
            "name": "trading_permit",
            "type": "TradingPermit | None",
            "description": "Explicit acknowledgement required for guarded live mutations.",
        },
        {
            "name": "http_client",
            "type": "httpx.Client | None",
            "description": "Optional caller-owned HTTP client.",
        },
    ]
    assert {namespace["name"] for namespace in index["entry_points"]["IGClient"]["namespaces"]} == {
        "positions",
        "markets",
        "accounts",
        "activity",
        "transactions",
        "watchlists",
        "confirms",
        "working_orders",
        "repeat_dealing_window",
        "categories",
        "sentiment",
        "costs",
        "applications",
        "prices",
        "session",
        "streaming",
        "v1",
        "v2",
        "v3",
        "v4",
    }
    assert "ig_trading_lib.async_services.AsyncResourceClient" not in index["entry_points"]
    assert (
        "ig_trading_lib.async_services.AsyncResourceClient"
        in index["complete_reference"]["classes"]
    )
    assert any(endpoint["name"] == "market_search" for endpoint in index["endpoints"])


def test_mkdocs_navigation_and_search_expose_the_conceptual_guides(tmp_path: Path) -> None:
    """A local Chromium browser can navigate guides and find them through MkDocs search."""
    site_dir = tmp_path / "site"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "mkdocs",
            "build",
            "--strict",
            "--site-dir",
            str(site_dir),
        ],
        check=True,
        cwd=PROJECT_ROOT,
    )

    expected_pages = {
        "guides/credentials/",
        "guides/accounts/",
        "guides/markets-and-history/",
        "guides/positions-and-working-orders/",
        "guides/confirmations/",
        "guides/streaming/",
        "guides/errors-and-observability/",
        "guides/pagination-and-rate-limits/",
        "guides/version-facades/",
        "recipes/",
        "reference/agent-api-index/",
    }
    assert all((site_dir / page / "index.html").is_file() for page in expected_pages)
    assert (site_dir / "llms.txt").is_file()

    search_index = json.loads(
        (site_dir / "search" / "search_index.json").read_text(encoding="utf-8")
    )
    locations = {document["location"] for document in search_index["docs"]}
    titles = {document["title"] for document in search_index["docs"]}

    assert "guides/credentials/" in locations
    assert "recipes/" in locations
    assert "Credentials and environments" in titles
    assert "Sync and async recipes" in titles

    with _serve_static_site(site_dir) as base_url, sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page()
            page.goto(base_url, wait_until="networkidle")
            page.get_by_role("link", name="Credentials and environments").first.click()
            expect(page).to_have_url(f"{base_url}/guides/credentials/")
            expect(page).to_have_title("Credentials and environments - IG Trading Library")

            page.goto(base_url, wait_until="networkidle")
            page.locator("input[data-md-component='search-query']").fill("TradingPermit")
            safety_result = page.locator("a.md-search-result__link[href*='guides/safety/']")
            expect(safety_result.first).to_be_visible(timeout=10_000)
            safety_result.first.click()
            expect(page).to_have_url(re.compile(r".*/guides/safety/(?:\?h=)?$"))
        finally:
            browser.close()


def test_ig_login_reference_theme_is_present_in_the_rendered_documentation(tmp_path: Path) -> None:
    """The local documentation preview uses the IG login page's restrained visual language."""
    configuration = (PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    landing = LANDING_PAGE.read_text(encoding="utf-8")
    getting_started = GETTING_STARTED_PAGE.read_text(encoding="utf-8")

    assert "extra_css:\n  - stylesheets/ig-theme.css" in configuration
    assert "show_root_heading: false" in configuration
    assert ">Start with a demo</a>" in landing
    assert "## Documentation contract" not in landing
    assert "Use Python 3.11, 3.12, or 3.13" in getting_started
    assert "asyncio.run(main())" in getting_started
    stylesheet = IG_THEME_STYLESHEET.read_text(encoding="utf-8")
    assert "--ig-login-black: #000000" in stylesheet
    assert "--ig-login-red: #e61e1e" in stylesheet

    site_dir = tmp_path / "site"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "mkdocs",
            "build",
            "--strict",
            "--site-dir",
            str(site_dir),
        ],
        check=True,
        cwd=PROJECT_ROOT,
    )

    assert (site_dir / "stylesheets" / "ig-theme.css").is_file()

    with _serve_static_site(site_dir) as base_url, sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            desktop = browser.new_page(viewport={"width": 1440, "height": 1000})
            desktop.goto(base_url, wait_until="networkidle")
            hero = desktop.locator(".ig-docs-hero")
            primary_action = desktop.locator(".ig-docs-primary-action")

            expect(hero).to_be_visible()
            expect(primary_action).to_be_visible()
            expect(primary_action).to_have_accessible_name("Start with a demo")
            assert primary_action.get_attribute("href") == "getting-started/"
            assert (
                hero.evaluate("element => getComputedStyle(element).backgroundColor")
                == "rgb(0, 0, 0)"
            )
            assert (
                primary_action.evaluate("element => getComputedStyle(element).backgroundColor")
                == "rgb(230, 30, 30)"
            )
            assert (
                primary_action.evaluate("element => getComputedStyle(element).color")
                == "rgb(0, 0, 0)"
            )

            light_code = browser.new_page()
            light_code.goto(f"{base_url}/guides/credentials/", wait_until="networkidle")
            code_block = light_code.locator(".md-typeset .highlight").first
            code_pre = code_block.locator("pre")

            assert (
                code_block.evaluate("element => getComputedStyle(element).borderTopWidth") == "1px"
            )
            assert code_pre.evaluate("element => getComputedStyle(element).borderTopWidth") == "0px"
            assert code_pre.evaluate("element => getComputedStyle(element).marginTop") == "0px"
            light_copy_button = code_block.locator(".md-code__button")
            light_copy_nav = code_block.locator(".md-code__nav")

            assert (
                light_copy_button.evaluate("element => getComputedStyle(element).color")
                == "rgb(111, 111, 111)"
            )
            assert (
                light_copy_nav.evaluate("element => getComputedStyle(element).backgroundColor")
                == "rgba(0, 0, 0, 0)"
            )

            mobile = browser.new_page(viewport={"width": 390, "height": 844})
            mobile.goto(base_url, wait_until="networkidle")
            assert mobile.evaluate("document.documentElement.scrollWidth <= window.innerWidth")

            dark = browser.new_page(color_scheme="dark")
            dark.goto(f"{base_url}/guides/markets-and-history/", wait_until="networkidle")
            assert dark.locator("body").get_attribute("data-md-color-scheme") == "ig-login-dark"
            assert (
                dark.locator(".md-typeset p").first.evaluate(
                    "element => getComputedStyle(element).color"
                )
                == "rgb(255, 255, 255)"
            )
            assert (
                dark.locator(".md-nav__link").first.evaluate(
                    "element => getComputedStyle(element).color"
                )
                == "rgb(255, 255, 255)"
            )
            code_name = dark.locator(".language-python .n").first
            copy_button = dark.locator(".md-code__button").first

            expect(copy_button).to_be_visible()
            assert (
                code_name.evaluate("element => getComputedStyle(element).color")
                == "rgb(244, 244, 244)"
            )
            assert (
                copy_button.evaluate("element => getComputedStyle(element).color")
                == "rgb(224, 224, 224)"
            )
            assert (
                copy_button.locator("xpath=..").evaluate(
                    "element => getComputedStyle(element).backgroundColor"
                )
                == "rgba(0, 0, 0, 0)"
            )

            reference = browser.new_page(viewport={"width": 1440, "height": 1000})
            reference.goto(f"{base_url}/reference/public-api/", wait_until="networkidle")
            reference_headings = [
                heading.strip() for heading in reference.locator("main h2").all_text_contents()
            ]

            assert reference_headings[:10] == [
                "Client construction",
                "Client façades",
                "Configuration and safety primitives",
                "Canonical models",
                "Public failures",
                "Synchronous services",
                "Asynchronous services",
                "Streaming",
                "Explicit-version façades",
                "Endpoint catalogue model",
            ]
            assert not any(heading.startswith("ig_trading_lib.") for heading in reference_headings)
            reference_text = reference.locator("main").inner_text()
            assert (
                "Immutable environment, credentials, timeout, retry, and account configuration."
                in (reference_text)
            )
            assert "Explicit acknowledgement required for guarded live mutations." in reference_text
            assert "Obtain service namespaces from a client; do not construct them directly." in (
                reference_text
            )
            constructor_tables = reference.locator("table").filter(
                has_text=(
                    "Immutable environment, credentials, timeout, retry, and account configuration."
                )
            )
            namespace_table = reference.locator("table").filter(has_text="client.positions")

            expect(constructor_tables).to_have_count(2)
            expect(namespace_table).to_be_visible()
        finally:
            browser.close()
