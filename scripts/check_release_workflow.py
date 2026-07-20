"""Validate the repository's constrained versioned-documentation workflow."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

WORKFLOW_PATH = Path(".github/workflows/release-documentation.yml")
LIBRARY_REPOSITORY = "evgesha9400/ig-trading-lib"
PORTAL_REPOSITORY = "evgesha9400/evgesha9400.github.io"
PORTAL_WORKFLOW = "rebuild-library-pages.yml"
PYPI_PUBLISH_ACTION = "pypa/gh-action-pypi-publish@ba38be9e461d3875417946c167d0b5f3d385a247"


class ReleaseWorkflowError(ValueError):
    """Raised when the release workflow loses a required safety guarantee."""


def validate_release_workflow(project_root: Path) -> None:
    """Check tag validation, immutable docs, permissions, and portal hand-off."""
    workflow_path = project_root / WORKFLOW_PATH
    _validate_secret_references(workflow_path)
    workflow = _load_workflow(workflow_path)
    _validate_triggers(workflow)
    _validate_top_level_permissions(workflow)
    _validate_jobs(workflow)


def _load_workflow(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ReleaseWorkflowError(f"Missing release workflow: {path}")
    workflow = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    if not isinstance(workflow, dict):
        raise ReleaseWorkflowError("Release workflow must be a YAML mapping.")
    return workflow


def _validate_secret_references(path: Path) -> None:
    secret_names = re.findall(
        r"secrets\.([A-Za-z_][A-Za-z0-9_]*)", path.read_text(encoding="utf-8")
    )
    if secret_names != ["PYPI_API_TOKEN", "LIBRARY_PORTAL_DISPATCH_TOKEN"]:
        raise ReleaseWorkflowError(
            "Only the PyPI publication and portal dispatch secrets may be referenced."
        )


def _validate_triggers(workflow: dict[str, Any]) -> None:
    triggers = workflow.get("on")
    if not isinstance(triggers, dict):
        raise ReleaseWorkflowError("Release workflow must declare event triggers.")
    push = triggers.get("push")
    if not isinstance(push, dict):
        raise ReleaseWorkflowError("Release workflow must validate push events.")
    if push.get("branches") != ["main", "develop"]:
        raise ReleaseWorkflowError("Only main and develop may run branch documentation validation.")
    if push.get("tags") != ["v*"]:
        raise ReleaseWorkflowError("Release documentation must be triggered only by v* tags.")
    if "pull_request" not in triggers or "workflow_dispatch" not in triggers:
        raise ReleaseWorkflowError("Documentation validation must also cover PRs and manual runs.")
    _validate_manual_recovery_input(triggers["workflow_dispatch"])


def _validate_manual_recovery_input(manual_dispatch: object) -> None:
    if not isinstance(manual_dispatch, dict):
        raise ReleaseWorkflowError("Manual documentation runs must declare the recovery-tag input.")
    inputs = manual_dispatch.get("inputs")
    if not isinstance(inputs, dict) or set(inputs) != {"release_tag"}:
        raise ReleaseWorkflowError("Manual runs must expose only the release_tag recovery input.")
    release_tag = inputs["release_tag"]
    if not isinstance(release_tag, dict):
        raise ReleaseWorkflowError("The recovery tag input must be a mapping.")
    if release_tag.get("required") != "false" or release_tag.get("type") != "string":
        raise ReleaseWorkflowError("The recovery tag input must be an optional string.")


def _validate_top_level_permissions(workflow: dict[str, Any]) -> None:
    if workflow.get("permissions") != {"contents": "read"}:
        raise ReleaseWorkflowError("The workflow default permission must be contents: read.")


def _validate_jobs(workflow: dict[str, Any]) -> None:
    _validate_workflow_environment(workflow)
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        raise ReleaseWorkflowError("Release workflow must declare jobs.")
    required_jobs = {
        "validate-documentation",
        "validate-release",
        "publish-versioned-documentation",
        "publish-python-package",
        "create-github-release",
        "dispatch-portal-rebuild",
    }
    if set(jobs) != required_jobs:
        raise ReleaseWorkflowError(
            "Release workflow jobs must match the constrained release pipeline."
        )

    _validate_documentation_job(jobs["validate-documentation"])
    _validate_tag_job(jobs["validate-release"])
    _validate_publish_job(jobs["publish-versioned-documentation"])
    _validate_pypi_publish_job(jobs["publish-python-package"])
    _validate_github_release_job(jobs["create-github-release"])
    _validate_portal_dispatch_job(jobs["dispatch-portal-rebuild"])


def _validate_workflow_environment(workflow: dict[str, Any]) -> None:
    expected_environment = {
        "LIBRARY_REPOSITORY": LIBRARY_REPOSITORY,
        "PORTAL_REPOSITORY": PORTAL_REPOSITORY,
        "PORTAL_WORKFLOW": PORTAL_WORKFLOW,
        "PORTAL_REF": "main",
    }
    if workflow.get("env") != expected_environment:
        raise ReleaseWorkflowError("Release workflow must use the fixed portal dispatch identity.")


def _validate_documentation_job(job: object) -> None:
    if not isinstance(job, dict) or job.get("permissions") != {"contents": "read"}:
        raise ReleaseWorkflowError("Documentation validation must remain read-only.")
    if _checkout_refs(job) != [_release_checkout_ref()] or _checkout_fetch_depths(job) != ["0"]:
        raise ReleaseWorkflowError(
            "Documentation validation must check out the exact release source."
        )
    commands = _job_commands(job)
    _require(commands, "make docs-check", "Documentation validation must build the site strictly.")
    _require(
        commands, "make workflow-check", "Documentation validation must check workflow safety."
    )


def _validate_tag_job(job: object) -> None:
    if not isinstance(job, dict):
        raise ReleaseWorkflowError("Tag validation must be a job mapping.")
    expected_condition = (
        "github.ref_type == 'tag' || "
        "(github.event_name == 'workflow_dispatch' && inputs.release_tag != '')"
    )
    if job.get("if") != expected_condition:
        raise ReleaseWorkflowError(
            "Only tags or explicit manual recovery tags may enter the release pipeline."
        )
    outputs = job.get("outputs")
    if not isinstance(outputs, dict) or set(outputs) != {"tag", "version", "commit", "is_stable"}:
        raise ReleaseWorkflowError("Tag validation must expose only the release identity fields.")
    commands = _job_commands(job)
    _require(commands, "semver_pattern=", "Release tags must use an explicit SemVer pattern.")
    _require(commands, 'git rev-parse "$tag_ref^{}"', "Release commits must resolve from tags.")
    _require(
        commands,
        'echo "commit=$commit"',
        "Release recovery must pass the tag commit to downstream jobs.",
    )
    _require(
        commands, 'git cat-file -t "$tag_ref"', "Release recovery must require annotated tags."
    )
    _require(
        commands,
        'git cat-file -p "$tag_ref"',
        "Release recovery tags must directly target commits.",
    )
    _require(
        commands,
        'git cat-file -t "$TAG^{}"',
        "Release recovery tags must resolve to commits.",
    )
    _require(
        commands,
        "Release checkout does not match tag",
        "Release recovery must check out the exact immutable tag.",
    )
    if "github.sha" in commands:
        raise ReleaseWorkflowError("Release recovery must derive commits from the immutable tag.")
    _require(commands, "pyproject.toml", "Release tags must match the package version.")
    _require(
        commands,
        "does not match pyproject.toml version",
        "Release tags must reject package-version mismatches.",
    )
    _require(commands, "is_stable=false", "Pre-release tags must be identified explicitly.")
    if _checkout_refs(job) != [_release_checkout_ref()] or _checkout_fetch_depths(job) != ["0"]:
        raise ReleaseWorkflowError(
            "Release validation must check out the exact tag or recovery tag."
        )


def _validate_publish_job(job: object) -> None:
    if not isinstance(job, dict) or job.get("permissions") != {"contents": "write"}:
        raise ReleaseWorkflowError("Versioned docs require only contents: write permission.")
    commands = _job_commands(job)
    if _checkout_refs(job) != [
        "${{ needs.validate-release.outputs.tag }}"
    ] or _checkout_fetch_depths(job) != ["0"]:
        raise ReleaseWorkflowError(
            "Versioned documentation must check out the validated release tag."
        )
    _require(
        commands,
        'git config user.name "github-actions[bot]"',
        "Versioned documentation commits require an explicit bot identity.",
    )
    _require(
        commands,
        'git config user.email "41898282+github-actions[bot]@users.noreply.github.com"',
        "Versioned documentation commits require an explicit bot email.",
    )
    _require(
        commands, "mike list --json", "Versioned documentation must check deployed versions first."
    )
    _require(
        commands,
        "git ls-remote --exit-code --heads origin gh-pages",
        "The Pages branch must be discovered before deployment.",
    )
    _require(
        commands,
        "first documentation release",
        "A missing Pages branch must be accepted for the first release.",
    )
    recovery_environment = _named_step_environment(
        job, "Refuse to replace immutable versioned documentation"
    )
    expected_recovery_environment = {
        "VERSION": "${{ needs.validate-release.outputs.version }}",
        "COMMIT": "${{ needs.validate-release.outputs.commit }}",
        "ALLOW_EXISTING_DOCUMENTATION": (
            "${{ github.event_name == 'workflow_dispatch' && inputs.release_tag != '' }}"
        ),
    }
    if recovery_environment != expected_recovery_environment:
        raise ReleaseWorkflowError(
            "Existing documentation recovery must use only the validated release identity."
        )
    _require(
        commands,
        'if [[ "$ALLOW_EXISTING_DOCUMENTATION" != "true" ]]; then',
        "Existing versioned docs must be rejected outside explicit manual recovery.",
    )
    _require(
        commands,
        "git log origin/gh-pages --format=%s",
        "Existing documentation recovery must verify deployment provenance.",
    )
    _require(
        commands,
        "does not prove deployment from release commit",
        "Existing documentation recovery must reject unproven deployment provenance.",
    )
    _require(
        commands,
        'echo "DOCUMENTATION_ALREADY_PUBLISHED=true" >> "$GITHUB_ENV"',
        "Proven existing documentation must be retained without another deployment.",
    )
    _require(
        commands,
        'if [[ "${DOCUMENTATION_ALREADY_PUBLISHED:-false}" == "true" ]]; then',
        "Documentation publishing must skip an already proven immutable version.",
    )
    _require(
        commands, "already exists and is immutable", "Existing versioned docs must be rejected."
    )
    _require(
        commands,
        "mike deploy --push --update-aliases --alias-type redirect",
        "Stable releases must update latest through a Pages-compatible redirect.",
    )
    _require(
        commands,
        "mike set-default --push latest",
        "Stable releases must redirect the root to latest.",
    )
    _require(
        commands, 'mike deploy --push "$VERSION"', "Pre-releases must deploy their own version."
    )
    _require(
        commands,
        'if [[ "$IS_STABLE" == "true" ]]; then',
        "Only stable releases may update latest and the root redirect.",
    )


def _validate_github_release_job(job: object) -> None:
    if not isinstance(job, dict) or job.get("permissions") != {"contents": "write"}:
        raise ReleaseWorkflowError(
            "GitHub Release creation requires only contents: write permission."
        )
    expected_dependencies = [
        "validate-release",
        "publish-versioned-documentation",
        "publish-python-package",
    ]
    if job.get("needs") != expected_dependencies:
        raise ReleaseWorkflowError(
            "GitHub Release creation must wait for documentation and PyPI publication."
        )
    expected_condition = (
        "needs.publish-versioned-documentation.result == 'success' "
        "&& needs.publish-python-package.result == 'success'"
    )
    if job.get("if") != expected_condition:
        raise ReleaseWorkflowError(
            "GitHub Release creation requires successful documentation and PyPI publication."
        )
    commands = _job_commands(job)
    _require(
        commands,
        'gh release view "$TAG" --repo "$LIBRARY_REPOSITORY"',
        "GitHub Release lookup must name the fixed repository.",
    )
    _require(
        commands, "gh release create", "A successful docs deployment must create a GitHub Release."
    )
    _require(
        commands,
        'gh release create "$TAG" "${release_flags[@]}" --repo "$LIBRARY_REPOSITORY"',
        "GitHub Release creation must name the fixed repository.",
    )


def _validate_pypi_publish_job(job: object) -> None:
    if not isinstance(job, dict) or job.get("permissions") != {"contents": "read"}:
        raise ReleaseWorkflowError("PyPI publication must retain read-only repository access.")
    expected_dependencies = ["validate-release", "publish-versioned-documentation"]
    if job.get("needs") != expected_dependencies:
        raise ReleaseWorkflowError("PyPI publication must wait for immutable documentation.")
    if job.get("if") != "needs.publish-versioned-documentation.result == 'success'":
        raise ReleaseWorkflowError("PyPI publication requires successful documentation.")
    if _checkout_refs(job) != [
        "${{ needs.validate-release.outputs.tag }}"
    ] or _checkout_fetch_depths(job) != ["0"]:
        raise ReleaseWorkflowError("PyPI publication must check out the validated release tag.")
    _require(
        _job_commands(job),
        "poetry build",
        "PyPI publication must build the validated package locally.",
    )
    publish_step = _step_using(job, PYPI_PUBLISH_ACTION)
    expected_inputs = {
        "user": "__token__",
        "password": "${{ secrets.PYPI_API_TOKEN }}",
        "packages-dir": "dist/",
        "skip-existing": (
            "${{ github.event_name == 'workflow_dispatch' && inputs.release_tag != '' }}"
        ),
    }
    if publish_step.get("with") != expected_inputs:
        raise ReleaseWorkflowError(
            "PyPI publication must use only the scoped token and recovery-safe inputs."
        )
    if "PYPI_API_TOKEN" in _job_commands(job):
        raise ReleaseWorkflowError("The PyPI token must never enter a shell command.")


def _validate_portal_dispatch_job(job: object) -> None:
    if not isinstance(job, dict) or job.get("permissions") != {}:
        raise ReleaseWorkflowError("Portal dispatch must not receive a repository token.")
    expected_dependencies = [
        "validate-release",
        "publish-versioned-documentation",
        "publish-python-package",
        "create-github-release",
    ]
    if job.get("needs") != expected_dependencies:
        raise ReleaseWorkflowError(
            "Portal dispatch must wait for the GitHub Release record after documentation."
        )
    expected_condition = (
        "needs.publish-versioned-documentation.result == 'success' "
        "&& needs.publish-python-package.result == 'success' "
        "&& needs.create-github-release.result == 'success'"
    )
    if job.get("if") != expected_condition:
        raise ReleaseWorkflowError(
            "Portal dispatch must require successful documentation and GitHub Release record jobs."
        )
    commands = _job_commands(job)
    environment = _job_environment(job)
    if environment.get("PORTAL_TOKEN") != "${{ secrets.LIBRARY_PORTAL_DISPATCH_TOKEN }}":
        raise ReleaseWorkflowError("Portal dispatch must use only LIBRARY_PORTAL_DISPATCH_TOKEN.")
    if "secrets." in commands:
        raise ReleaseWorkflowError(
            "Portal dispatch secrets must be scoped to its environment only."
        )
    _require(
        commands,
        "LIBRARY_PORTAL_DISPATCH_TOKEN is unavailable",
        "Missing portal tokens must skip clearly.",
    )
    _require(
        commands,
        'gh workflow run "$PORTAL_WORKFLOW"',
        "Portal hand-off must use workflow_dispatch.",
    )
    _require(
        commands,
        '-f "repository=$LIBRARY_REPOSITORY"',
        "Portal hand-off must include the library repository.",
    )
    _require(commands, '-f "tag=$TAG"', "Portal hand-off must include the release tag.")
    _require(commands, '-f "version=$VERSION"', "Portal hand-off must include the release version.")
    _require(commands, '-f "commit=$COMMIT"', "Portal hand-off must include the release commit.")
    if "curl " in commands:
        raise ReleaseWorkflowError("Portal hand-off must use the authenticated GitHub CLI.")


def _job_commands(job: dict[str, Any]) -> str:
    steps = job.get("steps")
    if not isinstance(steps, list):
        raise ReleaseWorkflowError("Release workflow jobs must define steps.")
    return "\n".join(str(step.get("run", "")) for step in steps if isinstance(step, dict))


def _job_environment(job: dict[str, Any]) -> dict[str, str]:
    steps = job.get("steps")
    if not isinstance(steps, list):
        return {}
    for step in steps:
        if not isinstance(step, dict):
            continue
        environment = step.get("env")
        if isinstance(environment, dict) and "PORTAL_TOKEN" in environment:
            return {str(key): str(value) for key, value in environment.items()}
    return {}


def _named_step_environment(job: object, name: str) -> dict[str, str]:
    if not isinstance(job, dict):
        return {}
    steps = job.get("steps")
    if not isinstance(steps, list):
        return {}
    for step in steps:
        if not isinstance(step, dict) or step.get("name") != name:
            continue
        environment = step.get("env")
        if isinstance(environment, dict):
            return {str(key): str(value) for key, value in environment.items()}
    return {}


def _step_using(job: dict[str, Any], action: str) -> dict[str, Any]:
    steps = job.get("steps")
    if not isinstance(steps, list):
        raise ReleaseWorkflowError("Release workflow jobs must define steps.")
    matching_steps = [
        step for step in steps if isinstance(step, dict) and step.get("uses") == action
    ]
    if len(matching_steps) != 1:
        raise ReleaseWorkflowError(f"Release workflow must use {action} exactly once.")
    return matching_steps[0]


def _checkout_refs(job: dict[str, Any]) -> list[str]:
    steps = job.get("steps")
    if not isinstance(steps, list):
        return []
    refs: list[str] = []
    for step in steps:
        if not isinstance(step, dict) or step.get("uses") != "actions/checkout@v5":
            continue
        with_values = step.get("with")
        if isinstance(with_values, dict) and "ref" in with_values:
            refs.append(str(with_values["ref"]))
    return refs


def _checkout_fetch_depths(job: dict[str, Any]) -> list[str]:
    steps = job.get("steps")
    if not isinstance(steps, list):
        return []
    depths: list[str] = []
    for step in steps:
        if not isinstance(step, dict) or step.get("uses") != "actions/checkout@v5":
            continue
        with_values = step.get("with")
        if isinstance(with_values, dict) and "fetch-depth" in with_values:
            depths.append(str(with_values["fetch-depth"]))
    return depths


def _release_checkout_ref() -> str:
    return (
        "${{ github.event_name == 'workflow_dispatch' "
        "&& format('refs/tags/{0}', inputs.release_tag) || github.ref }}"
    )


def _require(commands: str, expected: str, message: str) -> None:
    if expected not in commands:
        raise ReleaseWorkflowError(message)


if __name__ == "__main__":
    validate_release_workflow(Path(__file__).resolve().parents[1])
    print("Release documentation workflow is valid.")
