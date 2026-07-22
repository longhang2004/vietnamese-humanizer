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
    issues = lint_text(text, {"style-guide-vi"})
    findings = [issue for issue in issues if issue["pattern_id"] == "VI-STY-P01"]
    assert len(findings) == 1
    assert len(findings[0]["occurrences"]) == 3


def test_consistency_patterns_require_distinct_forms() -> None:
    assert "VI-STY-T01" not in ids(
        "Bạn đăng nhập rồi đăng nhập lại.", "style-guide-vi"
    )
    assert "VI-STY-N02" not in ids("Tỷ lệ A là 15%, tỷ lệ B là 20%.", "style-guide-vi")
    assert "VI-STY-P01" not in ids(
        "Chúng tôi đã kiểm tra và chúng tôi sẽ phản hồi khi chúng tôi hoàn tất.",
        "style-guide-vi",
    )

    terminology = lint_text(
        "Chọn Login rồi đăng nhập bằng email.", {"style-guide-vi"}
    )
    percentages = lint_text("Tỷ lệ A là 15%, tỷ lệ B là 20 %.", {"style-guide-vi"})
    assert len([issue for issue in terminology if issue["pattern_id"] == "VI-STY-T01"]) == 1
    assert len([issue for issue in percentages if issue["pattern_id"] == "VI-STY-N02"]) == 1


def test_count_pattern_is_one_finding_with_multiple_occurrences() -> None:
    text = (
        "Báo cáo được duyệt bởi quản lý. "
        "Thay đổi được triển khai bởi đội kỹ thuật."
    )
    findings = [
        issue
        for issue in lint_text(text, {"translationese-cleaner-vi"})
        if issue["pattern_id"] == "VI-TRA-S03"
    ]
    assert len(findings) == 1
    assert len(findings[0]["occurrences"]) == 2


def test_count_pattern_below_threshold_is_not_reported() -> None:
    text = "Báo cáo được duyệt bởi quản lý."
    assert "VI-TRA-S03" not in ids(text, "translationese-cleaner-vi")


def test_review_examples_have_expected_findings() -> None:
    marketing = (
        "Trong bối cảnh kỷ nguyên số không ngừng phát triển, giải pháp đột phá "
        "của chúng tôi mở ra một chương mới đầy hứa hẹn. Đây không chỉ là một "
        "sản phẩm, mà còn là minh chứng cho hành trình kiến tạo giá trị bền vững, "
        "giúp doanh nghiệp vươn tầm và chạm tới thành công."
    )
    passive = (
        "Một quyết định đã được thực hiện bởi ban quản lý nhằm cải thiện trải "
        "nghiệm của người dùng. Các thay đổi sẽ được triển khai bởi đội kỹ thuật "
        "trong tuần tới và phản hồi sẽ được thu thập từ khách hàng."
    )
    administrative = (
        "Việc thực hiện công tác rà soát và tiến hành đánh giá mức độ đáp ứng của "
        "hệ thống được tiến hành nhằm mục đích bảo đảm sự phù hợp trong quá trình "
        "vận hành và sử dụng thực tế."
    )
    grammar = (
        "Nhóm chúng tôi đã nghiên cứu rất kĩ vấn đề này. Tuy nhiên kết quả cho thấy "
        "phương án mới không những tiết kiệm chi phí nhưng còn giúp nhân viên xử lý "
        "công việc nhanh hơn. Vì vậy nên công ty sẽ áp dụng nó từ tháng sau."
    )
    style = (
        "Công ty sẽ ra mắt ứng dụng vào ngày 5/8/2026. App mới giúp người sử dụng "
        "quản lý hồ sơ cá nhân, trong khi người dùng cũng có thể gửi yêu cầu hỗ trợ "
        "qua Website. Chúng tôi dự kiến phục vụ khoảng 10 ngàn khách hàng trong năm "
        "đầu tiên."
    )
    clean = "Nhóm hoàn thành báo cáo hôm nay và sẽ gửi bản đã duyệt vào sáng mai."

    marketing_issues = lint_text(marketing)
    assert [issue["pattern_id"] for issue in marketing_issues].count("VI-HUM-L02") == 1
    assert "VI-STY-C01" not in [issue["pattern_id"] for issue in marketing_issues]

    passive_issues = lint_text(passive)
    passive_finding = next(
        issue for issue in passive_issues if issue["pattern_id"] == "VI-TRA-S03"
    )
    assert len(passive_finding["occurrences"]) == 2
    assert "VI-STY-C01" not in [issue["pattern_id"] for issue in passive_issues]

    assert "VI-TRA-S05" in [issue["pattern_id"] for issue in lint_text(administrative)]
    grammar_ids = [issue["pattern_id"] for issue in lint_text(grammar)]
    assert {"VI-GRA-C05", "VI-GRA-C06"}.issubset(grammar_ids)

    assert [issue["pattern_id"] for issue in lint_text(style)] == ["VI-STY-N03"]
    assert lint_text(clean) == []


def test_common_nouns_in_lowercase_do_not_trigger_capitalization() -> None:
    text = "Giải pháp này phục vụ khách hàng và cải thiện sản phẩm."
    assert "VI-STY-C01" not in ids(text, "style-guide-vi")


def test_excerpt_contains_the_match_instead_of_only_the_line_start() -> None:
    text = "Mở đầu " + "rất dài " * 20 + "Giải Pháp" + " ở cuối câu."
    issue = next(
        issue
        for issue in lint_text(text, {"style-guide-vi"})
        if issue["pattern_id"] == "VI-STY-C01"
    )
    assert len(issue["excerpt"]) <= 100
    assert "Giải Pháp" in issue["excerpt"]
    assert issue["occurrences"][0]["matched_text"] == "Giải Pháp"


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
        "occurrences",
    } == issue.keys()
    assert issue["occurrences"]
    first = issue["occurrences"][0]
    assert (issue["line"], issue["column"], issue["excerpt"]) == (
        first["line"],
        first["column"],
        first["excerpt"],
    )


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
    assert summary["total"] >= 4
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
