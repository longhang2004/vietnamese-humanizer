from __future__ import annotations

import argparse
from pathlib import Path

try:
    from scripts._shared import ROOT, iter_patterns
except ModuleNotFoundError:
    from _shared import ROOT, iter_patterns


def render(pattern_dir: Path) -> str:
    rows = sorted(
        (pattern for _, pattern in iter_patterns(pattern_dir)), key=lambda item: item["id"]
    )
    lines = [
        "# Danh mục pattern (được sinh tự động)",
        "",
        "> Không sửa trực tiếp file này. Chạy `python scripts/generate_pattern_docs.py` "
        "sau khi đổi YAML.",
        "",
        "| ID | Skill | Mức độ | Độ tin cậy | Tên | Tóm tắt |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for pattern in rows:
        summary = " ".join(pattern["summary"].split()).replace("|", "\\|")
        lines.append(
            f"| {pattern['id']} | {pattern['skill']} | {pattern['severity']} | "
            f"{pattern['confidence']} | `{pattern['name']}` | {summary} |"
        )
    lines.extend(["", f"Tổng cộng: **{len(rows)} pattern**.", ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sinh bảng pattern từ YAML")
    parser.add_argument("--patterns", type=Path, default=ROOT / "patterns")
    parser.add_argument("--output", type=Path, default=ROOT / "docs" / "generated-patterns.md")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    expected = render(args.patterns)
    if args.check:
        actual = args.output.read_text(encoding="utf-8") if args.output.exists() else ""
        if actual != expected:
            print(f"{args.output} chưa đồng bộ; hãy chạy generate_pattern_docs.py")
            return 1
        print(f"Generated docs đã đồng bộ: {args.output}")
        return 0
    args.output.write_text(expected, encoding="utf-8")
    print(f"Đã ghi {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
