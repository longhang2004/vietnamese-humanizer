"""Frontend lint results must represent aggregated core findings accurately."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "web" / "frontend"


def test_frontend_supports_aggregated_occurrences() -> None:
    types = (FRONTEND / "lib" / "types.ts").read_text(encoding="utf-8")
    card = (FRONTEND / "components" / "IssueCard.tsx").read_text(encoding="utf-8")

    assert "export interface IssueOccurrence" in types
    assert "occurrences: IssueOccurrence[]" in types
    assert "{occurrences.length} vị trí" in card
    assert 'aria-label="Các vị trí phát hiện"' in card


def test_frontend_zero_state_does_not_overclaim() -> None:
    issue_list = (FRONTEND / "components" / "IssueList.tsx").read_text(
        encoding="utf-8"
    )
    # JSX line wrapping must not change this copy contract.
    issue_list = " ".join(issue_list.split())

    assert "Chưa thấy chỗ cần lưu ý theo các quy tắc đã chọn." in issue_list
    assert "Kết quả này không có nghĩa văn bản đã hết lỗi." in issue_list
    assert "Bạn vẫn nên đọc lại theo ngữ cảnh." in issue_list
    assert "Văn bản diễn đạt mượt mà, tự nhiên" not in issue_list
