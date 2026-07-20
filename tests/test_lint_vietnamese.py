import json
from pathlib import Path

from vietnamese_writing_skills.cli.lint import lint_file, lint_text, main, mask_protected


def ids(text: str, skill: str | None = None) -> list[str]:
    skills = {skill} if skill else None
    return [issue["pattern_id"] for issue in lint_text(text, skills)]


def test_code_block_is_ignored() -> None:
    text = "Trước.\n```text\nmở khóa tiềm năng\n```\nSau.\n"
    assert "VI-TRA-L01" not in ids(text, "translationese-cleaner-vi")


def test_inline_code_and_url_keep_length() -> None:
    text = "Mở `thực hiện việc` rồi xem https://example.com/a,b."
    masked = mask_protected(text)
    assert len(masked) == len(text)
    assert "thực hiện việc" not in masked
    assert "https://" not in masked


def test_line_and_column_are_correct() -> None:
    text = "Dòng một.\nDòng hai.\n  Nhóm thực hiện việc kiểm tra.\n"
    issues = lint_text(text, {"translationese-cleaner-vi"})
    target = next(issue for issue in issues if issue["pattern_id"] == "VI-TRA-S02")
    assert (target["line"], target["column"]) == (3, 8)


def test_density_pattern_needs_two_occurrences() -> None:
    once = "Công cụ đóng vai trò quan trọng trong việc kiểm tra dữ liệu."
    twice = once + "\nNhóm đóng vai trò chính trong việc rà soát kết quả."
    assert "VI-HUM-L01" not in ids(once, "humanizer-vi")
    assert "VI-HUM-L01" in ids(twice, "humanizer-vi")


def test_sequence_pattern_needs_three_sentences() -> None:
    two = "Nhóm sửa lỗi. Nhóm viết test."
    three = two + " Nhóm cập nhật tài liệu."
    assert "VI-HUM-S01" not in ids(two, "humanizer-vi")
    assert "VI-HUM-S01" in ids(three, "humanizer-vi")


def test_pronoun_document_consistency_is_found() -> None:
    text = "Bạn mở ứng dụng. Quý khách chọn Hồ sơ. Sau đó bạn nhấn Lưu."
    assert "VI-STY-P01" in ids(text, "style-guide-vi")


def test_lexical_reduplication_is_not_reported() -> None:
    assert "VI-GRA-L01" not in ids("Hai tiến trình chạy song song và dữ liệu cập nhật dần dần.")


def test_common_acronym_is_not_reported() -> None:
    assert "VI-STY-T02" not in ids("API trả JSON.", "style-guide-vi")


def test_issue_json_has_taxonomy_fields(tmp_path: Path) -> None:
    path = tmp_path / "sample.md"
    path.write_text("Nhóm sẽ sẽ gửi báo cáo.", encoding="utf-8")
    result = lint_file(path)
    issue = next(item for item in result["issues"] if item["pattern_id"] == "VI-GRA-L01")
    assert {
        "pattern_id",
        "finding_type",
        "severity",
        "confidence",
        "scope",
        "line",
        "column",
        "excerpt",
        "message",
        "suggestion",
    } == issue.keys()


def test_summary_counts_finding_types(tmp_path: Path) -> None:
    path = tmp_path / "sample.md"
    path.write_text(
        "Nhóm sẽ sẽ gửi báo cáo. Mở khóa tiềm năng của dữ liệu. "
        "Bởi vì trời mưa cho nên tôi ở nhà.\nBởi vì đường ngập cho nên tôi không đi. "
        "Công cụ đóng vai trò chính trong việc kiểm tra. "
        "Nhóm đóng vai trò chính trong việc rà soát.",
        encoding="utf-8",
    )
    summary = lint_file(path)["summary"]
    assert summary["total"] >= 5
    assert all(summary[kind] >= 1 for kind in ("error", "warning", "preference", "heuristic"))


def test_text_output_labels_all_finding_types(tmp_path: Path, capsys) -> None:
    path = tmp_path / "sample.md"
    path.write_text(
        "Nhóm sẽ sẽ gửi báo cáo. Mở khóa tiềm năng của dữ liệu. "
        "Bởi vì trời mưa cho nên tôi ở nhà.\nBởi vì đường ngập cho nên tôi không đi. "
        "Công cụ đóng vai trò chính trong việc kiểm tra. "
        "Nhóm đóng vai trò chính trong việc rà soát.",
        encoding="utf-8",
    )
    assert main([str(path)]) == 1
    output = capsys.readouterr().out
    assert all(label in output for label in ("ERROR", "WARNING", "PREFERENCE", "HEURISTIC"))


def test_json_cli_output_is_valid(tmp_path: Path, capsys) -> None:
    path = tmp_path / "sample.md"
    path.write_text("Nhóm sẽ sẽ gửi báo cáo.", encoding="utf-8")
    assert main([str(path), "--format", "json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["summary"]["error"] == 1
