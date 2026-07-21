import json
import re
from collections import Counter
from pathlib import Path

from vietnamese_writing_skills.cli.generate_docs import render
from vietnamese_writing_skills.core.benchmark import (
    load_cases,
    summarize,
    validate_case,
    validate_results,
)
from vietnamese_writing_skills.core.patterns import load_jsonl, pattern_index

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")
PATTERN_IDS = set(pattern_index(ROOT / "patterns"))
REVIEW_SCHEMA = ROOT / "benchmarks" / "review-result.schema.json"


def review(
    case_id: str,
    reviewer_id: str = "reviewer-01",
    blockers: list[str] | None = None,
    output_mode: str = "clean_rewrite",
    output_mode_correct: bool = True,
) -> dict:
    return {
        "case_id": case_id,
        "system": "candidate-system",
        "reviewer_id": reviewer_id,
        "output_mode": output_mode,
        "output_mode_correct": output_mode_correct,
        "scores": {
            "naturalness": 4,
            "clarity": 5,
            "meaning_preservation": 5,
            "factual_preservation": 5,
            "register_fit": 4,
            "terminology_consistency": 5,
            "edit_necessity": 4,
            "over_editing_avoidance": 5,
        },
        "blockers": blockers or [],
        "notes": "",
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )


def test_benchmark_loader_reads_all_cases() -> None:
    cases, errors = load_cases(ROOT / "benchmarks" / "cases", PATTERN_IDS)
    assert errors == []
    assert len(cases) == 30
    assert all(
        "context" in case and "blockers" in case and "expected_output_mode" in case
        for case in cases
    )
    modes = {case["id"]: case["expected_output_mode"] for case in cases}
    assert modes["BENCH-HUM-001"] == "clean_rewrite"
    assert modes["BENCH-HUM-003"] == "review_comment"
    assert modes["BENCH-STY-002"] == "needs_author_decision"
    assert modes["BENCH-GRA-006"] == "no_change"


def test_benchmark_missing_context_is_reported(tmp_path: Path) -> None:
    case = {
        "id": "BENCH-HUM-999",
        "skill": "humanizer-vi",
        "domain": "technical",
        "register": "professional",
    }
    errors = validate_case(case, tmp_path / "case.jsonl", PATTERN_IDS)
    assert any("thiếu field context" in error for error in errors)


def test_manual_review_is_validated(tmp_path: Path) -> None:
    path = tmp_path / "reviews.jsonl"
    write_jsonl(path, [review("BENCH-HUM-001")])
    rows, errors = validate_results(
        path, REVIEW_SCHEMA, {"BENCH-HUM-001": "clean_rewrite"}
    )
    assert len(rows) == 1
    assert errors == []


def test_manual_review_missing_field_is_rejected(tmp_path: Path) -> None:
    row = review("BENCH-HUM-001")
    del row["reviewer_id"]
    path = tmp_path / "reviews.jsonl"
    write_jsonl(path, [row])
    _, errors = validate_results(path, REVIEW_SCHEMA, {"BENCH-HUM-001": "clean_rewrite"})
    assert any("reviewer_id" in error for error in errors)


def test_output_mode_mismatch_requires_blocker(tmp_path: Path) -> None:
    path = tmp_path / "reviews.jsonl"
    row = review(
        "BENCH-HUM-003",
        output_mode="clean_rewrite",
        output_mode_correct=False,
    )
    write_jsonl(path, [row])
    _, errors = validate_results(path, REVIEW_SCHEMA, {"BENCH-HUM-003": "review_comment"})
    assert any("incorrect_output_mode" in error for error in errors)

    row["blockers"] = ["incorrect_output_mode"]
    write_jsonl(path, [row])
    _, errors = validate_results(path, REVIEW_SCHEMA, {"BENCH-HUM-003": "review_comment"})
    assert errors == []


def test_output_mode_correct_must_match_expected_mode(tmp_path: Path) -> None:
    path = tmp_path / "reviews.jsonl"
    row = review("BENCH-GRA-006", output_mode="clean_rewrite")
    write_jsonl(path, [row])
    _, errors = validate_results(path, REVIEW_SCHEMA, {"BENCH-GRA-006": "no_change"})
    assert any("output_mode_correct" in error for error in errors)


def test_summary_averages_blocker_rate_and_unreviewed_count() -> None:
    cases, _ = load_cases(ROOT / "benchmarks" / "cases", PATTERN_IDS)
    results = [
        review("BENCH-HUM-001"),
        review("BENCH-HUM-001", "reviewer-02", ["fabricated_fact"]),
    ]
    summary = summarize(cases, results)
    assert summary["averages"]["clarity"] == 5
    assert summary["blocker_rate"] == 0.5
    assert summary["reviewers"] == 2
    assert summary["reviewed_cases"] == 1
    assert summary["unreviewed_cases"] == 29


def test_generated_pattern_docs_are_stable_and_complete() -> None:
    expected = render(ROOT / "patterns")
    actual = (ROOT / "docs" / "generated-patterns.md").read_text(encoding="utf-8")
    assert actual == expected
    assert "**40 pattern**" in actual
    assert "Finding type:" in actual
    assert "Scope / aggregation:" in actual
    assert "False-positive risk:" in actual
    assert "Rewrite strategy:" in actual
    assert "Good examples:" in actual
    assert "`clean_rewrite`:" in actual
    assert "`review_comment`:" in actual
    assert "`needs_author_decision`:" in actual
    assert "Exceptions:" in actual


def test_example_count_and_domain_distribution() -> None:
    examples = load_jsonl(ROOT / "examples" / "examples.jsonl")
    counts = Counter(example["domain"] for example in examples)
    assert len(examples) == 100
    assert counts == {
        "technical": 15,
        "work-email": 15,
        "blog": 15,
        "academic": 10,
        "product-description": 10,
        "marketing": 10,
        "customer-support": 10,
        "social-media": 10,
        "administrative": 5,
    }


def test_internal_markdown_links_resolve() -> None:
    broken: list[str] = []
    for document in ROOT.rglob("*.md"):
        ignored_dirs = {".git", ".venv", "node_modules", "dist", "build"}
        if any(part in ignored_dirs for part in document.parts):
            continue
        for target in LINK_RE.findall(document.read_text(encoding="utf-8")):
            clean = target.split("#", 1)[0].strip().strip("<>")
            if not clean or clean.startswith(("http://", "https://", "mailto:")):
                continue
            if not (document.parent / clean).exists():
                broken.append(f"{document.relative_to(ROOT)} -> {target}")
    assert broken == []


def test_public_docs_link_both_languages() -> None:
    pairs = (
        (ROOT / "README.md", ROOT / "README.vi.md"),
        (ROOT / "CONTRIBUTING.md", ROOT / "CONTRIBUTING.vi.md"),
    )

    for english, vietnamese in pairs:
        assert english.is_file()
        assert vietnamese.is_file()
        assert f"]({vietnamese.name})" in english.read_text(encoding="utf-8")
        assert f"]({english.name})" in vietnamese.read_text(encoding="utf-8")

    assert "](CONTRIBUTING.md)" in (ROOT / "README.md").read_text(encoding="utf-8")
    assert "](CONTRIBUTING.vi.md)" in (ROOT / "README.vi.md").read_text(
        encoding="utf-8"
    )


def test_public_docs_preserve_core_product_facts() -> None:
    facts = (
        "vietnamese-writing-skills",
        "humanizer-vi",
        "translationese-cleaner-vi",
        "grammar-checker-vi",
        "style-guide-vi",
        "clean_rewrite",
        "review_comment",
        "needs_author_decision",
        "no_change",
        "AI probability score",
        "detector",
        "python -m pip install .",
        "assets/donate-vietqr.png",
    )
    count_facts = (
        (ROOT / "README.md", ("40 patterns", "100 examples", "30 benchmark cases")),
        (ROOT / "README.vi.md", ("40 pattern", "100 example", "30 benchmark case")),
    )

    for document, document_count_facts in count_facts:
        contents = document.read_text(encoding="utf-8")
        for fact in facts:
            assert fact in contents, f"{document.name} is missing public fact: {fact}"
        for fact in document_count_facts:
            assert fact in contents, f"{document.name} is missing public fact: {fact}"


def test_donation_qr_is_published_in_both_readmes() -> None:
    qr_path = ROOT / "assets" / "donate-vietqr.png"
    assert qr_path.is_file()

    for readme in (ROOT / "README.md", ROOT / "README.vi.md"):
        assert "assets/donate-vietqr.png" in readme.read_text(encoding="utf-8")
