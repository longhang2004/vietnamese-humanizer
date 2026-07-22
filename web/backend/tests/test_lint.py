from vietnamese_writing_skills import __version__

from app.main import app


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == __version__
    assert data["capabilities"] == {
        "rewrite": False,
        "contributions": False,
    }


def test_optional_routes_remain_mounted_when_capabilities_are_disabled():
    paths = app.openapi()["paths"]

    assert "/api/rewrite" in paths
    assert "/api/contributions" in paths
    assert "/api/admin/contributions" in paths


def test_api_surfaces_expose_core_runtime_version(client):
    health_response = client.get("/api/health")
    lint_response = client.post(
        "/api/lint",
        json={"text": "Một văn bản kiểm tra.", "skills": ["humanizer-vi"]},
    )
    openapi_response = client.get("/openapi.json")

    assert health_response.json()["version"] == __version__
    assert lint_response.json()["version"] == __version__
    assert openapi_response.json()["info"]["version"] == __version__


def test_lint_text_valid(client):
    payload = {
        "text": "Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới. Trong bối cảnh không ngừng phát triển, thị trường yêu cầu linh hoạt.",
        "skills": ["humanizer-vi"],
    }
    response = client.post("/api/lint", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == __version__
    assert "summary" in data
    assert data["summary"]["total"] >= 1
    assert any(i["pattern_id"] == "VI-HUM-L02" for i in data["issues"])


def test_lint_aggregates_occurrences_into_one_finding(client):
    payload = {
        "text": (
            "Một quyết định được thực hiện bởi ban quản lý. "
            "Thay đổi được triển khai bởi đội kỹ thuật."
        ),
        "skills": ["translationese-cleaner-vi"],
    }
    response = client.post("/api/lint", json=payload)

    assert response.status_code == 200
    data = response.json()
    findings = [item for item in data["issues"] if item["pattern_id"] == "VI-TRA-S03"]
    assert len(findings) == 1
    assert data["summary"]["total"] == 1
    assert len(findings[0]["occurrences"]) == 2
    first = findings[0]["occurrences"][0]
    assert (findings[0]["line"], findings[0]["column"], findings[0]["excerpt"]) == (
        first["line"],
        first["column"],
        first["excerpt"],
    )


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
