from __future__ import annotations

from typing import Any

from jsonschema import Draft202012Validator

from vietnamese_writing_skills.core.patterns import load_json, load_jsonl, path_label


def validate_examples(
    examples_path: Any,
    schema_path: Any,
    known_pattern_ids: set[str],
) -> tuple[list[dict[str, Any]], list[str]]:
    try:
        rows = load_jsonl(examples_path)
    except ValueError as exc:
        return [], [str(exc)]
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    seen: dict[str, int] = {}
    for row in rows:
        line = row.get("_source_line", "?")
        prefix = f"{path_label(examples_path)}:{line}"
        value = {key: item for key, item in row.items() if key != "_source_line"}
        for issue in sorted(validator.iter_errors(value), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in issue.absolute_path) or "<root>"
            errors.append(f"{prefix}:{location}: {issue.message}")
        example_id = row.get("id")
        if isinstance(example_id, str):
            if example_id in seen:
                errors.append(f"{prefix}: ID {example_id} trùng với dòng {seen[example_id]}")
            seen[example_id] = int(line)
        for pattern_id in row.get("patterns_triggered", []):
            if pattern_id not in known_pattern_ids:
                errors.append(f"{prefix}: pattern ID không tồn tại: {pattern_id}")
        review = row.get("preservation_review", {})
        if not isinstance(review, dict):
            review = {}
        if row.get("gold") is True and review.get("status") != "reviewed":
            errors.append(f"{prefix}: gold example phải có preservation_review.status=reviewed")
        if review.get("status") == "reviewed" and not str(review.get("review_notes", "")).strip():
            errors.append(f"{prefix}: reviewed example phải có review_notes")
    return rows, errors
