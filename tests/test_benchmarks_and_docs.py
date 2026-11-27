import json
import re
from collections import Counter
from pathlib import Path

from vietnamese_writing_skills.cli.benchmarks import main as benchmarks_main
from vietnamese_writing_skills.cli.generate_docs import render
from vietnamese_writing_skills.cli.lint import lint_text
from vietnamese_writing_skills.core.benchmark import (
    load_cases,
    prepare_review_packet,
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
    assert len(cases) >= 33
    assert all(
        "context" in case and "blockers" in case and "expected_output_mode" in case
        for case in cases
    )
    modes = {case["id"]: case["expected_output_mode"] for case in cases}
    assert modes["BENCH-HUM-001"] == "clean_rewrite"
    assert modes["BENCH-HUM-003"] == "review_comment"
    assert modes["BENCH-STY-002"] == "needs_author_decision"
    assert modes["BENCH-GRA-006"] == "no_change"


def test_long_naturalness_cases_cover_preservation_and_editorial_decisions() -> None:
    cases = load_jsonl(ROOT / "benchmarks" / "cases" / "naturalness.jsonl")
    assert len(cases) == 30
    assert all(150 <= len(case["input"].split()) <= 500 for case in cases)
    assert all("\n\n" in case["input"] for case in cases)
    assert {case["expected_output_mode"] for case in cases} == {
        "clean_rewrite",
        "no_change",
        "review_comment",
        "needs_author_decision",
    }
    assert any(case.get("style", {}).get("reduce_hype") for case in cases)
    assert any(case.get("style", {}).get("channel") == "spoken_script" for case in cases)


def test_writing_profiles_include_preservation_controls_and_decision_cases() -> None:
    cases = load_jsonl(ROOT / "benchmarks" / "cases" / "writing-profiles.jsonl")
    assert len(cases) == 24
    for profile in ("plain", "business", "technical"):
        selected = [case for case in cases if case["style"]["profile"] == profile]
        assert len(selected) == 8
        assert sum(case["expected_output_mode"] == "no_change" for case in selected) == 4
        assert any(case["expected_output_mode"] == "clean_rewrite" for case in selected)
    assert {case["expected_output_mode"] for case in cases} == {
        "clean_rewrite", "no_change", "review_comment", "needs_author_decision",
    }


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
    rows, errors = validate_results(path, REVIEW_SCHEMA, {"BENCH-HUM-001": "clean_rewrite"})
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
    assert summary["unreviewed_cases"] == len(cases) - 1


def test_profile_report_separates_systems_and_unreviewed_profiles() -> None:
    cases = [
        {"id": "BENCH-HUM-040", "skill": "humanizer-vi", "domain": "blog",
         "style": {"profile": "plain"}},
        {"id": "BENCH-HUM-041", "skill": "humanizer-vi", "domain": "blog",
         "style": {"profile": "plain"}},
        {"id": "BENCH-HUM-056", "skill": "humanizer-vi", "domain": "technical",
         "style": {"profile": "technical"}},
    ]
    first = review("BENCH-HUM-040")
    second = review("BENCH-HUM-040", "reviewer-02", ["changed_certainty"])
    second["system"] = "baseline"
    second["scores"]["naturalness"] = 1
    summary = summarize(cases, [first, second])
    assert summary["by_profile"] == {"plain": 2, "technical": 1}
    systems = summary["profile_results"]["plain"]["systems"]
    assert systems["candidate-system"]["averages"]["naturalness"] == 4
    assert systems["baseline"]["averages"]["naturalness"] == 1
    assert systems["baseline"]["blocker_rate"] == 1
    assert systems["baseline"]["unreviewed_cases"] == 1
    assert summary["profile_results"]["technical"] == {"cases": 1, "systems": {}}


def test_generated_pattern_docs_are_stable_and_complete() -> None:
    expected = render(ROOT / "patterns")
    actual = (ROOT / "docs" / "generated-patterns.md").read_text(encoding="utf-8")
    assert actual == expected
    assert f"**{len(PATTERN_IDS)} pattern**" in actual
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
    assert len(examples) == 103
    assert counts == {
        "technical": 15,
        "work-email": 17,
        "blog": 15,
        "academic": 10,
        "product-description": 10,
        "marketing": 10,
        "customer-support": 10,
        "social-media": 10,
        "administrative": 6,
    }


def test_internal_markdown_links_resolve() -> None:
    broken: list[str] = []
    for document in ROOT.rglob("*.md"):
        ignored_dirs = {".git", ".venv", "node_modules", "dist", "build"}
        if any(part in ignored_dirs for part in document.parts):
            continue
        for target in LINK_RE.findall(document.read_text(encoding="utf-8")):
            clean = target.split("#", 1)[0].strip().strip("<>")
            if not clean or clean.startswith(("http://", "https://", "mailto:", "file:")):
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
    assert "](CONTRIBUTING.vi.md)" in (ROOT / "README.vi.md").read_text(encoding="utf-8")


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
    examples = [
        line
        for line in (ROOT / "examples" / "examples.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    cases, _ = load_cases(ROOT / "benchmarks" / "cases", PATTERN_IDS)
    pattern_count = len(PATTERN_IDS)
    example_count = len(examples)
    case_count = len(cases)
    count_facts = (
        (
            ROOT / "README.md",
            (
                f"{pattern_count} patterns",
                f"{example_count} examples",
                f"{case_count} benchmark cases",
            ),
        ),
        (
            ROOT / "README.vi.md",
            (
                f"{pattern_count} pattern",
                f"{example_count} example",
                f"{case_count} benchmark case",
            ),
        ),
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


def test_voice_and_linguistics_cases_cover_four_skills_and_voice_sample() -> None:
    cases = load_jsonl(ROOT / "benchmarks" / "cases" / "voice-and-linguistics.jsonl")
    assert len(cases) == 12
    assert {case["skill"] for case in cases} == {
        "humanizer-vi",
        "translationese-cleaner-vi",
        "style-guide-vi",
        "grammar-checker-vi",
    }
    voice_cases = [case for case in cases if case.get("style", {}).get("voice_sample")]
    assert {case["expected_output_mode"] for case in voice_cases} == {
        "clean_rewrite",
        "no_change",
    }
    for case in cases:
        found = {issue["pattern_id"] for issue in lint_text(case["input"], {case["skill"]})}
        expected = set(case["expected_patterns"])
        if expected:
            assert expected.issubset(found), f"{case['id']} thiếu pattern {expected}"
        elif case["expected_output_mode"] == "no_change":
            assert found == set(), f"{case['id']} báo nhầm trên case no_change: {found}"


def test_prepare_review_packet_strips_ground_truth_labels(tmp_path: Path) -> None:
    cases, errors = load_cases(
        ROOT / "benchmarks" / "cases",
        PATTERN_IDS,
        ROOT / "benchmarks" / "case.schema.json",
    )
    assert errors == []
    packet = prepare_review_packet(cases, skills={"humanizer-vi"})
    assert packet
    assert all(item["skill"] == "humanizer-vi" for item in packet)
    forbidden = {
        "expected_output_mode",
        "expected_patterns",
        "must_preserve",
        "must_not_add",
        "evaluation_notes",
        "blockers",
    }
    for item in packet:
        assert forbidden.isdisjoint(item.keys())
        assert "Yêu cầu biên tập:" in item["context"]

    out_path = tmp_path / "packet.jsonl"
    assert (
        benchmarks_main(
            [
                "--prepare-packet",
                str(out_path),
                "--skill",
                "humanizer-vi",
                "--profile",
                "business",
            ]
        )
        == 0
    )
    exported = [json.loads(line) for line in out_path.read_text(encoding="utf-8").splitlines()]
    assert any(
        item["case_id"] == "BENCH-HUM-109" and item["style"].get("voice_sample")
        for item in exported
    )
    assert all(forbidden.isdisjoint(item.keys()) for item in exported)


def test_spoken_humor_satire_cases_are_valid() -> None:
    cases = load_jsonl(ROOT / "benchmarks" / "cases" / "spoken-humor-satire.jsonl")
    assert len(cases) == 10
    assert {case["domain"] for case in cases} >= {"spoken-script", "social-media", "blog"}
    assert {case["expected_output_mode"] for case in cases} == {
        "clean_rewrite",
        "no_change",
        "review_comment",
    }
    for case in cases:
        found = {issue["pattern_id"] for issue in lint_text(case["input"], {case["skill"]})}
        expected = set(case["expected_patterns"])
        if expected:
            assert expected.issubset(found), f"{case['id']} thiếu pattern {expected}"
        elif case["expected_output_mode"] == "no_change":
            assert found == set(), f"{case['id']} báo nhầm trên case no_change: {found}"


def test_new_pattern_restraint_cases_cover_true_positives_and_no_change() -> None:
    cases = load_jsonl(ROOT / "benchmarks" / "cases" / "new-pattern-restraint.jsonl")
    assert len(cases) == 8
    assert sum(case["expected_output_mode"] == "clean_rewrite" for case in cases) == 3
    assert sum(case["expected_output_mode"] == "no_change" for case in cases) == 5
    triggered_patterns: set[str] = set()
    for case in cases:
        found = {issue["pattern_id"] for issue in lint_text(case["input"], {case["skill"]})}
        expected = set(case["expected_patterns"])
        if expected:
            assert expected.issubset(found), f"{case['id']} thiếu pattern {expected}"
            triggered_patterns.update(expected)
        elif case["expected_output_mode"] == "no_change":
            assert found == set(), f"{case['id']} báo nhầm trên case no_change: {found}"
    assert triggered_patterns == {"VI-TRA-S06", "VI-TRA-S07", "VI-TRA-S08"}
