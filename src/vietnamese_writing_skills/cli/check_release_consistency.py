"""Verify release metadata and backend dependency mirrors stay aligned."""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACKAGE_NAME = "vietnamese-writing-skills"


def read_project_version(path: Path) -> str:
    with path.open("rb") as file:
        return tomllib.load(file)["project"]["version"]


def main() -> int:
    root_version = read_project_version(ROOT / "pyproject.toml")
    backend_pyproject = ROOT / "web" / "backend" / "pyproject.toml"
    backend_version = read_project_version(backend_pyproject)

    with backend_pyproject.open("rb") as file:
        backend_dependencies = tomllib.load(file)["project"]["dependencies"]
    expected_dependency = f"{PACKAGE_NAME}=={root_version}"

    requirements = (
        ROOT / "web" / "backend" / "requirements.txt"
    ).read_text(encoding="utf-8").splitlines()

    errors = []
    if backend_version != root_version:
        errors.append(
            f"backend version is {backend_version!r}; expected {root_version!r} "
            "from root pyproject.toml"
        )
    if expected_dependency not in backend_dependencies:
        errors.append(
            f"backend pyproject dependency must be {expected_dependency!r}"
        )
    if expected_dependency not in requirements:
        errors.append(
            f"backend requirements dependency must be {expected_dependency!r}"
        )

    if errors:
        print("Release consistency check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Release consistency check passed for {root_version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
