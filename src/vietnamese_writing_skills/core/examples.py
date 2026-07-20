from __future__ import annotations

from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

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
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
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
        status = review.get("status")
        reviewed_statuses = {
            "agent-reviewed",
            "maintainer-reviewed",
            "independently-reviewed",
        }
        if row.get("gold_rewrite") is True and status not in reviewed_statuses:
            errors.append(f"{prefix}: gold rewrite phải có preservation review và provenance")
        if row.get("gold_output_mode") is True and status not in reviewed_statuses:
            errors.append(f"{prefix}: gold output mode phải có preservation review và provenance")
        if row.get("gold_rewrite") is True and row.get("output_mode") in {
            "review_comment",
            "needs_author_decision",
        }:
            errors.append(f"{prefix}: review comment hoặc author decision không phải gold rewrite")
        if (
            row.get("gold_rewrite") is True
            and row.get("output_mode") == "no_change"
            and row.get("output") != row.get("input")
        ):
            errors.append(f"{prefix}: gold no_change phải có output trùng input")
        if status in reviewed_statuses:
            for field in ("reviewer_id", "review_method", "reviewed_at"):
                if not str(review.get(field, "")).strip():
                    errors.append(f"{prefix}: reviewed example phải có {field}")
        if status == "unreviewed" and row.get("gold_rewrite") is True:
            errors.append(f"{prefix}: unreviewed example không thể là gold rewrite")
    return rows, errors
