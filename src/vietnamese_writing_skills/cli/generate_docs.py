from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from vietnamese_writing_skills.core.paths import data_location, repository_root
from vietnamese_writing_skills.core.patterns import iter_patterns


def _clean(value: str) -> str:
    return " ".join(value.split())


def render(pattern_dir: Any) -> str:
    rows = sorted(
        (pattern for _, pattern in iter_patterns(pattern_dir)),
        key=lambda item: item["id"],
    )
    lines = [
        "# Danh mục pattern (được sinh tự động)",
        "",
        "> Không sửa trực tiếp file này. Chạy `python scripts/generate_pattern_docs.py` "
        "sau khi đổi YAML.",
        "",
    ]
    for pattern in rows:
        lines.extend(
            [
                f"## {pattern['id']}: `{pattern['name']}`",
                "",
                f"- Skill: `{pattern['skill']}`",
                f"- Finding type: `{pattern['finding_type']}`",
                f"- Scope / aggregation: `{pattern['scope']}` / `{pattern['aggregation']}`",
                f"- Severity / confidence: `{pattern['severity']}` / `{pattern['confidence']}`",
                f"- False-positive risk: `{pattern['false_positive_risk']}`",
                f"- Tóm tắt: {_clean(pattern['summary'])}",
                "- Rewrite strategy:",
            ]
        )
        lines.extend(f"  - {_clean(item)}" for item in pattern["rewrite_strategy"])
        lines.append("- Exceptions:")
        lines.extend(f"  - {_clean(item)}" for item in pattern["exceptions"])
        lines.append("")
    lines.extend([f"Tổng cộng: **{len(rows)} pattern**.", ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sinh tài liệu pattern từ YAML")
    parser.add_argument("--root", type=Path, help="Repository cần xử lý")
    parser.add_argument("--patterns", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    root = repository_root(args.root)
    pattern_dir = args.patterns or data_location("patterns", root)
    output = args.output or ((root / "docs" / "generated-patterns.md") if root else None)
    if output is None:
        parser.error("--output hoặc repository root là bắt buộc khi chạy ngoài source checkout")
    expected = render(pattern_dir)
    if args.check:
        actual = output.read_text(encoding="utf-8") if output.exists() else ""
        if actual != expected:
            print(f"{output} chưa đồng bộ; hãy chạy generate_pattern_docs.py")
            return 1
        print(f"Generated docs đã đồng bộ: {output}")
        return 0
    output.write_text(expected, encoding="utf-8")
    print(f"Đã ghi {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
