from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
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


def iter_patterns(pattern_dir: Path | None = None) -> Iterable[tuple[Path, dict[str, Any]]]:
    directory = pattern_dir or ROOT / "patterns"
    for path in sorted(directory.glob("*.yml")):
        document = load_yaml(path)
        if not isinstance(document, dict) or not isinstance(document.get("patterns"), list):
            continue
        for pattern in document["patterns"]:
            if isinstance(pattern, dict):
                yield path, pattern
