def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_lint_text_valid(client):
    payload = {
        "text": "Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới. Trong bối cảnh không ngừng phát triển, thị trường yêu cầu linh hoạt.",
        "skills": ["humanizer-vi"],
    }
    response = client.post("/api/lint", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "0.4.1"
    assert "summary" in data
    assert data["summary"]["total"] >= 1
    assert any(i["pattern_id"] == "VI-HUM-L02" for i in data["issues"])


def test_lint_text_invalid_skills(client):
    payload = {
        "text": "Một văn bản kiểm tra.",
        "skills": ["invalid-skill-name"],
    }
    response = client.post("/api/lint", json=payload)
    assert response.status_code == 400
    assert "Kỹ năng không hợp lệ" in response.json()["detail"]


def test_lint_text_empty(client):
    payload = {
        "text": "   ",
    }
    response = client.post("/api/lint", json=payload)
    assert response.status_code == 400
