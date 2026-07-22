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

    assert "Không tìm thấy tín hiệu trong bộ quy tắc hiện tại." in issue_list
    assert "Văn bản vẫn nên được người viết rà lại theo ngữ cảnh." in issue_list
    assert "Văn bản diễn đạt mượt mà, tự nhiên" not in issue_list
