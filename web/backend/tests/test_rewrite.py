from app.config import settings


def test_rewrite_missing_gemini_key(client, monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", None)
    payload = {
        "text": "Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới.",
        "skill": "humanizer-vi",
    }
    response = client.post("/api/rewrite", json=payload)
    assert response.status_code == 503
    assert "GEMINI_API_KEY" in response.json()["detail"]


def test_rewrite_with_gemini_key(client, monkeypatch, mock_gemini):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "dummy_test_key")
    payload = {
        "text": "Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới.",
        "skill": "humanizer-vi",
        "issue_ids": ["VI-HUM-L02"],
    }
    response = client.post("/api/rewrite", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["review_status"] == "unreviewed"
    assert "Gợi ý do model sinh" in data["disclaimer"]
    assert "rewrite" in data
    assert data["rewrite"] == "Bản dịch/viết lại đã được gọt giũa tự nhiên hơn."
