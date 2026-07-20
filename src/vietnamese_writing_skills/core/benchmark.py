from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from typing import Any

from jsonschema import Draft202012Validator

from vietnamese_writing_skills.core.paths import sorted_files
from vietnamese_writing_skills.core.patterns import load_json, load_jsonl, path_label

CASE_FIELDS = {
    "id": str,
    "skill": str,
    "domain": str,
    "register": str,
    "input": str,
    "context": str,
    "constraints": list,
    "expected_patterns": list,
    "expected_output_mode": str,
    "must_preserve": list,
    "must_not_add": list,
    "blockers": list,
    "evaluation_notes": str,
}
SKILLS = {
    "humanizer-vi",
    "translationese-cleaner-vi",
    "grammar-checker-vi",
    "style-guide-vi",
}
OUTPUT_MODES = {
    "clean_rewrite",
    "review_comment",
    "needs_author_decision",
    "no_change",
}
CRITERIA = (
    "naturalness",
    "clarity",
    "meaning_preservation",
    "factual_preservation",
    "register_fit",
    "terminology_consistency",
    "edit_necessity",
    "over_editing_avoidance",
)


def validate_case(
    case: dict[str, Any],
    source: Any,
    known_pattern_ids: set[str] | None = None,
) -> list[str]:
    line = case.get("_source_line", "?")
    prefix = f"{path_label(source)}:{line}"
    errors: list[str] = []
    for field, expected_type in CASE_FIELDS.items():
        if field not in case:
            errors.append(f"{prefix}: thiếu field {field}")
        elif not isinstance(case[field], expected_type):
            errors.append(f"{prefix}: {field} phải có kiểu {expected_type.__name__}")
        elif field not in {"context", "expected_patterns"} and isinstance(
            case[field], (str, list)
        ) and not case[field]:
            errors.append(f"{prefix}: {field} không được rỗng")
    if case.get("skill") not in SKILLS:
        errors.append(f"{prefix}: skill không hợp lệ: {case.get('skill')!r}")
    if case.get("expected_output_mode") not in OUTPUT_MODES:
        errors.append(
            f"{prefix}: expected_output_mode không hợp lệ: "
            f"{case.get('expected_output_mode')!r}"
        )
    pattern_ids = case.get("expected_patterns", [])
    if isinstance(pattern_ids, list):
        if not all(isinstance(item, str) and item.startswith("VI-") for item in pattern_ids):
            errors.append(f"{prefix}: expected_patterns chứa ID không hợp lệ")
        if known_pattern_ids is not None:
            for pattern_id in pattern_ids:
                if pattern_id not in known_pattern_ids:
                    errors.append(f"{prefix}: pattern ID không tồn tại: {pattern_id}")
    for field in ("constraints", "must_preserve", "must_not_add", "blockers"):
        values = case.get(field, [])
        if isinstance(values, list) and not all(
            isinstance(item, str) and item.strip() for item in values
        ):
            errors.append(f"{prefix}: {field} chỉ được chứa chuỗi không rỗng")
    return errors


def load_cases(
    case_dir: Any,
    known_pattern_ids: set[str] | None = None,
    schema_path: Any | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    cases: list[dict[str, Any]] = []
    errors: list[str] = []
    seen: dict[str, Any] = {}
    schema_validator = Draft202012Validator(load_json(schema_path)) if schema_path else None
    for path in sorted_files(case_dir, ".jsonl"):
        try:
            rows = load_jsonl(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for case in rows:
            errors.extend(validate_case(case, path, known_pattern_ids))
            if schema_validator is not None:
                value = {key: item for key, item in case.items() if key != "_source_line"}
                for issue in sorted(
                    schema_validator.iter_errors(value), key=lambda item: list(item.path)
                ):
                    location = ".".join(str(part) for part in issue.absolute_path) or "<root>"
                    errors.append(
                        f"{path_label(path)}:{case['_source_line']}:{location}: {issue.message}"
                    )
            case_id = case.get("id")
            if isinstance(case_id, str):
                if case_id in seen:
                    errors.append(f"{path}: ID {case_id} trùng với {seen[case_id]}")
                seen[case_id] = path
            cases.append(case)
    if not cases:
        errors.append(f"{case_dir}: không có benchmark case")
    return cases, errors


def validate_results(
    path: Any,
    schema_path: Any,
    expected_modes: Mapping[str, str],
) -> tuple[list[dict[str, Any]], list[str]]:
    rows = load_jsonl(path)
    validator = Draft202012Validator(load_json(schema_path))
    errors: list[str] = []
    seen: set[tuple[str, str, str]] = set()
    for row in rows:
        prefix = f"{path_label(path)}:{row['_source_line']}"
        value = {key: item for key, item in row.items() if key != "_source_line"}
        for issue in sorted(validator.iter_errors(value), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in issue.absolute_path) or "<root>"
            errors.append(f"{prefix}:{location}: {issue.message}")
        case_id = row.get("case_id")
        if case_id not in expected_modes:
            errors.append(f"{prefix}: benchmark case_id không tồn tại")
        else:
            expected_mode = expected_modes[case_id]
            actual_mode = row.get("output_mode")
            mode_correct = actual_mode == expected_mode
            if row.get("output_mode_correct") is not mode_correct:
                errors.append(
                    f"{prefix}: output_mode_correct phải là {str(mode_correct).lower()} "
                    f"khi expected={expected_mode!r} và actual={actual_mode!r}"
                )
            blockers = row.get("blockers", [])
            has_mode_blocker = (
                isinstance(blockers, list) and "incorrect_output_mode" in blockers
            )
            if not mode_correct and not has_mode_blocker:
                errors.append(f"{prefix}: output mode sai phải có blocker incorrect_output_mode")
            if mode_correct and has_mode_blocker:
                errors.append(f"{prefix}: không được gắn incorrect_output_mode khi mode đúng")
        key = (str(case_id), str(row.get("system")), str(row.get("reviewer_id")))
        if key in seen:
            errors.append(f"{prefix}: review bị trùng cho cùng case, system và reviewer")
        seen.add(key)
    return rows, errors


def summarize(
    cases: list[dict[str, Any]],
    results: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "cases": len(cases),
        "by_skill": dict(sorted(Counter(case["skill"] for case in cases).items())),
        "by_domain": dict(sorted(Counter(case["domain"] for case in cases).items())),
    }
    if results is None:
        return summary
    valid_rows = [row for row in results if isinstance(row.get("scores"), dict)]
    reviewed_case_ids = {row.get("case_id") for row in valid_rows}
    averages = (
        {
            criterion: round(
                sum(row["scores"][criterion] for row in valid_rows) / len(valid_rows),
                2,
            )
            for criterion in CRITERIA
        }
        if valid_rows
        else {}
    )
    blocker_rows = sum(bool(row.get("blockers")) for row in valid_rows)
    summary["reviews"] = len(valid_rows)
    summary["reviewed_cases"] = len(reviewed_case_ids)
    summary["unreviewed_cases"] = len({case["id"] for case in cases} - reviewed_case_ids)
    summary["reviewers"] = len({row.get("reviewer_id") for row in valid_rows})
    summary["averages"] = averages
    summary["blocker_reviews"] = blocker_rows
    summary["blocker_rate"] = round(blocker_rows / len(valid_rows), 4) if valid_rows else 0.0
    summary["agreement"] = "not calculated; raw scores are retained for independent review"
    return summary
