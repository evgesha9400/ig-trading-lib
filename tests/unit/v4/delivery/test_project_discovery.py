from __future__ import annotations

import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DOCUMENTATION_URL = "https://evgesha9400.github.io/ig-trading-lib/latest/"
SOURCE_URL = "https://github.com/evgesha9400/ig-trading-lib"
PYPI_URL = "https://pypi.org/project/ig-trading-lib/"


def test_readme_exposes_primary_project_destinations() -> None:
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

    assert f"[Documentation]({DOCUMENTATION_URL})" in readme
    assert f"[Source]({SOURCE_URL})" in readme
    assert f"[PyPI]({PYPI_URL})" in readme


def test_package_metadata_exposes_primary_project_destinations() -> None:
    pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project_urls = pyproject["project"]["urls"]

    assert project_urls["Documentation"] == DOCUMENTATION_URL
    assert project_urls["Source"] == SOURCE_URL
    assert project_urls["Issues"] == f"{SOURCE_URL}/issues"
