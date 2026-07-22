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
        "output_mode": "no_change",
        "patterns_triggered": [],
        "must_preserve": ["API", "có thể", "429"],
        "must_not_add": ["Nguyên nhân chưa được nêu"],
        "notes": "Câu đã rõ nên giữ nguyên.",
        "gold_output_mode": True,
        "gold_rewrite": True,
        "preservation_review": {
            "status": "agent-reviewed",
            "reviewer_id": "test-agent",
            "review_method": "manual-pair-audit",
            "reviewed_at": "2026-07-20",
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


def test_invalid_output_mode_is_rejected(tmp_path: Path) -> None:
    example = sample_example()
    example["output_mode"] = "rewrite_anyway"
    assert any("output_mode" in error for error in errors_for(tmp_path, example))


def test_unknown_pattern_id_is_rejected(tmp_path: Path) -> None:
    example = sample_example()
    example["patterns_triggered"] = ["VI-HUM-L98"]
    assert any("pattern ID không tồn tại" in error for error in errors_for(tmp_path, example))


def test_duplicate_example_id_is_rejected(tmp_path: Path) -> None:
    example = sample_example()
    assert any("trùng" in error for error in errors_for(tmp_path, example, example))


def test_unreviewed_gold_rewrite_is_rejected(tmp_path: Path) -> None:
    example = sample_example()
    example["preservation_review"] = {
        "status": "unreviewed",
        "meaning_preserved": False,
        "facts_preserved": False,
        "review_notes": "Chưa audit cặp input và output.",
    }
    assert any("gold rewrite" in error for error in errors_for(tmp_path, example))


def test_review_comment_is_classification_gold_not_rewrite_gold(tmp_path: Path) -> None:
    example = sample_example()
    example["output"] = "Cần bổ sung nguồn cụ thể cho nhận định này."
    example["output_mode"] = "review_comment"
    example["gold_rewrite"] = False
    assert errors_for(tmp_path, example) == []
    example["gold_rewrite"] = True
    errors = errors_for(tmp_path, example)
    assert any("gold_rewrite" in error or "gold rewrite" in error for error in errors)


def test_needs_author_decision_is_not_gold_rewrite(tmp_path: Path) -> None:
    example = sample_example()
    example["output"] = "Cần xác nhận chủ thể thực hiện hành động."
    example["output_mode"] = "needs_author_decision"
    example["gold_rewrite"] = True
    errors = errors_for(tmp_path, example)
    assert any("gold_rewrite" in error or "gold rewrite" in error for error in errors)


def test_gold_no_change_requires_identical_output(tmp_path: Path) -> None:
    example = sample_example()
    assert errors_for(tmp_path, example) == []
    example["output"] = "API trả lỗi 429."
    assert any("output trùng input" in error for error in errors_for(tmp_path, example))


def test_review_provenance_is_required(tmp_path: Path) -> None:
    example = sample_example()
    del example["preservation_review"]["reviewer_id"]
    assert any("reviewer_id" in error for error in errors_for(tmp_path, example))


def test_review_date_must_be_valid_iso_date(tmp_path: Path) -> None:
    example = sample_example()
    example["preservation_review"]["reviewed_at"] = "2026-02-31"
    assert any("reviewed_at" in error for error in errors_for(tmp_path, example))


def test_self_contained_example_is_valid(tmp_path: Path) -> None:
    assert errors_for(tmp_path, sample_example()) == []


def test_example_with_explicit_context_is_valid(tmp_path: Path) -> None:
    example = sample_example()
    example["input"] = "Hạn phản hồi là 07/08/2026."
    example["context"] = "Tài liệu dùng thứ tự ngày/tháng/năm."
    example["output"] = "Hạn phản hồi là ngày 7 tháng 8 năm 2026."
    example["output_mode"] = "clean_rewrite"
    example["must_preserve"] = ["Ngày 7 tháng 8 năm 2026"]
    assert errors_for(tmp_path, example) == []


def test_release_corpus_has_103_reviewed_unique_examples() -> None:
    rows, errors = validate_examples(ROOT / "examples" / "examples.jsonl", SCHEMA, PATTERN_IDS)
    assert errors == []
    assert len(rows) == 103
    assert len({row["id"] for row in rows}) == 103
    assert all(row["gold_output_mode"] for row in rows)
    assert all(row["preservation_review"]["status"] == "agent-reviewed" for row in rows)
    assert {
        row["preservation_review"]["reviewer_id"] for row in rows
    } == {"codex-semantic-audit-01", "codex-semantic-audit-02"}
    assert all(
        "meaning_preserved" not in row and "facts_preserved" not in row for row in rows
    )


def test_semantic_audit_regressions() -> None:
    rows, errors = validate_examples(ROOT / "examples" / "examples.jsonl", SCHEMA, PATTERN_IDS)
    assert errors == []
    examples = {row["id"]: row for row in rows}

    assert "quan trọng" in examples["EX-020"]["output"]
    assert "thống nhất" in examples["EX-020"]["output"]
    assert examples["EX-027"]["output_mode"] == "needs_author_decision"
    assert examples["EX-027"]["gold_rewrite"] is False
    assert all(
        phrase in examples["EX-028"]["output"]
        for phrase in ("cần thiết", "quan trọng", "hữu ích")
    )
    assert examples["EX-031"]["output_mode"] == "needs_author_decision"
    assert examples["EX-031"]["gold_rewrite"] is False
    assert "không có ai ở cạnh" not in examples["EX-032"]["output"]
    assert "trải nghiệm" in examples["EX-035"]["output"]
    assert examples["EX-038"]["output_mode"] == "needs_author_decision"
    assert "2026" not in examples["EX-038"]["output"]
    assert "tôi" not in examples["EX-039"]["output"].casefold()
    assert "bạn" in examples["EX-045"]["output"].casefold()
    assert "quan trọng" in examples["EX-046"]["output"]
    assert examples["EX-054"]["output_mode"] == "review_comment"
    assert examples["EX-054"]["gold_rewrite"] is False
    assert "đột phá" in examples["EX-056"]["output"]
    assert "trải nghiệm" in examples["EX-056"]["output"]
