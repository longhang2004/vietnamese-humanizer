from pathlib import Path

from vietnamese_writing_skills.core.frontmatter import (
    parse_frontmatter,
    validate_all,
    validate_skill,
)

VALID_BODY = """---
name: demo-skill
description: Sửa văn bản khi người dùng yêu cầu; không dùng cho code.
---
# Demo
## Quy trình
Đọc rồi sửa.
## Bảo toàn
Giữ dữ kiện.
## Anti-goals
Không bịa.
"""


def make_skill(root: Path, body: str = VALID_BODY) -> Path:
    skill = root / "demo-skill"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(body, encoding="utf-8")
    (skill / "README.md").write_text("# Demo\n", encoding="utf-8")
    return skill


def test_parse_frontmatter() -> None:
    metadata, body = parse_frontmatter(VALID_BODY)
    assert metadata["name"] == "demo-skill"
    assert "## Quy trình" in body


def test_missing_skill_md_is_reported(tmp_path: Path) -> None:
    skill = tmp_path / "empty-skill"
    skill.mkdir()
    assert any("thiếu SKILL.md" in error for error in validate_skill(skill))


def test_broken_reference_is_reported(tmp_path: Path) -> None:
    body = VALID_BODY.replace("Đọc rồi sửa.", "Đọc [hướng dẫn](references/missing.md) rồi sửa.")
    skill = make_skill(tmp_path, body)
    assert any("link hỏng" in error for error in validate_skill(skill))


def test_valid_skill_directory_passes(tmp_path: Path) -> None:
    make_skill(tmp_path)
    assert validate_all(tmp_path) == []
