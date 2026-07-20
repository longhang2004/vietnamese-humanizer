from scripts.lint_vietnamese import lint_text, mask_protected


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


def test_line_number_is_correct() -> None:
    text = "Dòng một.\nDòng hai.\nNhóm thực hiện việc kiểm tra.\n"
    issues = lint_text(text, {"translationese-cleaner-vi"})
    target = next(issue for issue in issues if issue["pattern_id"] == "VI-TRA-S02")
    assert target["line"] == 3


def test_density_pattern_needs_two_occurrences() -> None:
    once = "Công cụ đóng vai trò quan trọng trong việc kiểm tra dữ liệu."
    twice = once + "\nNhóm đóng vai trò chính trong việc rà soát kết quả."
    assert "VI-HUM-L01" not in ids(once, "humanizer-vi")
    assert "VI-HUM-L01" in ids(twice, "humanizer-vi")


def test_high_confidence_translationese_is_found_once() -> None:
    assert "VI-TRA-L01" in ids("Công cụ giúp mở khóa tiềm năng của dữ liệu.")


def test_lexical_reduplication_is_not_reported() -> None:
    assert "VI-GRA-L01" not in ids("Hai tiến trình chạy song song và dữ liệu cập nhật dần dần.")


def test_pronoun_inconsistency_is_found() -> None:
    text = "Bạn mở ứng dụng. Quý khách chọn Hồ sơ. Sau đó bạn nhấn Lưu."
    assert "VI-STY-P01" in ids(text, "style-guide-vi")


def test_common_acronym_is_not_reported() -> None:
    assert "VI-STY-T02" not in ids("API trả JSON.", "style-guide-vi")


def test_unexplained_acronym_is_reported_case_sensitively() -> None:
    assert "VI-STY-T02" in ids("RTO của dịch vụ là 30 phút.", "style-guide-vi")


def test_repeated_sentence_opening_is_found() -> None:
    text = "Nhóm sửa lỗi. Nhóm viết test. Nhóm cập nhật tài liệu."
    assert "VI-HUM-S01" in ids(text, "humanizer-vi")
