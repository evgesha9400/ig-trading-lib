"""Install and smoke-test the exact wheel and source distribution."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SMOKE = ROOT / "scripts/smoke_installed_package.py"


def _version() -> str:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert project["name"] == "ig-trading-lib"
    assert project["requires-python"] == ">=3.11,<3.14"
    assert project["urls"]["Documentation"].endswith("/latest/")
    return project["version"]


def _artifacts(version: str) -> tuple[Path, Path]:
    wheel = DIST / f"ig_trading_lib-{version}-py3-none-any.whl"
    source = DIST / f"ig_trading_lib-{version}.tar.gz"
    if not wheel.is_file() or not source.is_file():
        raise FileNotFoundError("Expected exact wheel and source distribution artifacts.")
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        assert any(name.endswith("METADATA") for name in names)
        assert not any(name.startswith("tests/") or name.startswith("docs/") for name in names)
    return wheel, source


def _install_and_smoke(artifact: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="ig-trading-lib-smoke-") as directory:
        environment = Path(directory)
        subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True)
        python = environment / "bin/python"
        subprocess.run(
            [str(python), "-m", "pip", "install", "--disable-pip-version-check", str(artifact)],
            check=True,
        )
        subprocess.run([str(python), str(SMOKE)], cwd=directory, check=True)


def main() -> None:
    for artifact in _artifacts(_version()):
        _install_and_smoke(artifact)
    print("Wheel and source distribution smoke tests passed.")


if __name__ == "__main__":
    main()
