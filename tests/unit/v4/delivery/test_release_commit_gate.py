from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[4]
WORKFLOW_PATH = PROJECT_ROOT / ".github" / "workflows" / "release-documentation.yml"


def test_release_publication_requires_exact_branch_and_python_matrix_proof() -> None:
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    jobs = workflow["jobs"]
    gate = jobs["verify-release-commit"]
    assert gate["needs"] == "validate-release"
    assert gate["strategy"]["matrix"]["python-version"] == ["3.11", "3.12", "3.13"]
    commands = "\n".join(step.get("run", "") for step in gate["steps"] if isinstance(step, dict))
    assert "git fetch --no-tags origin main develop" in commands
    assert '"$RELEASE_COMMIT" != "$(git rev-parse origin/main)"' in commands
    assert '"$(git rev-parse origin/main)" != "$(git rev-parse origin/develop)"' in commands
    assert "make verify" in commands
    for job_name in (
        "publish-versioned-documentation",
        "publish-python-package",
        "create-github-release",
    ):
        needs = jobs[job_name]["needs"]
        assert "verify-release-commit" in (needs if isinstance(needs, list) else [needs])
