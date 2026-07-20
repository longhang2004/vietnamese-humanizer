from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from scripts._shared import ROOT, load_jsonl
except ModuleNotFoundError:
    from _shared import ROOT, load_jsonl

CASE_FIELDS = {
    "id": str,
    "skill": str,
    "domain": str,
    "register": str,
    "input": str,
    "constraints": list,
    "expected_patterns": list,
    "must_preserve": list,
    "must_not_add": list,
    "evaluation_notes": str,
}
SKILLS = {
    "humanizer-vi",
    "translationese-cleaner-vi",
    "grammar-checker-vi",
    "style-guide-vi",
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
BLOCKERS = (
    "fabricated_fact",
    "changed_number",
    "changed_proper_name",
    "changed_certainty",
    "changed_stance",
    "invented_source",
    "removed_condition",
    "incorrect_terminology",
)


def validate_case(case: dict[str, Any], source: Path) -> list[str]:
    line = case.get("_source_line", "?")
    prefix = f"{source}:{line}"
    errors: list[str] = []
    for field, expected_type in CASE_FIELDS.items():
        if field not in case:
            errors.append(f"{prefix}: thiếu field {field}")
        elif not isinstance(case[field], expected_type):
            errors.append(f"{prefix}: {field} phải có kiểu {expected_type.__name__}")
        elif isinstance(case[field], (str, list)) and not case[field]:
            errors.append(f"{prefix}: {field} không được rỗng")
    if case.get("skill") not in SKILLS:
        errors.append(f"{prefix}: skill không hợp lệ: {case.get('skill')!r}")
    pattern_ids = case.get("expected_patterns", [])
    if isinstance(pattern_ids, list) and not all(
        isinstance(item, str) and item.startswith("VI-") for item in pattern_ids
    ):
        errors.append(f"{prefix}: expected_patterns chứa ID không hợp lệ")
    return errors


def load_cases(case_dir: Path) -> tuple[list[dict[str, Any]], list[str]]:
    cases: list[dict[str, Any]] = []
    errors: list[str] = []
    seen: dict[str, Path] = {}
    for path in sorted(case_dir.glob("*.jsonl")):
        try:
            rows = load_jsonl(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for case in rows:
            errors.extend(validate_case(case, path))
            case_id = case.get("id")
            if isinstance(case_id, str):
                if case_id in seen:
                    errors.append(f"{path}: ID {case_id} trùng với {seen[case_id]}")
                seen[case_id] = path
            cases.append(case)
    if not cases:
        errors.append(f"{case_dir}: không có benchmark case")
    return cases, errors


def validate_results(path: Path, case_ids: set[str]) -> tuple[list[dict[str, Any]], list[str]]:
    rows = load_jsonl(path)
    errors: list[str] = []
    for row in rows:
        prefix = f"{path}:{row['_source_line']}"
        if row.get("id") not in case_ids:
            errors.append(f"{prefix}: benchmark id không tồn tại")
        scores = row.get("scores")
        if not isinstance(scores, dict):
            errors.append(f"{prefix}: thiếu scores object")
        else:
            for criterion in CRITERIA:
                score = scores.get(criterion)
                if not isinstance(score, int) or not 1 <= score <= 5:
                    errors.append(f"{prefix}: scores.{criterion} phải là số nguyên từ 1 đến 5")
        blockers = row.get("blockers")
        if not isinstance(blockers, dict):
            errors.append(f"{prefix}: thiếu blockers object")
        else:
            for blocker in BLOCKERS:
                if not isinstance(blockers.get(blocker), bool):
                    errors.append(f"{prefix}: blockers.{blocker} phải là boolean")
    return rows, errors


def summarize(
    cases: list[dict[str, Any]], results: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "cases": len(cases),
        "by_skill": dict(sorted(Counter(case["skill"] for case in cases).items())),
        "by_domain": dict(sorted(Counter(case["domain"] for case in cases).items())),
    }
    if results is not None:
        valid_rows = [row for row in results if isinstance(row.get("scores"), dict)]
        averages = {
            criterion: round(
                sum(row["scores"][criterion] for row in valid_rows) / len(valid_rows), 2
            )
            for criterion in CRITERIA
        } if valid_rows else {}
        blocker_count = sum(
            any(row.get("blockers", {}).values()) for row in valid_rows
        )
        summary["results"] = len(results)
        summary["averages"] = averages
        summary["failed_by_blocker"] = blocker_count
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate và tổng hợp benchmark tiếng Việt")
    parser.add_argument("--cases", type=Path, default=ROOT / "benchmarks" / "cases")
    parser.add_argument("--results", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args(argv)
    cases, errors = load_cases(args.cases)
    results: list[dict[str, Any]] | None = None
    if args.results:
        try:
            results, result_errors = validate_results(args.results, {case["id"] for case in cases})
            errors.extend(result_errors)
        except ValueError as exc:
            errors.append(str(exc))
    if errors:
        print("Benchmark validation thất bại:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    summary = summarize(cases, results)
    rendered = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.output and not args.validate_only:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
