from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from vietnamese_writing_skills.core.paths import child, data_location, repository_root, sorted_files
from vietnamese_writing_skills.core.patterns import load_json, load_yaml, path_label


def validate_catalog(pattern_dir: Any, schema_path: Any, docs_path: Path | None) -> list[str]:
    errors: list[str] = []
    validator = Draft202012Validator(load_json(schema_path))
    seen_ids: dict[str, Any] = {}
    seen_names: dict[tuple[str, str], Any] = {}
    docs = docs_path.read_text(encoding="utf-8") if docs_path and docs_path.exists() else ""
    files = sorted_files(pattern_dir, ".yml")
    if not files:
        return [f"{pattern_dir}: không có catalog .yml"]
    for path in files:
        try:
            document = load_yaml(path)
        except Exception as exc:  # PyYAML cung cấp vị trí trong thông báo
            errors.append(f"{path_label(path)}: YAML không hợp lệ: {exc}")
            continue
        for issue in sorted(validator.iter_errors(document), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in issue.absolute_path) or "<root>"
            errors.append(f"{path_label(path)}:{location}: {issue.message}")
        if not isinstance(document, dict) or not isinstance(document.get("patterns"), list):
            continue
        for pattern in document["patterns"]:
            if not isinstance(pattern, dict):
                continue
            pattern_id = pattern.get("id")
            skill = pattern.get("skill")
            name = pattern.get("name")
            if isinstance(pattern_id, str):
                if pattern_id in seen_ids:
                    errors.append(
                        f"{path_label(path)}: ID {pattern_id} trùng với "
                        f"{seen_ids[pattern_id]}"
                    )
                seen_ids[pattern_id] = path_label(path)
                if docs_path and pattern_id not in docs:
                    errors.append(f"{path_label(path)}: {pattern_id} chưa có trong {docs_path}")
            if isinstance(skill, str) and isinstance(name, str):
                key = (skill, name)
                if key in seen_names:
                    errors.append(f"{path_label(path)}: name {name!r} trùng trong {skill}")
                seen_names[key] = path
            signals = pattern.get("signals", {})
            if isinstance(signals, dict):
                flags = 0 if pattern.get("case_sensitive", False) else re.IGNORECASE
                for expression in signals.get("regex", []):
                    try:
                        re.compile(expression, flags=flags)
                    except re.error as exc:
                        errors.append(
                            f"{path_label(path)}: {pattern_id}: regex không hợp lệ "
                            f"{expression!r}: {exc}"
                        )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Kiểm tra pattern YAML theo schema")
    parser.add_argument("--root", type=Path, help="Repository cần kiểm tra")
    parser.add_argument("--patterns", type=Path)
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--docs", type=Path)
    args = parser.parse_args(argv)
    try:
        root = repository_root(args.root)
        pattern_dir = args.patterns or data_location("patterns", root)
        schema_path = args.schema or child(pattern_dir, "schema.json")
        docs_path = args.docs
        if docs_path is None and root is not None:
            docs_path = root / "docs" / "generated-patterns.md"
        errors = validate_catalog(pattern_dir, schema_path, docs_path)
    except (OSError, ValueError) as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("Pattern validation thất bại:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    count = sum(len(load_yaml(path)["patterns"]) for path in sorted_files(pattern_dir, ".yml"))
    file_count = len(sorted_files(pattern_dir, ".yml"))
    print(f"Pattern validation đạt: {count} pattern trong {file_count} file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
