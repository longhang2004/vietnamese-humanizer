from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

try:
    from scripts._shared import ROOT, load_yaml
except ModuleNotFoundError:
    from _shared import ROOT, load_yaml


def validate_catalog(pattern_dir: Path, schema_path: Path, docs_path: Path | None) -> list[str]:
    errors: list[str] = []
    schema = load_yaml(schema_path)
    validator = Draft202012Validator(schema)
    seen_ids: dict[str, Path] = {}
    seen_names: dict[tuple[str, str], Path] = {}
    docs = docs_path.read_text(encoding="utf-8") if docs_path and docs_path.exists() else ""
    files = sorted(pattern_dir.glob("*.yml"))
    if not files:
        return [f"{pattern_dir}: không có catalog .yml"]
    for path in files:
        try:
            document = load_yaml(path)
        except Exception as exc:  # PyYAML cung cấp vị trí cụ thể trong thông báo
            errors.append(f"{path}: YAML không hợp lệ: {exc}")
            continue
        for issue in sorted(validator.iter_errors(document), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in issue.absolute_path) or "<root>"
            errors.append(f"{path}:{location}: {issue.message}")
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
                    errors.append(f"{path}: ID {pattern_id} trùng với {seen_ids[pattern_id]}")
                seen_ids[pattern_id] = path
                if docs_path and pattern_id not in docs:
                    errors.append(f"{path}: {pattern_id} chưa có trong {docs_path}")
            if isinstance(skill, str) and isinstance(name, str):
                key = (skill, name)
                if key in seen_names:
                    errors.append(f"{path}: name {name!r} trùng trong {skill}")
                seen_names[key] = path
            signals = pattern.get("signals", {})
            if isinstance(signals, dict):
                flags = 0 if pattern.get("case_sensitive", False) else re.IGNORECASE
                for expression in signals.get("regex", []):
                    try:
                        re.compile(expression, flags=flags)
                    except re.error as exc:
                        errors.append(
                            f"{path}: {pattern_id}: regex không hợp lệ {expression!r}: {exc}"
                        )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Kiểm tra pattern YAML theo schema")
    parser.add_argument("--patterns", type=Path, default=ROOT / "patterns")
    parser.add_argument("--schema", type=Path, default=ROOT / "patterns" / "schema.json")
    parser.add_argument("--docs", type=Path, default=ROOT / "docs" / "generated-patterns.md")
    args = parser.parse_args(argv)
    errors = validate_catalog(args.patterns, args.schema, args.docs)
    if errors:
        print("Pattern validation thất bại:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    count = sum(len(load_yaml(path)["patterns"]) for path in args.patterns.glob("*.yml"))
    file_count = len(list(args.patterns.glob("*.yml")))
    print(f"Pattern validation đạt: {count} pattern trong {file_count} file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
