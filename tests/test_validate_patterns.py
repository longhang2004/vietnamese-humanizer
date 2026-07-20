import json
from copy import deepcopy
from pathlib import Path

import yaml

from vietnamese_writing_skills.cli.validate_patterns import validate_catalog

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "patterns" / "schema.json"


def sample_pattern(pattern_id: str = "VI-HUM-L99") -> dict:
    return {
        "id": pattern_id,
        "name": f"pattern-{pattern_id[-2:]}",
        "skill": "humanizer-vi",
        "category": "lexical",
        "finding_type": "heuristic",
        "scope": "phrase",
        "aggregation": "density",
        "severity": "low",
        "confidence": "medium",
        "summary": "Một pattern đủ dài để kiểm tra schema dữ liệu.",
        "signals": {"regex": [r"\bcụm thử\b"]},
        "why_it_matters": "Giúp test xác nhận catalog phát hiện dữ liệu không hợp lệ.",
        "rewrite_strategy": ["Sửa trực tiếp khi có đủ ngữ cảnh."],
        "bad_examples": [{"text": "Cụm thử một."}, {"text": "Cụm thử hai."}],
        "good_examples": [
            {"mode": "clean_rewrite", "text": "Câu tốt một."},
            {"mode": "review_comment", "text": "Cần bổ sung nguồn cho câu hai."},
        ],
        "exceptions": ["Khi cụm nằm trong trích dẫn."],
        "false_positive_risk": "medium",
        "tags": ["test"],
    }


def write_catalog(path: Path, patterns: list[dict]) -> None:
    path.write_text(
        yaml.safe_dump({"schema_version": "1.0", "patterns": patterns}, allow_unicode=True),
        encoding="utf-8",
    )


def schema_errors(tmp_path: Path, pattern: dict) -> list[str]:
    write_catalog(tmp_path / "one.yml", [pattern])
    return validate_catalog(tmp_path, SCHEMA, None)


def test_duplicate_pattern_id_is_reported(tmp_path: Path) -> None:
    pattern = sample_pattern()
    second = deepcopy(pattern)
    second["name"] = "pattern-khac"
    write_catalog(tmp_path / "one.yml", [pattern, second])
    errors = validate_catalog(tmp_path, SCHEMA, None)
    assert any("ID VI-HUM-L99 trùng" in error for error in errors)


def test_schema_error_is_reported(tmp_path: Path) -> None:
    pattern = sample_pattern()
    del pattern["exceptions"]
    assert any("exceptions" in error for error in schema_errors(tmp_path, pattern))


def test_invalid_finding_type_is_reported(tmp_path: Path) -> None:
    pattern = sample_pattern()
    pattern["finding_type"] = "mistake"
    assert any("finding_type" in error for error in schema_errors(tmp_path, pattern))


def test_invalid_scope_is_reported(tmp_path: Path) -> None:
    pattern = sample_pattern()
    pattern["scope"] = "chapter"
    assert any("scope" in error for error in schema_errors(tmp_path, pattern))


def test_invalid_aggregation_is_reported(tmp_path: Path) -> None:
    pattern = sample_pattern()
    pattern["aggregation"] = "average"
    assert any("aggregation" in error for error in schema_errors(tmp_path, pattern))


def test_invalid_regex_is_reported(tmp_path: Path) -> None:
    pattern = sample_pattern()
    pattern["signals"] = {"regex": ["("]}
    assert any("regex không hợp lệ" in error for error in schema_errors(tmp_path, pattern))


def test_clean_rewrite_and_review_comment_examples_are_valid(tmp_path: Path) -> None:
    assert schema_errors(tmp_path, sample_pattern()) == []


def test_invalid_good_example_mode_is_reported(tmp_path: Path) -> None:
    pattern = sample_pattern()
    pattern["good_examples"][0]["mode"] = "replacement"
    assert any("good_examples" in error for error in schema_errors(tmp_path, pattern))


def test_good_example_mode_is_required(tmp_path: Path) -> None:
    pattern = sample_pattern()
    del pattern["good_examples"][0]["mode"]
    assert any("mode" in error for error in schema_errors(tmp_path, pattern))


def test_schema_file_is_json() -> None:
    assert json.loads(SCHEMA.read_text(encoding="utf-8"))["$schema"].endswith("2020-12/schema")
