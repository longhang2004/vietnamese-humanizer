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


def core_dependencies(dependencies: list[str]) -> list[str]:
    return [
        dependency
        for dependency in dependencies
        if dependency.startswith(PACKAGE_NAME)
        and (
            len(dependency) == len(PACKAGE_NAME)
            or dependency[len(PACKAGE_NAME)] in " [<>=!~;@"
        )
    ]


def main(root: Path = ROOT) -> int:
    root_version = read_project_version(root / "pyproject.toml")
    backend_pyproject = root / "web" / "backend" / "pyproject.toml"
    backend_version = read_project_version(backend_pyproject)

    with backend_pyproject.open("rb") as file:
        backend_dependencies = tomllib.load(file)["project"]["dependencies"]
    expected_dependency = f"{PACKAGE_NAME}=={root_version}"

    requirements = (
        root / "web" / "backend" / "requirements.txt"
    ).read_text(encoding="utf-8").splitlines()

    errors = []
    if backend_version != root_version:
        errors.append(
            f"backend version is {backend_version!r}; expected {root_version!r} "
            "from root pyproject.toml"
        )
    if core_dependencies(backend_dependencies) != [expected_dependency]:
        errors.append(
            f"backend pyproject dependency must be {expected_dependency!r}"
        )
    if core_dependencies(requirements) != [expected_dependency]:
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
