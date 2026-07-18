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
    if secret_names != ["LIBRARY_PORTAL_DISPATCH_TOKEN"]:
        raise ReleaseWorkflowError(
            "Only LIBRARY_PORTAL_DISPATCH_TOKEN may be referenced as a secret."
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
    commands = _job_commands(job)
    _require(commands, "make docs-check", "Documentation validation must build the site strictly.")
    _require(
        commands, "make workflow-check", "Documentation validation must check workflow safety."
    )


def _validate_tag_job(job: object) -> None:
    if not isinstance(job, dict):
        raise ReleaseWorkflowError("Tag validation must be a job mapping.")
    if job.get("if") != "github.ref_type == 'tag'":
        raise ReleaseWorkflowError("Only tags may enter the release pipeline.")
    outputs = job.get("outputs")
    if not isinstance(outputs, dict) or set(outputs) != {"tag", "version", "commit", "is_stable"}:
        raise ReleaseWorkflowError("Tag validation must expose only the release identity fields.")
    commands = _job_commands(job)
    _require(commands, "semver_pattern=", "Release tags must use an explicit SemVer pattern.")
    _require(commands, "pyproject.toml", "Release tags must match the package version.")
    _require(
        commands,
        "does not match pyproject.toml version",
        "Release tags must reject package-version mismatches.",
    )
    _require(commands, "is_stable=false", "Pre-release tags must be identified explicitly.")


def _validate_publish_job(job: object) -> None:
    if not isinstance(job, dict) or job.get("permissions") != {"contents": "write"}:
        raise ReleaseWorkflowError("Versioned docs require only contents: write permission.")
    commands = _job_commands(job)
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
    commands = _job_commands(job)
    _require(
        commands, "gh release create", "A successful docs deployment must create a GitHub Release."
    )
    if "pypi" in commands.lower() or "twine" in commands.lower():
        raise ReleaseWorkflowError("Release workflow must not publish packages.")


def _validate_portal_dispatch_job(job: object) -> None:
    if not isinstance(job, dict) or job.get("permissions") != {}:
        raise ReleaseWorkflowError("Portal dispatch must not receive a repository token.")
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


def _require(commands: str, expected: str, message: str) -> None:
    if expected not in commands:
        raise ReleaseWorkflowError(message)


if __name__ == "__main__":
    validate_release_workflow(Path(__file__).resolve().parents[1])
    print("Release documentation workflow is valid.")
