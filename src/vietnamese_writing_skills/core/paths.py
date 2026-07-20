from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Any

PROJECT_MARKERS = ("pyproject.toml", "patterns", "skills")


def is_repository_root(path: Path) -> bool:
    return all((path / marker).exists() for marker in PROJECT_MARKERS)


def repository_root(explicit: Path | None = None) -> Path | None:
    if explicit is not None:
        root = explicit.expanduser().resolve()
        if not root.is_dir():
            raise ValueError(f"repository root không tồn tại: {root}")
        return root
    current = Path.cwd().resolve()
    for candidate in (current, *current.parents):
        if is_repository_root(candidate):
            return candidate
    return None


def data_location(name: str, root: Path | None = None) -> Any:
    if root is not None:
        return root / name
    discovered = repository_root()
    if discovered is not None:
        return discovered / name
    return resources.files("vietnamese_writing_skills").joinpath("data", name)


def child(location: Any, *parts: str) -> Any:
    for part in parts:
        location = location / part
    return location


def sorted_files(location: Any, suffix: str) -> list[Any]:
    if isinstance(location, Path):
        return sorted(
            path for path in location.iterdir() if path.is_file() and path.suffix == suffix
        )
    return sorted(
        (item for item in location.iterdir() if item.is_file() and item.name.endswith(suffix)),
        key=lambda item: item.name,
    )
