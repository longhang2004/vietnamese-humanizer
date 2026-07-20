from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml

from vietnamese_writing_skills.core.paths import data_location, sorted_files


def read_text(path: Any) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Any) -> Any:
    return yaml.safe_load(read_text(path))


def load_json(path: Any) -> Any:
    return json.loads(read_text(path))


def load_jsonl(path: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(read_text(path).splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: JSON không hợp lệ: {exc.msg}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: mỗi dòng phải là một JSON object")
        value["_source_line"] = line_number
        rows.append(value)
    return rows


def iter_patterns(pattern_dir: Any | None = None) -> Iterable[tuple[Any, dict[str, Any]]]:
    directory = pattern_dir or data_location("patterns")
    for path in sorted_files(directory, ".yml"):
        document = load_yaml(path)
        if not isinstance(document, dict) or not isinstance(document.get("patterns"), list):
            continue
        for pattern in document["patterns"]:
            if isinstance(pattern, dict):
                yield path, pattern


def pattern_index(pattern_dir: Any | None = None) -> dict[str, dict[str, Any]]:
    return {pattern["id"]: pattern for _, pattern in iter_patterns(pattern_dir)}


def path_label(path: Any) -> str:
    return str(path) if isinstance(path, Path) else getattr(path, "name", str(path))
