"""Repository hygiene for the SDK.

Given a fresh checkout / When the package is imported / Then it is typed, versioned and locked,
which is what ``uv sync --locked`` and ``mypy --strict`` need before W4 fills in the client.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import mfx

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE = REPO_ROOT / "src" / "mfx"


def test_package_exposes_a_version() -> None:
    assert mfx.__version__


def test_package_ships_py_typed() -> None:
    """Typed end to end, so consumers get the types from the wheel."""
    assert (PACKAGE / "py.typed").is_file()


def test_lockfile_is_committed() -> None:
    assert (REPO_ROOT / "uv.lock").is_file()


def test_the_contract_guard_asks_for_an_open_pull_request_not_for_any() -> None:
    """Given the workflow that re-vendors the contract and opens the pull request for it
    When it decides whether one is needed
    Then it lists the *open* pull requests from its branch, and never asks whether the branch has
    one at all: that question is answered by a pull request merged days ago.

    `gh pr view <branch>` found #24, merged on 3 Oct 2026, on every run after it, so the
    guard pushed its branch, opened nothing and ended green while the copy fell 2,700 lines behind
    in five days. The guard exists to end exactly that.
    """
    path = REPO_ROOT / ".github" / "workflows" / "spec-sync.yml"
    if not path.is_file():
        pytest.skip("the contract is re-vendored only in the repository the SDK is developed in")
    workflow = path.read_text(encoding="utf-8")
    steps = "\n".join(line for line in workflow.splitlines() if not line.lstrip().startswith("#"))

    assert "gh pr list --head chore/spec-sync --base develop --state open" in steps
    assert "gh pr view chore/spec-sync" not in steps
