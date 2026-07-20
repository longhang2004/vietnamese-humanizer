from __future__ import annotations

import argparse
import sys
from pathlib import Path

from vietnamese_writing_skills.core.examples import validate_examples
from vietnamese_writing_skills.core.paths import child, data_location, repository_root
from vietnamese_writing_skills.core.patterns import pattern_index


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Kiểm tra corpus example và preservation metadata")
    parser.add_argument("--root", type=Path, help="Repository cần kiểm tra")
    parser.add_argument("--examples", type=Path)
    parser.add_argument("--schema", type=Path)
    args = parser.parse_args(argv)
    try:
        root = repository_root(args.root)
        example_dir = data_location("examples", root)
        examples_path = args.examples or child(example_dir, "examples.jsonl")
        schema_path = args.schema or child(example_dir, "schema.json")
        pattern_ids = set(pattern_index(data_location("patterns", root)))
        rows, errors = validate_examples(examples_path, schema_path, pattern_ids)
    except (OSError, ValueError) as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("Example validation thất bại:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    reviewed = sum(row["preservation_review"]["status"] != "unreviewed" for row in rows)
    print(f"Example validation đạt: {len(rows)} example, {reviewed} có provenance review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
