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

from playwright.sync_api import expect, sync_playwright

from scripts.generate_documentation_indexes import (
    API_INDEX_PATH,
    LLMS_PATH,
    build_api_index,
    build_llms_document,
    load_endpoint_index,
    load_public_contract,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]


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


def test_api_index_and_llms_are_exactly_generated_from_the_public_contract() -> None:
    """Committed agent artifacts must be a deterministic projection of canonical sources."""
    contract = load_public_contract(PROJECT_ROOT)
    endpoints = load_endpoint_index(PROJECT_ROOT)
    expected_index = build_api_index(contract, endpoints)
    expected_llms = build_llms_document(expected_index, site_root=True)

    actual_index = json.loads((PROJECT_ROOT / API_INDEX_PATH).read_text(encoding="utf-8"))
    actual_llms = (PROJECT_ROOT / LLMS_PATH).read_text(encoding="utf-8")

    assert actual_index == expected_index
    assert actual_llms == expected_llms
    assert (PROJECT_ROOT / "llms.txt").read_text(encoding="utf-8") == build_llms_document(
        expected_index,
        site_root=False,
    )
    assert actual_index["classes"] == contract["classes"]
    assert actual_index["functions"] == contract["functions"]
    assert actual_index["root_exports"] == contract["root_exports"]
    assert actual_index["endpoints"] == endpoints


def test_generated_index_declares_its_canonical_sources() -> None:
    """Agents can identify the files to re-read when the generated index drifts."""
    index = json.loads((PROJECT_ROOT / API_INDEX_PATH).read_text(encoding="utf-8"))

    assert index["generated_from"] == {
        "contract": "docs/contracts/public-api.yml",
        "endpoint_catalog": "src/ig_trading_lib/endpoint_catalog.py",
    }
    assert "ig_trading_lib.versions.VersionFacade" in index["classes"]
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
            safety_result = page.locator("a.md-search-result__link").filter(has_text="Safety")
            expect(safety_result.first).to_be_visible(timeout=10_000)
            safety_result.first.click()
            expect(page).to_have_url(re.compile(r".*/guides/safety/(?:\?h=)?$"))
        finally:
            browser.close()
