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

from vietnamese_writing_skills.core.paths import data_location, repository_root
from vietnamese_writing_skills.core.patterns import iter_patterns, pattern_index

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
FINDING_TYPES = ("error", "warning", "preference", "heuristic")
SPECIAL_PATTERN_IDS = {
    "VI-HUM-S01",
    "VI-HUM-S04",
    "VI-STY-N02",
    "VI-STY-P01",
    "VI-STY-T01",
    "VI-TRA-S05",
}


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
    line = text[line_start:line_end]
    leading = len(line) - len(line.lstrip())
    excerpt = line.strip()
    relative_start = max(0, start - line_start - leading)
    relative_end = min(len(excerpt), end - line_start - leading)
    if len(excerpt) <= limit:
        return excerpt

    matched_length = max(1, relative_end - relative_start)
    context_budget = max(0, limit - min(matched_length, limit) - 2)
    left_context = min(relative_start, context_budget // 2)
    right_context = min(len(excerpt) - relative_end, context_budget - left_context)
    remaining = context_budget - left_context - right_context
    if remaining:
        extra_left = min(relative_start - left_context, remaining)
        left_context += extra_left
        remaining -= extra_left
        right_context += min(len(excerpt) - relative_end - right_context, remaining)

    clip_start = relative_start - left_context
    clip_end = relative_end + right_context
    prefix = "…" if clip_start > 0 else ""
    suffix = "…" if clip_end < len(excerpt) else ""
    return prefix + excerpt[clip_start:clip_end].strip() + suffix


def _occurrence(text: str, start: int, end: int) -> dict[str, Any]:
    line, column = _location(text, start)
    return {
        "line": line,
        "column": column,
        "excerpt": _excerpt(text, start, end),
        "matched_text": text[start:end],
    }


def _issue(
    text: str,
    start: int,
    end: int,
    pattern: dict[str, Any],
    message: str | None = None,
    suggestion: str | None = None,
    occurrence_spans: list[tuple[int, int]] | None = None,
) -> dict[str, Any]:
    spans = occurrence_spans or [(start, end)]
    occurrences = [_occurrence(text, span_start, span_end) for span_start, span_end in spans]
    first = occurrences[0]
    return {
        "pattern_id": pattern["id"],
        "finding_type": pattern["finding_type"],
        "severity": pattern["severity"],
        "confidence": pattern["confidence"],
        "scope": pattern["scope"],
        "line": first["line"],
        "column": first["column"],
        "excerpt": first["excerpt"],
        "message": message or " ".join(pattern["summary"].split()),
        "suggestion": suggestion or pattern["rewrite_strategy"][0],
        "occurrences": occurrences,
    }


def _signal_matches(masked: str, pattern: dict[str, Any]) -> list[re.Match[str]]:
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
    return [unique[key] for key in sorted(unique)]


def _catalog_issues(
    text: str,
    masked: str,
    pattern_dir: Any,
    skills: set[str] | None,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for _, pattern in iter_patterns(pattern_dir):
        if skills and pattern["skill"] not in skills:
            continue
        if pattern["id"] in SPECIAL_PATTERN_IDS:
            continue
        ordered = _signal_matches(masked, pattern)
        threshold = pattern.get("min_occurrences", 1)
        if len(ordered) < threshold:
            continue
        aggregation = pattern.get("aggregation", "single")
        if aggregation == "single":
            issues.extend(_issue(text, match.start(), match.end(), pattern) for match in ordered)
            continue
        first = ordered[0]
        issues.append(
            _issue(
                text,
                first.start(),
                first.end(),
                pattern,
                occurrence_spans=[(match.start(), match.end()) for match in ordered],
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


def _repeated_opening_issues(
    text: str,
    masked: str,
    patterns: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
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
                patterns["VI-HUM-S01"],
                f"Ba câu liên tiếp cùng mở đầu bằng “{openings[0]}”.",
                "Đổi chủ thể hoặc gộp câu nếu quan hệ giữa các ý cho phép.",
                occurrence_spans=[
                    (sentence_match.start(), sentence_match.start() + len(words[0]))
                    for sentence_match, words in window
                ],
            )
        )
    return issues


def _uniform_length_issue(
    text: str,
    masked: str,
    patterns: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    sentences = _sentences(masked)
    lengths = [len(words) for _, words in sentences if len(words) >= 6]
    if len(lengths) < 5:
        return []
    average = sum(lengths) / len(lengths)
    variance = sum((length - average) ** 2 for length in lengths) / len(lengths)
    coefficient = math.sqrt(variance) / average if average else 1.0
    if coefficient >= 0.16:
        return []
    return [
        _issue(
            text,
            sentences[0][0].start(),
            sentences[-1][0].end(),
            patterns["VI-HUM-S04"],
            "Độ dài của ít nhất năm câu gần như đồng đều; đây chỉ là tín hiệu cần đọc lại.",
            "Đọc thành tiếng và chỉ tách hoặc gộp câu khi nhịp đều làm ý khó theo dõi.",
        )
    ]


def _pronoun_issues(
    text: str,
    masked: str,
    patterns: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    lower = masked.casefold()
    for group in PRONOUN_GROUPS:
        alternatives = "|".join(
            re.escape(pronoun) for pronoun in sorted(group, key=len, reverse=True)
        )
        matches = list(re.finditer(rf"(?<!\w)(?:{alternatives})(?!\w)", lower))
        matched_pronouns = {match.group(0) for match in matches}
        present = [pronoun for pronoun in group if pronoun in matched_pronouns]
        if len(present) < 2 or len(matches) < 3:
            continue
        first = matches[0]
        issues.append(
            _issue(
                text,
                first.start(),
                first.end(),
                patterns["VI-STY-P01"],
                f"Đại từ có thể chưa nhất quán: {', '.join(present)}.",
                "Chọn cách xưng hô theo quan hệ với độc giả rồi rà toàn văn.",
                occurrence_spans=[(match.start(), match.end()) for match in matches],
            )
        )
    return issues


def _terminology_consistency_issues(
    text: str,
    masked: str,
    patterns: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    pattern = patterns["VI-STY-T01"]
    matches = _signal_matches(masked, pattern)
    variants = {" ".join(match.group(0).casefold().split()) for match in matches}
    if len(matches) < pattern.get("min_occurrences", 1) or len(variants) < 2:
        return []
    first = matches[0]
    return [
        _issue(
            text,
            first.start(),
            first.end(),
            pattern,
            f"Thuật ngữ có thể chưa nhất quán: {', '.join(sorted(variants))}.",
            occurrence_spans=[(match.start(), match.end()) for match in matches],
        )
    ]


def _percentage_consistency_issues(
    text: str,
    masked: str,
    patterns: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    pattern = patterns["VI-STY-N02"]
    matches = _signal_matches(masked, pattern)
    spacing_styles = {bool(re.search(r"\s+%$", match.group(0))) for match in matches}
    if len(matches) < pattern.get("min_occurrences", 1) or len(spacing_styles) < 2:
        return []
    first = matches[0]
    return [
        _issue(
            text,
            first.start(),
            first.end(),
            pattern,
            occurrence_spans=[(match.start(), match.end()) for match in matches],
        )
    ]


def _administrative_stack_issues(
    text: str,
    masked: str,
    patterns: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    pattern = patterns["VI-TRA-S05"]
    matches = _signal_matches(masked, pattern)
    threshold = pattern.get("min_occurrences", 1)
    issues: list[dict[str, Any]] = []
    for sentence_match, _ in _sentences(masked):
        sentence_matches = [
            match
            for match in matches
            if sentence_match.start() <= match.start() < sentence_match.end()
        ]
        if len(sentence_matches) < threshold:
            continue
        first = sentence_matches[0]
        issues.append(
            _issue(
                text,
                first.start(),
                first.end(),
                pattern,
                occurrence_spans=[
                    (match.start(), match.end()) for match in sentence_matches
                ],
            )
        )
    return issues


def lint_text(
    text: str,
    skills: set[str] | None = None,
    pattern_dir: Any | None = None,
) -> list[dict[str, Any]]:
    directory = pattern_dir or data_location("patterns")
    patterns = pattern_index(directory)
    masked = mask_protected(text)
    issues = _catalog_issues(text, masked, directory, skills)
    if not skills or "humanizer-vi" in skills:
        issues.extend(_repeated_opening_issues(text, masked, patterns))
        issues.extend(_uniform_length_issue(text, masked, patterns))
    if not skills or "style-guide-vi" in skills:
        issues.extend(_pronoun_issues(text, masked, patterns))
        issues.extend(_terminology_consistency_issues(text, masked, patterns))
        issues.extend(_percentage_consistency_issues(text, masked, patterns))
    if not skills or "translationese-cleaner-vi" in skills:
        issues.extend(_administrative_stack_issues(text, masked, patterns))
    unique: dict[tuple[str, int, int], dict[str, Any]] = {}
    for issue in issues:
        key = (issue["pattern_id"], issue["line"], issue["column"])
        unique[key] = issue
    return sorted(
        unique.values(),
        key=lambda item: (item["line"], item["column"], SEVERITY_ORDER[item["severity"]]),
    )


def lint_file(
    path: Path,
    skills: set[str] | None = None,
    pattern_dir: Any | None = None,
) -> dict[str, Any]:
    issues = lint_text(path.read_text(encoding="utf-8"), skills, pattern_dir)
    counts = Counter(issue["finding_type"] for issue in issues)
    return {
        "file": str(path),
        "summary": {
            "total": len(issues),
            **{finding_type: counts[finding_type] for finding_type in FINDING_TYPES},
            "note": "Số phát hiện cần review, không phải xác suất văn bản do AI tạo.",
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
    print(f"{result['file']}: {result['summary']['total']} phát hiện cần review")
    for issue in result["issues"]:
        label = issue["finding_type"].upper()
        print(
            f"  {issue['line']}:{issue['column']} {label} {issue['severity']} "
            f"{issue['pattern_id']} {issue['message']}"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lint heuristic bề mặt cho tiếng Việt; không phải công cụ phát hiện AI"
    )
    parser.add_argument("path", type=Path)
    parser.add_argument(
        "--root",
        type=Path,
        help="Repository chứa patterns/; mặc định tự phát hiện",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--skill", action="append", dest="skills")
    args = parser.parse_args(argv)
    try:
        root = repository_root(args.root)
        pattern_dir = data_location("patterns", root)
        selected_skills = set(args.skills) if args.skills else None
        results = [
            lint_file(path, selected_skills, pattern_dir)
            for path in _paths(args.path, args.recursive)
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
    return 1 if any(result["summary"]["total"] for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
