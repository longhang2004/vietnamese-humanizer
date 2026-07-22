from vietnamese_writing_skills import __version__
from vietnamese_writing_skills.cli.lint import lint_text
from vietnamese_writing_skills.core.patterns import pattern_index

from app.schemas import IssueItem, LintResponse, LintSummary, PatternItem


def run_linter(text: str, skills: list[str] | None = None) -> LintResponse:
    skills_set = set(skills) if skills else None
    raw_issues = lint_text(text, skills=skills_set)

    issues: list[IssueItem] = []
    finding_counts = {
        "error": 0,
        "warning": 0,
        "preference": 0,
        "heuristic": 0,
    }

    for item in raw_issues:
        issue = IssueItem(
            pattern_id=item["pattern_id"],
            finding_type=item["finding_type"],
            severity=item["severity"],
            confidence=item["confidence"],
            scope=item["scope"],
            line=item["line"],
            column=item["column"],
            excerpt=item["excerpt"],
            message=item["message"],
            suggestion=item["suggestion"],
            occurrences=item["occurrences"],
        )
        issues.append(issue)
        ftype = item["finding_type"]
        if ftype in finding_counts:
            finding_counts[ftype] += 1

    summary = LintSummary(
        total=len(issues),
        error=finding_counts["error"],
        warning=finding_counts["warning"],
        preference=finding_counts["preference"],
        heuristic=finding_counts["heuristic"],
    )

    return LintResponse(
        version=__version__,
        summary=summary,
        issues=issues,
    )


def get_patterns_list() -> list[PatternItem]:
    index = pattern_index()
    patterns: list[PatternItem] = []

    for pat in index.values():
        strategies = pat.get("rewrite_strategy", [])
        if isinstance(strategies, list):
            strategy = strategies[0] if strategies else ""
        else:
            strategy = str(strategies)

        item = PatternItem(
            id=pat["id"],
            name=pat.get("name", ""),
            skill=pat.get("skill", ""),
            category=pat.get("category", ""),
            finding_type=pat.get("finding_type", "heuristic"),
            severity=pat.get("severity", "low"),
            summary=pat.get("summary", ""),
            why_it_matters=pat.get("why_it_matters", ""),
            rewrite_strategy=strategy,
        )
        patterns.append(item)

    return patterns
