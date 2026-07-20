from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from vietnamese_writing_skills.core.benchmark import (
    load_cases,
    summarize,
    validate_case,
    validate_results,
)
from vietnamese_writing_skills.core.paths import child, data_location, repository_root
from vietnamese_writing_skills.core.patterns import pattern_index

__all__ = ["load_cases", "summarize", "validate_case", "validate_results"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate và tổng hợp benchmark tiếng Việt")
    parser.add_argument("--root", type=Path, help="Repository cần xử lý")
    parser.add_argument("--cases", type=Path)
    parser.add_argument("--review-schema", type=Path)
    parser.add_argument("--results", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = repository_root(args.root)
        benchmark_dir = data_location("benchmarks", root)
        case_dir = args.cases or child(benchmark_dir, "cases")
        case_schema = child(benchmark_dir, "case.schema.json")
        review_schema = args.review_schema or child(benchmark_dir, "review-result.schema.json")
        known_ids = set(pattern_index(data_location("patterns", root)))
        cases, errors = load_cases(case_dir, known_ids, case_schema)
        results = None
        if args.results:
            results, result_errors = validate_results(
                args.results,
                review_schema,
                {case["id"]: case["expected_output_mode"] for case in cases},
            )
            errors.extend(result_errors)
    except (OSError, ValueError) as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 2
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
