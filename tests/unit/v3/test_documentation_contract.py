import shutil
import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.check_documentation_contract import (  # noqa: E402
    DocumentationContractError,
    validate_documentation_contract,
)


def test_public_documentation_contract_is_complete() -> None:
    """Documentation must cover every declared public surface before release."""
    validate_documentation_contract(PROJECT_ROOT)


def test_portal_manifest_marks_v3_documentation_as_published() -> None:
    """The v3.0.0 portal manifest must advertise published documentation."""
    manifest_path = PROJECT_ROOT / "docs" / "library.yml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

    assert manifest["status"] == "published"


def test_contract_parameters_have_types_and_descriptions() -> None:
    """Each declared callable parameter must explain its public meaning."""
    contract_path = PROJECT_ROOT / "docs" / "contracts" / "public-api.yml"
    contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    parameters = contract["classes"]["ig_trading_lib.client.IGClient"]["constructor"]["parameters"]

    assert parameters == [
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


def test_documentation_contract_rejects_missing_parameter_description(tmp_path: Path) -> None:
    """Parameter prose is required in addition to the source signature."""
    project_root = tmp_path / "project"
    for directory_name in ("docs", "examples", "src"):
        shutil.copytree(PROJECT_ROOT / directory_name, project_root / directory_name)
    contract_path = project_root / "docs" / "contracts" / "public-api.yml"
    contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    contract["classes"]["ig_trading_lib.client.IGClient"]["constructor"]["parameters"][0][
        "description"
    ] = ""
    contract_path.write_text(yaml.safe_dump(contract, sort_keys=False), encoding="utf-8")

    try:
        validate_documentation_contract(project_root)
    except DocumentationContractError as error:
        assert "Parameter descriptions" in str(error)
    else:
        raise AssertionError("A missing parameter description must be rejected.")


def test_documentation_contract_rejects_missing_rest_reference_entries(tmp_path: Path) -> None:
    """Each generated REST category is a release gate, not an informational table."""
    project_root = tmp_path / "project"
    for directory_name in ("docs", "examples", "src"):
        shutil.copytree(PROJECT_ROOT / directory_name, project_root / directory_name)
    endpoint_table = project_root / "docs" / "rest-api-reference" / ".account-endpoints.md"
    endpoint_table.write_text(
        endpoint_table.read_text(encoding="utf-8").replace(
            "| accounts | GET | `/accounts` |\n", "", 1
        ),
        encoding="utf-8",
    )

    try:
        validate_documentation_contract(project_root)
    except DocumentationContractError as error:
        assert "REST reference section" in str(error)
    else:
        raise AssertionError("A missing REST reference entry must be rejected.")


def test_documentation_contract_rejects_missing_public_module_reference(tmp_path: Path) -> None:
    """Generated reference coverage is required for every documented source module."""
    project_root = tmp_path / "project"
    for directory_name in ("docs", "examples", "src"):
        shutil.copytree(PROJECT_ROOT / directory_name, project_root / directory_name)
    reference_path = project_root / "docs" / "reference" / "public-api.md"
    reference_path.write_text(
        reference_path.read_text(encoding="utf-8").replace("::: ig_trading_lib.streaming", "", 1),
        encoding="utf-8",
    )

    try:
        validate_documentation_contract(project_root)
    except DocumentationContractError as error:
        assert "Public API reference" in str(error)
    else:
        raise AssertionError("A missing public module reference must be rejected.")
