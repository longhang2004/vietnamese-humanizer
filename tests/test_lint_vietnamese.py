import importlib
import json
from pathlib import Path

import pytest
import yaml

from vietnamese_writing_skills.cli.lint import lint_file, lint_text, main, mask_protected

ROOT = Path(__file__).resolve().parents[1]


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
    findings = [
        issue
        for issue in lint_text(twice, {"humanizer-vi"})
        if issue["pattern_id"] == "VI-HUM-L01"
    ]
    assert len(findings) == 1
    assert len(findings[0]["occurrences"]) == 2


def test_sequence_pattern_needs_three_sentences() -> None:
    two = "Nhóm sửa lỗi. Nhóm viết test."
    three = two + " Nhóm cập nhật tài liệu."
    assert "VI-HUM-S01" not in ids(two, "humanizer-vi")
    findings = [
        issue
        for issue in lint_text(three, {"humanizer-vi"})
        if issue["pattern_id"] == "VI-HUM-S01"
    ]
    assert len(findings) == 1
    assert len(findings[0]["occurrences"]) == 3


def test_variance_detector_emits_one_finding_without_catalog_duplicate() -> None:
    text = (
        "Nhóm ghi nhận yêu cầu trong buổi sáng. "
        "Nhóm kiểm tra dữ liệu trong buổi trưa. "
        "Nhóm cập nhật kết quả trong buổi chiều. "
        "Nhóm gửi thông báo kết quả trong buổi tối. "
        "Nhóm lưu lại biên bản trong ngày mai."
    )
    findings = [
        issue
        for issue in lint_text(text, {"humanizer-vi"})
        if issue["pattern_id"] == "VI-HUM-S04"
    ]
    assert len(findings) == 1


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


def test_sentence_scoped_patterns_do_not_cross_sentence_boundaries() -> None:
    grammar = "Không chỉ nhanh. Nhưng còn dễ dùng."
    humanizer = "Trong bối cảnh nhiều biến động. Hệ thống không ngừng phát triển."

    assert "VI-GRA-C05" not in ids(grammar, "grammar-checker-vi")
    assert "VI-HUM-L02" not in ids(humanizer, "humanizer-vi")


def test_redundant_connector_allows_optional_comma() -> None:
    assert "VI-GRA-C06" in ids("Ông đến muộn. Vì vậy, nên cuộc họp bị hoãn.")


def test_administrative_threshold_is_scoped_to_each_sentence() -> None:
    text = (
        "Việc thực hiện công tác rà soát đã hoàn tất. "
        "Đánh giá được tiến hành vào hôm qua."
    )
    assert "VI-TRA-S05" not in ids(text, "translationese-cleaner-vi")


def test_explained_acronym_is_not_reported() -> None:
    text = "Thỏa thuận mức dịch vụ (SLA) sẽ được rà trong cuộc họp."
    assert "VI-STY-T02" not in ids(text, "style-guide-vi")


def test_new_rules_ignore_protected_content() -> None:
    text = """```text
Không những nhanh nhưng còn dễ dùng. Vì vậy nên đổi.
Việc thực hiện công tác được tiến hành nhằm mục đích kiểm tra.
```
Giữ `Vì vậy nên` làm ví dụ, xem https://example.com/vi_vay_nen và biến vi_vay_nen.
"""
    protected_ids = {"VI-GRA-C05", "VI-GRA-C06", "VI-TRA-S05"}
    assert protected_ids.isdisjoint(ids(text))


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


def test_excerpt_remains_bounded_when_match_is_longer_than_limit() -> None:
    text = "Không chỉ " + "rất dài " * 14 + "nhưng còn hữu ích."
    issue = next(issue for issue in lint_text(text) if issue["pattern_id"] == "VI-GRA-C05")

    assert len(issue["excerpt"]) <= 100
    assert len(issue["occurrences"][0]["matched_text"]) > 100


def test_catalog_examples_match_runtime_contract(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lint_module = importlib.import_module("vietnamese_writing_skills.cli.lint")
    records: list[tuple[Path, dict]] = []
    for path in sorted((ROOT / "patterns").glob("*.yml")):
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
        records.extend((path, pattern) for pattern in document["patterns"])

    index = {pattern["id"]: pattern for _, pattern in records}
    monkeypatch.setattr(lint_module, "iter_patterns", lambda _directory: iter(records))
    monkeypatch.setattr(lint_module, "pattern_index", lambda _directory=None: index)

    for _, pattern in records:
        pattern_id = pattern["id"]
        skill = {pattern["skill"]}
        bad_text = "\n".join(example["text"] for example in pattern["bad_examples"])
        bad_ids = {issue["pattern_id"] for issue in lint_module.lint_text(bad_text, skill)}
        assert pattern_id in bad_ids, f"{pattern_id} không bắt bad_examples trong catalog"

        for example in pattern["good_examples"]:
            good_ids = {
                issue["pattern_id"]
                for issue in lint_module.lint_text(example["text"], skill)
            }
            assert pattern_id not in good_ids, (
                f"{pattern_id} báo nhầm good_example: {example['text']}"
            )


def test_lexical_reduplication_is_not_reported() -> None:
    assert "VI-GRA-L01" not in ids("Hai tiến trình chạy song song và dữ liệu cập nhật dần dần.")


def test_common_acronym_is_not_reported() -> None:
    assert "VI-STY-T02" not in ids("API trả JSON.", "style-guide-vi")


def test_uppercase_vietnamese_emphasis_is_not_reported_as_acronym() -> None:
    """Từ tiếng Việt viết hoa nhấn mạnh (CTA, quảng cáo) không phải viết tắt."""
    # Từ có dấu tiếng Việt
    assert "VI-STY-T02" not in ids("Ưu đãi GIẢM GIÁ SỐC!", "style-guide-vi")
    # Từ không dấu nhưng nằm trong exclude_phrases
    assert "VI-STY-T02" not in ids("Nhận ưu đãi lên đến 40% NGAY TẠI ĐÂY!", "style-guide-vi")
    # Cụm viết hoa nhấn mạnh cùng dòng có từ có dấu
    assert "VI-STY-T02" not in ids("MUA NGAY SIÊU KHỦNG!", "style-guide-vi")
    # Viết tắt thật vẫn bị detect
    assert "VI-STY-T02" in ids("SLA sẽ được rà soát.", "style-guide-vi")


def test_vietnamese_administrative_acronyms_are_excluded() -> None:
    """Viết tắt hành chính VN phổ biến không trigger vì quá quen thuộc."""
    assert "VI-STY-T02" not in ids("UBND tỉnh đã phê duyệt.", "style-guide-vi")
    assert "VI-STY-T02" not in ids("CSGT xử lý vi phạm.", "style-guide-vi")
    assert "VI-STY-T02" not in ids("BHXH là bắt buộc.", "style-guide-vi")
    assert "VI-STY-T02" not in ids("CMND hoặc CCCD đều được.", "style-guide-vi")


def test_quoted_acronyms_are_not_reported() -> None:
    """Từ viết hoa trong ngoặc kép (slogan, quote) không trigger."""
    assert "VI-STY-T02" not in ids('"JUST DO IT" là slogan Nike.', "style-guide-vi")
    assert "VI-STY-T02" not in ids('"HELLO WORLD" trong code.', "style-guide-vi")
    assert "VI-STY-T02" not in ids('Slogan "KEEP CALM" đã nổi tiếng.', "style-guide-vi")
    assert "VI-STY-T02" not in ids("Slogan “KEEP CALM” đã nổi tiếng.", "style-guide-vi")


def test_previously_defined_acronym_is_not_reported_later() -> None:
    text = (
        "Thỏa thuận mức dịch vụ (SLA) được nêu ở đầu tài liệu. "
        "SLA vẫn được rà trong cuộc họp."
    )
    assert "VI-STY-T02" not in ids(text, "style-guide-vi")


def test_nested_four_backtick_fence_is_ignored() -> None:
    text = """Trước.

````markdown
```text
Nhóm sẽ sẽ gửi báo cáo.
```
````

Sau.
"""
    assert "VI-GRA-L01" not in ids(text, "grammar-checker-vi")


def test_density_signals_do_not_span_paragraphs_or_lists() -> None:
    split = (
        "Nhóm lưu log, đồng thời gửi cảnh báo.\n\n"
        "Qua đó quy trình rõ hơn.\n\n"
        "Từ đó chất lượng tăng."
    )
    listed = (
        "- Nhóm lưu log, đồng thời gửi cảnh báo.\n"
        "- Qua đó, quy trình rõ hơn.\n"
        "- Từ đó, chất lượng tăng."
    )
    together = (
        "Hệ thống lưu log, đồng thời gửi cảnh báo, qua đó giúp nhóm phản hồi, "
        "từ đó nâng cao chất lượng."
    )
    assert "VI-HUM-S03" not in ids(split, "humanizer-vi")
    assert "VI-HUM-S03" not in ids(listed, "humanizer-vi")
    assert "VI-HUM-S03" in ids(together, "humanizer-vi")


def test_repeated_opening_does_not_span_paragraphs_or_lists() -> None:
    split = (
        "Chúng tôi cập nhật phần mềm.\n\n"
        "Chúng tôi kiểm tra dữ liệu.\n\n"
        "Chúng tôi gửi báo cáo."
    )
    listed = (
        "- Chúng tôi cập nhật phần mềm.\n"
        "- Chúng tôi kiểm tra dữ liệu.\n"
        "- Chúng tôi gửi báo cáo."
    )
    prose = (
        "Chúng tôi cập nhật phần mềm. "
        "Chúng tôi kiểm tra dữ liệu. "
        "Chúng tôi gửi báo cáo."
    )
    assert "VI-HUM-S01" not in ids(split, "humanizer-vi")
    assert "VI-HUM-S01" not in ids(listed, "humanizer-vi")
    assert "VI-HUM-S01" in ids(prose, "humanizer-vi")


def test_nen_as_advice_is_not_redundant_connector() -> None:
    for text in (
        "Vì vậy, nên sao lưu dữ liệu trước khi nâng cấp.",
        "Vì vậy, nên chọn người có kinh nghiệm.",
        "Vì vậy, nên dùng máy có quạt.",
        "Vì vậy, nên nghỉ. Tôi sẽ quay lại.",
        "Vì vậy, nên chọn người đã làm việc ở đây.",
        "Vì vậy, nên chọn máy được bảo hành.",
        "Vì vậy, nên mua máy đang giảm giá.",
        "Vì vậy, nên thuê người đã có kinh nghiệm.",
        "Vì vậy, nên ưu tiên máy được bảo hành.",
        "Vì vậy, nên công bố bản đã duyệt.",
        "Vì vậy, nên công nhận người đã đóng góp.",
        "Vì vậy, nên dự thi khi đã chuẩn bị kỹ.",
    ):
        assert "VI-GRA-C06" not in ids(text, "grammar-checker-vi"), text
    assert "VI-GRA-C06" in ids(
        "Vì vậy nên công ty sẽ áp dụng phương án mới.",
        "grammar-checker-vi",
    )


def test_meaningful_reduplication_is_not_a_typo() -> None:
    assert "VI-GRA-L01" not in ids(
        "Người người, nhà nhà đều hướng về quê.",
        "grammar-checker-vi",
    )
    assert "VI-GRA-L01" not in ids("Bạn cứ từ từ đọc báo cáo.", "grammar-checker-vi")
    assert "VI-GRA-L01" in ids("Nhóm sẽ sẽ gửi báo cáo.", "grammar-checker-vi")


def test_email_filename_and_abbreviation_keep_dot_spacing() -> None:
    text = "Gửi hotro@example.com hoặc xem README.md tại TP.HCM."
    assert "VI-GRA-P02" not in ids(text, "grammar-checker-vi")


def test_addressee_and_user_role_are_not_treated_as_inconsistent() -> None:
    text = (
        "Bạn có thể mời người dùng mới vào workspace. "
        "Người dùng sẽ nhận email. Bạn xác nhận danh sách."
    )
    assert "VI-STY-P01" not in ids(text, "style-guide-vi")


def test_unbalanced_quotes_are_flagged_without_inventing_a_close() -> None:
    findings = [
        issue
        for issue in lint_text('Báo cáo “quý 3 vẫn chưa đóng.', {"grammar-checker-vi"})
        if issue["pattern_id"] == "VI-GRA-P04"
    ]
    assert len(findings) == 1
    assert "VI-GRA-P04" not in ids(
        "Báo cáo “quý 3” vẫn chưa đóng.",
        "grammar-checker-vi",
    )


def test_markdown_links_quoted_urls_and_list_markers_are_not_unbalanced() -> None:
    assert "VI-GRA-P04" not in ids(
        "Xem [hướng dẫn](https://example.com/docs).",
        "grammar-checker-vi",
    )
    assert "VI-GRA-P04" not in ids(
        'Truy cập "https://example.com" để đọc thêm.',
        "grammar-checker-vi",
    )
    assert "VI-GRA-P04" not in ids(
        "Truy cập “https://example.com” để đọc thêm.",
        "grammar-checker-vi",
    )
    assert "VI-GRA-P04" not in ids(
        "Xem https://example.com/a(b) để biết thêm.",
        "grammar-checker-vi",
    )
    assert "VI-GRA-P04" not in ids(
        "1) Mở ứng dụng.\n2) Chọn báo cáo.",
        "grammar-checker-vi",
    )
    text = "Xem [hướng dẫn](https://example.com/docs)."
    masked = mask_protected(text)
    assert masked[text.index("(")] == "("
    assert masked[text.rindex(")")] == ")"


def test_ipv6_url_brackets_are_masked_together() -> None:
    text = "Kết nối http://[::1]:8000/ để thử."
    assert "VI-GRA-P04" not in ids(text, "grammar-checker-vi")
    masked = mask_protected(text)
    opening = text.index("[")
    closing = text.index("]")
    assert masked[opening] == " "
    assert masked[closing] == " "


def test_unicode_space_after_url_does_not_swallow_following_words() -> None:
    for space in ("\u00a0", "\u202f", " "):
        text = f"Xem https://example.com{space}sẽ sẽ chạy."
        assert "VI-GRA-L01" in ids(text, "grammar-checker-vi"), repr(space)


def test_unbalanced_delimiters_follow_scan_order() -> None:
    findings = [
        issue
        for issue in lint_text(
            "Vui lòng xem (bảng 1).\nPhụ lục (bảng 2 chưa đóng.",
            {"grammar-checker-vi"},
        )
        if issue["pattern_id"] == "VI-GRA-P04"
    ]
    assert len(findings) == 1
    assert findings[0]["line"] == 2
    assert "VI-GRA-P04" in ids(")quý 3(", "grammar-checker-vi")


def test_common_tech_acronyms_are_excluded() -> None:
    """Viết tắt tech phổ biến đã có trong exclude_phrases."""
    assert "VI-STY-T02" not in ids("Dùng APP để đặt hàng.", "style-guide-vi")
    assert "VI-STY-T02" not in ids("Tải APK từ trang chính thức.", "style-guide-vi")


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
