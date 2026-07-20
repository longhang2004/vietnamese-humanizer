import json
from pathlib import Path

from vietnamese_writing_skills.core.examples import validate_examples
from vietnamese_writing_skills.core.patterns import pattern_index

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "examples" / "schema.json"
PATTERN_IDS = set(pattern_index(ROOT / "patterns"))


def sample_example() -> dict:
    return {
        "id": "EX-999",
        "skill": "humanizer-vi",
        "domain": "technical",
        "register": "professional",
        "input": "API có thể trả lỗi 429.",
        "context": "",
        "output": "API có thể trả lỗi 429.",
        "patterns_triggered": [],
        "must_preserve": ["API", "có thể", "429"],
        "must_not_add": ["Nguyên nhân chưa được nêu"],
        "notes": "Câu đã rõ nên giữ nguyên.",
        "gold": True,
        "preservation_review": {
            "status": "reviewed",
            "meaning_preserved": True,
            "facts_preserved": True,
            "review_notes": "Output trùng input.",
        },
    }


def write_examples(path: Path, *examples: dict) -> None:
    path.write_text(
        "\n".join(json.dumps(item, ensure_ascii=False) for item in examples) + "\n",
        encoding="utf-8",
    )


def errors_for(tmp_path: Path, *examples: dict) -> list[str]:
    path = tmp_path / "examples.jsonl"
    write_examples(path, *examples)
    return validate_examples(path, SCHEMA, PATTERN_IDS)[1]


def test_missing_context_is_rejected(tmp_path: Path) -> None:
    example = sample_example()
    del example["context"]
    assert any("context" in error for error in errors_for(tmp_path, example))


def test_missing_must_preserve_is_rejected(tmp_path: Path) -> None:
    example = sample_example()
    del example["must_preserve"]
    assert any("must_preserve" in error for error in errors_for(tmp_path, example))


def test_missing_must_not_add_is_rejected(tmp_path: Path) -> None:
    example = sample_example()
    del example["must_not_add"]
    assert any("must_not_add" in error for error in errors_for(tmp_path, example))


def test_reviewed_without_notes_is_rejected(tmp_path: Path) -> None:
    example = sample_example()
    example["preservation_review"]["review_notes"] = ""
    assert any("review_notes" in error for error in errors_for(tmp_path, example))


def test_unknown_pattern_id_is_rejected(tmp_path: Path) -> None:
    example = sample_example()
    example["patterns_triggered"] = ["VI-HUM-L98"]
    assert any("pattern ID không tồn tại" in error for error in errors_for(tmp_path, example))


def test_duplicate_example_id_is_rejected(tmp_path: Path) -> None:
    example = sample_example()
    assert any("trùng" in error for error in errors_for(tmp_path, example, example))


def test_gold_example_needing_review_is_rejected(tmp_path: Path) -> None:
    example = sample_example()
    example["preservation_review"]["status"] = "needs-review"
    assert any("gold example" in error for error in errors_for(tmp_path, example))


def test_self_contained_example_is_valid(tmp_path: Path) -> None:
    assert errors_for(tmp_path, sample_example()) == []


def test_example_with_explicit_context_is_valid(tmp_path: Path) -> None:
    example = sample_example()
    example["input"] = "Hạn phản hồi là 07/08/2026."
    example["context"] = "Tài liệu dùng thứ tự ngày/tháng/năm."
    example["output"] = "Hạn phản hồi là ngày 7 tháng 8 năm 2026."
    example["must_preserve"] = ["Ngày 7 tháng 8 năm 2026"]
    assert errors_for(tmp_path, example) == []


def test_release_corpus_has_100_reviewed_unique_examples() -> None:
    rows, errors = validate_examples(ROOT / "examples" / "examples.jsonl", SCHEMA, PATTERN_IDS)
    assert errors == []
    assert len(rows) == 100
    assert len({row["id"] for row in rows}) == 100
    assert all(row["gold"] for row in rows)
    assert all(row["preservation_review"]["status"] == "reviewed" for row in rows)
    assert all(
        "meaning_preserved" not in row and "facts_preserved" not in row for row in rows
    )
