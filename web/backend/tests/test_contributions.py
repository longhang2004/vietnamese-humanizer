from app.limiter import limiter


def test_contribution_without_consent(client):
    payload = {
        "input_text": "Cơ quan chức năng tiến hành kiểm tra.",
        "suggestion": "Nhà chức trách kiểm tra.",
        "skill": "humanizer-vi",
        "consent": False,
    }
    response = client.post("/api/contributions", json=payload)
    assert response.status_code == 400
    assert "consent=true" in response.json()["detail"]


def test_contribution_success(client):
    payload = {
        "input_text": "Trong bối cảnh không ngừng phát triển...",
        "context": "Văn bản doanh nghiệp",
        "suggestion": "Doanh nghiệp liên tục đổi mới...",
        "skill": "humanizer-vi",
        "pattern_ids": ["VI-HUM-L02"],
        "note": "Cần sửa câu dẫn dài dòng",
        "consent": True,
    }
    response = client.post("/api/contributions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["status"] == "pending"
    assert "Cảm ơn đóng góp" in data["message"]


def test_contribution_invalid_skill(client):
    payload = {
        "input_text": "Văn bản mẫu",
        "suggestion": "Văn bản sửa",
        "skill": "invalid-skill",
        "consent": True,
    }
    response = client.post("/api/contributions", json=payload)
    assert response.status_code == 400
    assert "Kỹ năng không hợp lệ" in response.json()["detail"]


def test_contribution_rate_limit(client):
    limiter.enabled = True
    payload = {
        "input_text": "Văn bản thử rate limit",
        "suggestion": "Văn bản gợi ý",
        "skill": "humanizer-vi",
        "consent": True,
    }
    # 3 requests per minute allowed
    for _ in range(3):
        res = client.post("/api/contributions", json=payload)
        assert res.status_code in (200, 400)

    # 4th request should return 429
    res_exceeded = client.post("/api/contributions", json=payload)
    assert res_exceeded.status_code == 429
    limiter.enabled = False
