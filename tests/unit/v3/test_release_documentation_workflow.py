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


def test_release_documentation_workflow_recovers_an_existing_tag_without_retagging() -> None:
    """A failed tagged release can resume from main without changing the tag."""
    workflow = (PROJECT_ROOT / WORKFLOW_PATH).read_text(encoding="utf-8")
    recovery_checkout = (
        "ref: ${{ github.event_name == 'workflow_dispatch' "
        "&& format('refs/tags/{0}', inputs.release_tag) || github.ref }}"
    )

    assert "workflow_dispatch:\n    inputs:\n      release_tag:" in workflow
    assert "github.event_name == 'workflow_dispatch' && inputs.release_tag != ''" in workflow
    assert 'git rev-parse "$tag_ref^{}"' in workflow
    assert 'git cat-file -p "$tag_ref"' in workflow
    assert 'git cat-file -t "$TAG^{}"' in workflow
    assert "ref: ${{ needs.validate-release.outputs.tag }}" in workflow
    assert workflow.count(recovery_checkout) == 2
    assert 'echo "commit=$commit"' in workflow


def test_release_documentation_workflow_configures_a_generated_docs_commit_identity() -> None:
    """Mike receives an explicit bot identity before it writes gh-pages."""
    workflow = (PROJECT_ROOT / WORKFLOW_PATH).read_text(encoding="utf-8")

    assert 'git config user.name "github-actions[bot]"' in workflow
    assert (
        'git config user.email "41898282+github-actions[bot]@users.noreply.github.com"' in workflow
    )


def test_release_documentation_workflow_rejects_an_unpinned_recovery_checkout(
    tmp_path: Path,
) -> None:
    """A manual recovery must validate the requested tag, never the dispatch branch."""
    workflow_path = tmp_path / WORKFLOW_PATH
    workflow_path.parent.mkdir(parents=True)
    workflow = (PROJECT_ROOT / WORKFLOW_PATH).read_text(encoding="utf-8")
    workflow_path.write_text(
        workflow.replace(
            "ref: ${{ github.event_name == 'workflow_dispatch' "
            "&& format('refs/tags/{0}', inputs.release_tag) || github.ref }}",
            "ref: ${{ github.ref }}",
        ),
        encoding="utf-8",
    )

    with pytest.raises(ReleaseWorkflowError, match="exact release source"):
        validate_release_workflow(tmp_path)


def test_release_documentation_workflow_rejects_a_missing_mike_commit_identity(
    tmp_path: Path,
) -> None:
    """Generated docs must always have a declared bot author."""
    workflow_path = tmp_path / WORKFLOW_PATH
    workflow_path.parent.mkdir(parents=True)
    workflow = (PROJECT_ROOT / WORKFLOW_PATH).read_text(encoding="utf-8")
    workflow_path.write_text(
        workflow.replace('git config user.name "github-actions[bot]"', "true"),
        encoding="utf-8",
    )

    with pytest.raises(ReleaseWorkflowError, match="bot identity"):
        validate_release_workflow(tmp_path)


def test_release_documentation_workflow_rejects_a_shallow_release_checkout(
    tmp_path: Path,
) -> None:
    """Annotated-tag validation needs the complete tag history."""
    workflow_path = tmp_path / WORKFLOW_PATH
    workflow_path.parent.mkdir(parents=True)
    workflow = (PROJECT_ROOT / WORKFLOW_PATH).read_text(encoding="utf-8")
    workflow_path.write_text(workflow.replace("fetch-depth: 0", "fetch-depth: 1"), encoding="utf-8")

    with pytest.raises(ReleaseWorkflowError, match="exact release source"):
        validate_release_workflow(tmp_path)


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
