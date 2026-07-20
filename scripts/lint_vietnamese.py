from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any

try:
    from scripts._shared import iter_patterns
except ModuleNotFoundError:
    from _shared import iter_patterns

FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
URL_RE = re.compile(r"(?:https?://|www\.)\S+", flags=re.IGNORECASE)
IDENTIFIER_RE = re.compile(r"\b(?:[A-Za-z_][A-Za-z0-9_]*_[A-Za-z0-9_]+|[A-Za-z]+::[A-Za-z:]+)\b")
SENTENCE_RE = re.compile(r"[^.!?\n]+[.!?]?", flags=re.UNICODE)
WORD_RE = re.compile(r"[\wÀ-ỹĐđ]+", flags=re.UNICODE)
PRONOUN_GROUPS = (
    ("bạn", "quý khách", "người dùng", "khách hàng"),
    ("tôi", "chúng tôi", "chúng ta"),
)
SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def mask_protected(text: str) -> str:
    """Che nội dung không nên lint nhưng giữ nguyên newline và vị trí ký tự."""
    output: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in text.splitlines(keepends=True):
        fence = FENCE_RE.match(line)
        if fence and (not in_fence or line.lstrip().startswith(fence_marker)):
            marker = fence.group(1)
            output.append("".join("\n" if char == "\n" else " " for char in line))
            if in_fence:
                in_fence = False
                fence_marker = ""
            else:
                in_fence = True
                fence_marker = marker
            continue
        if in_fence:
            output.append("".join("\n" if char == "\n" else " " for char in line))
            continue
        masked = line
        for expression in (INLINE_CODE_RE, URL_RE, IDENTIFIER_RE):
            masked = expression.sub(lambda match: " " * len(match.group(0)), masked)
        output.append(masked)
    return "".join(output)


def _location(text: str, start: int) -> tuple[int, int]:
    line = text.count("\n", 0, start) + 1
    previous_newline = text.rfind("\n", 0, start)
    return line, start - previous_newline


def _excerpt(text: str, start: int, end: int, limit: int = 100) -> str:
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end < 0:
        line_end = len(text)
    excerpt = text[line_start:line_end].strip()
    return excerpt if len(excerpt) <= limit else excerpt[: limit - 1].rstrip() + "…"


def _issue(
    text: str,
    start: int,
    end: int,
    pattern_id: str,
    severity: str,
    message: str,
    suggestion: str,
) -> dict[str, Any]:
    line, column = _location(text, start)
    return {
        "pattern_id": pattern_id,
        "severity": severity,
        "line": line,
        "column": column,
        "excerpt": _excerpt(text, start, end),
        "message": message,
        "suggestion": suggestion,
    }


def _catalog_issues(text: str, masked: str, skills: set[str] | None) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for _, pattern in iter_patterns():
        if skills and pattern["skill"] not in skills:
            continue
        matches: list[re.Match[str]] = []
        signals = pattern.get("signals", {})
        flags = 0 if pattern.get("case_sensitive", False) else re.IGNORECASE
        for phrase in signals.get("phrases", []):
            matches.extend(re.finditer(re.escape(phrase), masked, flags=flags))
        for expression in signals.get("regex", []):
            matches.extend(re.finditer(expression, masked, flags=flags))
        excluded = {phrase.casefold() for phrase in signals.get("exclude_phrases", [])}
        matches = [match for match in matches if match.group(0).casefold() not in excluded]
        unique = {(match.start(), match.end()): match for match in matches}
        ordered = [unique[key] for key in sorted(unique)]
        threshold = pattern.get("min_occurrences", 2)
        if len(ordered) < threshold:
            continue
        strategy = pattern.get("rewrite_strategy", ["Xem lại cấu trúc này."])[0]
        message = " ".join(pattern["summary"].split())
        for match in ordered:
            issues.append(
                _issue(
                    text,
                    match.start(),
                    match.end(),
                    pattern["id"],
                    pattern["severity"],
                    message,
                    strategy,
                )
            )
    return issues


def _sentences(masked: str) -> list[tuple[re.Match[str], list[str]]]:
    output: list[tuple[re.Match[str], list[str]]] = []
    for match in SENTENCE_RE.finditer(masked):
        words = WORD_RE.findall(match.group(0))
        if words:
            output.append((match, words))
    return output


def _repeated_opening_issues(text: str, masked: str) -> list[dict[str, Any]]:
    sentences = _sentences(masked)
    issues: list[dict[str, Any]] = []
    for index in range(len(sentences) - 2):
        window = sentences[index : index + 3]
        openings = [words[0].casefold() for _, words in window]
        if len(set(openings)) != 1:
            continue
        match = window[0][0]
        issues.append(
            _issue(
                text,
                match.start(),
                match.end(),
                "VI-HUM-S01",
                "medium",
                f"Ba câu liên tiếp cùng mở đầu bằng “{openings[0]}”.",
                "Đổi chủ thể hoặc gộp câu nếu quan hệ giữa các ý cho phép.",
            )
        )
    return issues


def _uniform_length_issue(text: str, masked: str) -> list[dict[str, Any]]:
    sentences = _sentences(masked)
    lengths = [len(words) for _, words in sentences if len(words) >= 6]
    if len(lengths) < 5:
        return []
    average = sum(lengths) / len(lengths)
    variance = sum((length - average) ** 2 for length in lengths) / len(lengths)
    coefficient = math.sqrt(variance) / average if average else 1.0
    if coefficient >= 0.16:
        return []
    start = sentences[0][0].start()
    return [
        _issue(
            text,
            start,
            sentences[-1][0].end(),
            "VI-HUM-S04",
            "low",
            "Độ dài của ít nhất năm câu gần như đồng đều; đây chỉ là tín hiệu cần đọc lại.",
            "Đọc thành tiếng và chỉ tách hoặc gộp câu khi nhịp đều làm ý khó theo dõi.",
        )
    ]


def _pronoun_issues(text: str, masked: str) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    lower = masked.casefold()
    for group in PRONOUN_GROUPS:
        counts = {
            pronoun: len(re.findall(rf"(?<!\w){re.escape(pronoun)}(?!\w)", lower))
            for pronoun in group
        }
        present = [pronoun for pronoun, count in counts.items() if count]
        if len(present) < 2 or sum(counts.values()) < 3:
            continue
        first = min(lower.find(pronoun) for pronoun in present if lower.find(pronoun) >= 0)
        issues.append(
            _issue(
                text,
                first,
                first + len(present[0]),
                "VI-STY-P01",
                "medium",
                f"Đại từ có thể chưa nhất quán: {', '.join(present)}.",
                "Chọn cách xưng hô theo quan hệ với độc giả rồi rà toàn văn.",
            )
        )
    return issues


def lint_text(text: str, skills: set[str] | None = None) -> list[dict[str, Any]]:
    masked = mask_protected(text)
    issues = _catalog_issues(text, masked, skills)
    if not skills or "humanizer-vi" in skills:
        issues.extend(_repeated_opening_issues(text, masked))
        issues.extend(_uniform_length_issue(text, masked))
    if not skills or "style-guide-vi" in skills:
        issues.extend(_pronoun_issues(text, masked))
    unique: dict[tuple[str, int, int], dict[str, Any]] = {}
    for issue in issues:
        key = (issue["pattern_id"], issue["line"], issue["column"])
        unique[key] = issue
    return sorted(
        unique.values(),
        key=lambda item: (item["line"], item["column"], SEVERITY_ORDER[item["severity"]]),
    )


def lint_file(path: Path, skills: set[str] | None = None) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    issues = lint_text(text, skills)
    counts = Counter(issue["severity"] for issue in issues)
    return {
        "file": str(path),
        "summary": {
            "issues": len(issues),
            "high": counts["high"],
            "medium": counts["medium"],
            "low": counts["low"],
            "note": "Số tín hiệu cần review, không phải xác suất văn bản do AI tạo.",
        },
        "issues": issues,
    }


def _paths(target: Path, recursive: bool) -> Iterable[Path]:
    if target.is_file():
        yield target
    elif target.is_dir() and recursive:
        for path in sorted(target.rglob("*")):
            if path.is_file() and path.suffix.lower() in {".md", ".txt"}:
                yield path
    else:
        raise ValueError("đường dẫn phải là file, hoặc dùng --recursive với thư mục")


def _print_text(result: dict[str, Any]) -> None:
    print(f"{result['file']}: {result['summary']['issues']} tín hiệu cần review")
    for issue in result["issues"]:
        print(
            f"  {issue['line']}:{issue['column']} {issue['severity']} "
            f"{issue['pattern_id']} {issue['message']}"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lint heuristic bề mặt cho tiếng Việt; không phải công cụ phát hiện AI"
    )
    parser.add_argument("path", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--skill", action="append", dest="skills")
    args = parser.parse_args(argv)
    try:
        selected_skills = set(args.skills) if args.skills else None
        results = [
            lint_file(path, selected_skills) for path in _paths(args.path, args.recursive)
        ]
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        payload = results[0] if len(results) == 1 else results
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for result in results:
            _print_text(result)
    return 1 if any(result["summary"]["issues"] for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
