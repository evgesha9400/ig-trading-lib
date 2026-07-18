"""Offline safety checks for tag-only documentation publishing."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.check_release_workflow import (
    WORKFLOW_PATH,
    ReleaseWorkflowError,
    validate_release_workflow,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def test_release_documentation_workflow_preserves_the_release_boundary() -> None:
    """Versioned docs, releases, and portal dispatch retain their narrow contract."""
    validate_release_workflow(PROJECT_ROOT)


def test_portal_dispatch_waits_for_documentation_and_release_record() -> None:
    """The portal cannot advertise a release before its immutable record exists."""
    workflow = (PROJECT_ROOT / WORKFLOW_PATH).read_text(encoding="utf-8")

    assert _expected_portal_dispatch_header() in workflow


def test_release_documentation_workflow_rejects_portal_dispatch_before_release_record(
    tmp_path: Path,
) -> None:
    """Portal publication must wait for both docs and the GitHub Release record."""
    workflow_path = tmp_path / WORKFLOW_PATH
    workflow_path.parent.mkdir(parents=True)
    workflow = (PROJECT_ROOT / WORKFLOW_PATH).read_text(encoding="utf-8")
    workflow_path.write_text(
        workflow.replace(
            _expected_portal_dispatch_header(),
            """  dispatch-portal-rebuild:
    name: Dispatch portal rebuild
    needs: [validate-release, publish-versioned-documentation]
    if: needs.publish-versioned-documentation.result == 'success'
""",
        ),
        encoding="utf-8",
    )

    with pytest.raises(ReleaseWorkflowError, match="GitHub Release record"):
        validate_release_workflow(tmp_path)


def _expected_portal_dispatch_header() -> str:
    return (
        "  dispatch-portal-rebuild:\n"
        "    name: Dispatch portal rebuild\n"
        "    needs: [validate-release, publish-versioned-documentation, create-github-release]\n"
        "    if: needs.publish-versioned-documentation.result == 'success' "
        "&& needs.create-github-release.result == 'success'\n"
    )


def test_release_documentation_workflow_rejects_missing_package_version_match(
    tmp_path: Path,
) -> None:
    """A release tag cannot be decoupled from the package version gate."""
    workflow_path = tmp_path / WORKFLOW_PATH
    workflow_path.parent.mkdir(parents=True)
    workflow = (PROJECT_ROOT / WORKFLOW_PATH).read_text(encoding="utf-8")
    workflow_path.write_text(
        workflow.replace(
            "Release tag $TAG does not match pyproject.toml version $package_version.",
            "Release tag $TAG does not match the configured package version.",
        ),
        encoding="utf-8",
    )

    with pytest.raises(ReleaseWorkflowError, match="package-version mismatches"):
        validate_release_workflow(tmp_path)
