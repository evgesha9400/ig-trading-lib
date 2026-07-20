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

import yaml
from playwright.sync_api import expect, sync_playwright
from pytest import MonkeyPatch

from scripts.generate_documentation_indexes import (
    API_INDEX_PATH,
    CLIENT_ENTRY_POINTS_PATH,
    LLMS_PATH,
    build_api_index,
    build_client_entry_points_document,
    build_llms_document,
    load_endpoint_reference,
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
    endpoints, sections = load_endpoint_reference(PROJECT_ROOT)
    expected_index = build_api_index(PROJECT_ROOT, contract, endpoints, sections)
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
    assert actual_index["schema_version"] == 4
    assert actual_index["contract_schema_version"] == contract["schema_version"]
    assert actual_index["root_exports"] == contract["root_exports"]
    assert actual_index["endpoints"] == endpoints
    assert actual_index["rest_reference"] == {
        "directory": "docs/rest-api-reference",
        "sections": sections,
    }
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
    }
    assert all("versions" not in endpoint for endpoint in index["endpoints"])
    assert "ig_trading_lib.async_services.AsyncResourceClient" not in index["entry_points"]
    assert (
        "ig_trading_lib.async_services.AsyncResourceClient"
        in index["complete_reference"]["classes"]
    )
    assert any(endpoint["name"] == "market_search" for endpoint in index["endpoints"])


def test_documentation_exposes_only_the_current_library_surface() -> None:
    """Legacy migration and version-facade guidance must never re-enter published docs."""
    documentation_paths = [
        PROJECT_ROOT / "README.md",
        PROJECT_ROOT / "llms.txt",
        *(PROJECT_ROOT / "docs").rglob("*.json"),
        *(PROJECT_ROOT / "docs").rglob("*.md"),
        *(PROJECT_ROOT / "docs").rglob("*.yml"),
        PROJECT_ROOT / "mkdocs.yml",
    ]
    documentation = "\n".join(path.read_text(encoding="utf-8") for path in documentation_paths)

    assert "v2" not in documentation.casefold()
    assert "migration" not in documentation.casefold()
    assert not (PROJECT_ROOT / "docs" / "migration-v2-to-v3.md").exists()
    assert not (PROJECT_ROOT / "docs" / "reference" / "version-compatibility.md").exists()


def test_mkdocs_navigation_and_search_mirror_ig_api_information_architecture(
    tmp_path: Path,
) -> None:
    """The local navigation follows the API guide and a trader workflow reference order."""
    configuration = yaml.safe_load((PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
    navigation = configuration["nav"]

    assert [next(iter(item)) for item in navigation] == [
        "Overview",
        "API guide",
        "REST API reference",
        "Integration guides",
        "Library reference",
    ]
    assert [next(iter(item)) for item in navigation[2]["REST API reference"]] == [
        "Login",
        "Account",
        "Markets",
        "Watchlists",
        "Client sentiment",
        "Indicative costs and charges",
        "Dealing",
        "General",
    ]
    assert [next(iter(item)) for item in navigation[3]["Integration guides"]] == [
        "Overview",
        "Streaming API",
        "Recipes",
    ]

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
        "api-guide/http-requests/",
        "api-guide/authentication-and-authorisation/",
        "api-guide/paging/",
        "api-guide/errors/",
        "api-guide/trading-safety/",
        "rest-api-reference/account/",
        "rest-api-reference/dealing/",
        "rest-api-reference/markets/",
        "rest-api-reference/watchlists/",
        "rest-api-reference/client-sentiment/",
        "rest-api-reference/login/",
        "rest-api-reference/indicative-costs-and-charges/",
        "rest-api-reference/general/",
        "integration-guides/",
        "streaming-api/",
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

    assert "rest-api-reference/dealing/" in locations
    assert "recipes/" in locations
    assert "Authentication and authorisation" in titles
    assert "Sync and async recipes" in titles

    with _serve_static_site(site_dir) as base_url, sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page()
            page.goto(base_url, wait_until="networkidle")
            page.get_by_role("link", name="Login").first.click()
            expect(page).to_have_url(f"{base_url}/rest-api-reference/login/")
            expect(page).to_have_title("Login - IG Trading Library")

            page.goto(base_url, wait_until="networkidle")
            page.locator("input[data-md-component='search-query']").fill("TradingPermit")
            safety_result = page.locator(
                "a.md-search-result__link[href*='api-guide/trading-safety/']"
            )
            expect(safety_result.first).to_be_visible(timeout=10_000)
            safety_result.first.click()
            expect(page).to_have_url(re.compile(r".*/api-guide/trading-safety/(?:\?h=)?$"))
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
            wordmark = desktop.get_by_role("link", name="IG Trading Library")
            brand_mark = wordmark.locator(".ig-docs-brand-mark")
            product_name = wordmark.locator(".ig-docs-brand-name")

            expect(wordmark).to_have_class(re.compile(r"\bmd-header__brand\b"))
            expect(product_name).to_have_text("Trading Library")
            assert (
                brand_mark.evaluate("element => getComputedStyle(element).color")
                == "rgb(230, 30, 30)"
            )
            assert (
                product_name.evaluate("element => getComputedStyle(element).color")
                == "rgb(255, 255, 255)"
            )
            wordmark.hover()
            assert (
                brand_mark.evaluate("element => getComputedStyle(element).color")
                == "rgb(255, 108, 108)"
            )
            assert product_name.evaluate(
                "element => getComputedStyle(element).textDecorationLine"
            ) == ("underline")
            wordmark.click()
            expect(desktop).to_have_url(f"{base_url}/")

            header = desktop.locator(".md-header")
            content_inner = desktop.locator(".md-content__inner")
            header_search = desktop.locator(".ig-docs-header-search")
            search_form = desktop.locator(".ig-docs-header-search .md-search__form")
            utilities = desktop.locator(".ig-docs-header-utilities")
            palette = utilities.locator(".md-header__option")
            source = utilities.locator(".md-header__source")
            header_box = header.bounding_box()
            content_inner_box = content_inner.bounding_box()
            search_box = search_form.bounding_box()
            utilities_box = utilities.bounding_box()
            palette_box = palette.bounding_box()
            source_box = source.bounding_box()

            assert header_box is not None
            assert content_inner_box is not None
            assert (
                header_search.evaluate("element => getComputedStyle(element).position")
                == "absolute"
            )
            assert search_box is not None
            assert utilities_box is not None
            assert palette_box is not None
            assert source_box is not None
            assert (
                abs(
                    (search_box["x"] + search_box["width"] / 2)
                    - (header_box["x"] + header_box["width"] / 2)
                )
                <= 1
            )
            assert search_box["x"] == content_inner_box["x"]
            assert search_box["width"] == content_inner_box["width"]
            assert search_box["x"] + search_box["width"] <= palette_box["x"]
            assert palette_box["x"] < source_box["x"]
            assert utilities_box["x"] + utilities_box["width"] <= header_box["width"]

            search_input = desktop.locator("input[data-md-component='search-query']")
            search_toggle = desktop.locator("#__search")
            search_overlay = desktop.locator(".md-search__overlay")
            search_output = desktop.locator(".md-search__output")

            search_input.click()
            desktop.wait_for_timeout(300)
            focused_search_box = search_form.bounding_box()

            expect(search_input).to_be_focused()
            expect(search_toggle).to_be_checked()
            expect(search_overlay).to_be_visible()
            assert (
                search_overlay.evaluate("element => getComputedStyle(element).backgroundColor")
                == "rgba(0, 0, 0, 0)"
            )
            assert focused_search_box is not None
            assert focused_search_box["width"] == search_box["width"]
            assert focused_search_box["x"] == search_box["x"]
            assert (
                abs(
                    (focused_search_box["x"] + focused_search_box["width"] / 2)
                    - (header_box["x"] + header_box["width"] / 2)
                )
                <= 1
            )
            assert (
                search_input.evaluate("element => getComputedStyle(element).outlineStyle") == "none"
            )

            desktop.mouse.click(20, 200)
            expect(search_toggle).not_to_be_checked()
            expect(search_input).not_to_be_focused()
            expect(search_output).not_to_be_visible()

            search_input.click()
            expect(search_toggle).to_be_checked()
            expect(search_input).to_be_focused()

            search_input.press_sequentially("TradingPermit")
            desktop.wait_for_timeout(300)
            search_result = desktop.locator(
                "a.md-search-result__link[href*='api-guide/trading-safety/']"
            )
            search_highlight = search_output.locator("mark").first
            populated_search_box = search_form.bounding_box()
            search_output_box = search_output.bounding_box()

            expect(search_input).to_have_value("TradingPermit")
            expect(search_result.first).to_be_visible(timeout=10_000)
            expect(search_highlight).to_be_visible()
            assert populated_search_box is not None
            assert search_output_box is not None
            assert populated_search_box["width"] == search_box["width"]
            assert populated_search_box["x"] == search_box["x"]
            assert search_output_box["x"] == search_box["x"]
            assert search_output_box["width"] == search_box["width"]
            assert search_output_box["height"] <= 560
            assert (
                search_output.evaluate("element => getComputedStyle(element).backgroundColor")
                == "rgb(255, 255, 255)"
            )
            assert (
                search_highlight.evaluate("element => getComputedStyle(element).color")
                == "rgb(22, 22, 22)"
            )
            assert (
                search_highlight.evaluate("element => getComputedStyle(element).backgroundColor")
                == "rgb(244, 244, 244)"
            )

            desktop.mouse.click(20, 200)
            expect(search_toggle).not_to_be_checked()
            expect(search_output).not_to_be_visible()
            theme_toggle = desktop.locator("label[title='Switch to dark mode']")
            theme_toggle.click()
            assert desktop.locator("body").get_attribute("data-md-color-scheme") == "ig-login-dark"
            desktop.locator("label[title='Switch to light mode']").click()
            assert desktop.locator("body").get_attribute("data-md-color-scheme") == "ig-login-light"

            api_guide = desktop.locator(
                ".md-nav--primary > .md-nav__list > .md-nav__item--section"
            ).filter(has_text="API guide")
            section_title = api_guide.locator(":scope > .md-nav__link")
            section_pages = api_guide.locator(":scope > .md-nav > .md-nav__list")
            first_section_page = section_pages.locator(
                ":scope > .md-nav__item > .md-nav__link"
            ).first
            section_title_box = section_title.bounding_box()
            first_section_page_box = first_section_page.bounding_box()

            assert section_title_box is not None
            assert first_section_page_box is not None
            assert (
                section_title.evaluate("element => getComputedStyle(element).color")
                == "rgb(22, 22, 22)"
            )
            assert first_section_page_box["x"] - section_title_box["x"] >= 8
            assert (
                section_pages.evaluate("element => getComputedStyle(element).borderLeftWidth")
                == "2px"
            )

            light_code = browser.new_page()
            light_code.goto(
                f"{base_url}/api-guide/authentication-and-authorisation/",
                wait_until="networkidle",
            )
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
            mobile_brand_box = mobile.locator(".md-header__brand").bounding_box()
            mobile_search_box = mobile.locator(
                ".ig-docs-header-search > .md-header__button"
            ).bounding_box()
            mobile_palette_box = mobile.locator(".ig-docs-header-utilities").bounding_box()

            assert mobile_brand_box is not None
            assert mobile_search_box is not None
            assert mobile_palette_box is not None
            assert mobile_brand_box["x"] + mobile_brand_box["width"] <= mobile_search_box["x"]
            assert mobile_search_box["x"] + mobile_search_box["width"] <= mobile_palette_box["x"]
            expect(mobile.locator(".md-header__source")).not_to_be_visible()
            assert mobile.evaluate("document.documentElement.scrollWidth <= window.innerWidth")

            keyboard = browser.new_page(viewport={"width": 1440, "height": 1000})
            keyboard.goto(base_url, wait_until="networkidle")
            keyboard.keyboard.press("Tab")
            keyboard.keyboard.press("Tab")
            keyboard.keyboard.press("Tab")
            expect(keyboard.locator("input[data-md-component='search-query']")).to_be_focused()

            dark = browser.new_page(color_scheme="dark")
            dark.goto(f"{base_url}/rest-api-reference/markets/", wait_until="networkidle")
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

            assert reference_headings[:8] == [
                "Client construction",
                "Client façades",
                "Configuration and safety primitives",
                "Canonical models",
                "Public failures",
                "Synchronous services",
                "Asynchronous services",
                "Streaming",
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
