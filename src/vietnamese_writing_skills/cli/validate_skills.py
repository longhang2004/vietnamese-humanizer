from __future__ import annotations

import argparse
import sys
from pathlib import Path

from vietnamese_writing_skills.core.frontmatter import (
    parse_frontmatter,
    validate_all,
    validate_skill,
)
from vietnamese_writing_skills.core.paths import data_location, repository_root

__all__ = ["parse_frontmatter", "validate_all", "validate_skill"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Kiểm tra cấu trúc Agent Skills")
    parser.add_argument("path", nargs="?", type=Path)
    parser.add_argument("--root", type=Path, help="Repository cần kiểm tra")
    args = parser.parse_args(argv)
    try:
        root = repository_root(args.root)
        skills_dir = args.path.resolve() if args.path else data_location("skills", root)
        errors = validate_all(skills_dir)
    except (OSError, ValueError) as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("Skill validation thất bại:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    count = sum(item.is_dir() for item in skills_dir.iterdir())
    print(f"Skill validation đạt: {count} thư mục skill.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
