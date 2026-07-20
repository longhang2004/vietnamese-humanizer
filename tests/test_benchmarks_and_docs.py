import re
from collections import Counter
from pathlib import Path

from scripts._shared import load_jsonl
from scripts.generate_pattern_docs import render
from scripts.run_benchmarks import load_cases, validate_case

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def test_benchmark_loader_reads_all_cases() -> None:
    cases, errors = load_cases(ROOT / "benchmarks" / "cases")
    assert errors == []
    assert len(cases) == 30


def test_benchmark_missing_field_is_reported(tmp_path: Path) -> None:
    case = {
        "id": "BENCH-HUM-999",
        "skill": "humanizer-vi",
        "domain": "technical",
        "register": "professional",
    }
    errors = validate_case(case, tmp_path / "case.jsonl")
    assert any("thiếu field input" in error for error in errors)


def test_generated_pattern_docs_are_stable() -> None:
    expected = render(ROOT / "patterns")
    actual = (ROOT / "docs" / "generated-patterns.md").read_text(encoding="utf-8")
    assert actual == expected
    assert "**40 pattern**" in actual


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


def test_example_required_fields() -> None:
    required = {
        "domain",
        "register",
        "input",
        "output",
        "patterns_triggered",
        "notes",
        "meaning_preserved",
        "facts_preserved",
    }
    for example in load_jsonl(ROOT / "examples" / "examples.jsonl"):
        assert required <= example.keys()


def test_internal_markdown_links_resolve() -> None:
    broken: list[str] = []
    for document in ROOT.rglob("*.md"):
        if any(part in {".git", ".venv"} for part in document.parts):
            continue
        for target in LINK_RE.findall(document.read_text(encoding="utf-8")):
            clean = target.split("#", 1)[0].strip().strip("<>")
            if not clean or clean.startswith(("http://", "https://", "mailto:")):
                continue
            if not (document.parent / clean).exists():
                broken.append(f"{document.relative_to(ROOT)} -> {target}")
    assert broken == []
