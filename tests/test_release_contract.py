"""Release metadata must describe the same tested product version."""

from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

from vietnamese_writing_skills.cli.check_release_consistency import main

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_release_consistency.py"


def test_release_contract_is_consistent() -> None:
    result = subprocess.run(
        [sys.executable, str(CHECKER)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def test_backend_preview_resolves_core_from_repository() -> None:
    backend_project = tomllib.loads(
        (ROOT / "web" / "backend" / "pyproject.toml").read_text(encoding="utf-8")
    )

    assert backend_project["tool"]["uv"]["sources"]["vietnamese-writing-skills"] == {
        "path": "../.."
    }


def write_release_files(
    root: Path, backend_dependencies: list[str], requirements: list[str]
) -> None:
    (root / "pyproject.toml").write_text(
        "[project]\nversion = '0.4.1'\n", encoding="utf-8"
    )
    backend = root / "web" / "backend"
    backend.mkdir(parents=True)
    backend_dependencies_toml = ", ".join(repr(dependency) for dependency in backend_dependencies)
    (backend / "pyproject.toml").write_text(
        "[project]\n"
        "version = '0.4.1'\n"
        f"dependencies = [{backend_dependencies_toml}]\n",
        encoding="utf-8",
    )
    (backend / "requirements.txt").write_text(
        "\n".join(requirements), encoding="utf-8"
    )


@pytest.mark.parametrize(
    ("backend_dependencies", "requirements", "mirror"),
    [
        (
            ["vietnamese-writing-skills>=0.2.0"],
            ["vietnamese-writing-skills==0.4.1"],
            "pyproject",
        ),
        (
            [
                "vietnamese-writing-skills==0.4.1",
                "vietnamese-writing-skills>=0.2.0",
            ],
            ["vietnamese-writing-skills==0.4.1"],
            "pyproject",
        ),
        (
            ["vietnamese-writing-skills==0.4.1"],
            ["vietnamese-writing-skills>=0.2.0"],
            "requirements",
        ),
        (
            ["vietnamese-writing-skills==0.4.1"],
            [
                "vietnamese-writing-skills==0.4.1",
                "vietnamese-writing-skills>=0.2.0",
            ],
            "requirements",
        ),
    ],
)
def test_release_contract_rejects_conflicting_dependency_mirrors(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    backend_dependencies: list[str],
    requirements: list[str],
    mirror: str,
) -> None:
    write_release_files(tmp_path, backend_dependencies, requirements)

    assert main(tmp_path) == 1
    assert f"backend {mirror} dependency must be" in capsys.readouterr().err
