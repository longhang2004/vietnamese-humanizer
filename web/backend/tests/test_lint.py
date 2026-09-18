from fastapi.testclient import TestClient
from vietnamese_writing_skills import __version__

from app.config import settings
from app.limiter import limiter
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
        "text": (
            "Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới. "
            "Trong bối cảnh không ngừng phát triển, thị trường yêu cầu linh hoạt."
        ),
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


def _enable_lint_rate_limit(monkeypatch):
    monkeypatch.setattr(
        "app.routers.lint.run_linter",
        lambda **_kwargs: {
            "version": "0.4.6",
            "summary": {
                "total": 0,
                "error": 0,
                "warning": 0,
                "preference": 0,
                "heuristic": 0,
                "note": "test",
            },
            "issues": [],
        },
    )
    limiter.enabled = True
    storage = getattr(limiter, "_storage", None)
    inner = getattr(storage, "storage", None) if storage is not None else None
    if isinstance(inner, dict):
        inner.clear()
    return limiter


def test_lint_rate_limit_ignores_untrusted_forwarded_for(client, monkeypatch):
    limiter = _enable_lint_rate_limit(monkeypatch)
    payload = {"text": "Một văn bản kiểm tra."}
    statuses = []
    for index in range(32):
        response = client.post(
            "/api/lint",
            json=payload,
            headers={"X-Forwarded-For": f"198.51.100.{index}"},
        )
        statuses.append(response.status_code)

    assert statuses.count(200) == 30
    assert statuses.count(429) == 2
    limiter.enabled = False


def test_lint_rate_limit_ignores_xff_from_undeclared_private_peer(monkeypatch):
    limiter = _enable_lint_rate_limit(monkeypatch)
    monkeypatch.setattr(settings, "TRUSTED_PROXY_HOSTS", "127.0.0.1,localhost,::1")
    payload = {"text": "Một văn bản kiểm tra."}
    statuses = []
    with TestClient(app, client=("10.0.0.8", 50000)) as private_client:
        for index in range(32):
            response = private_client.post(
                "/api/lint",
                json=payload,
                headers={"X-Forwarded-For": f"198.51.100.{index}"},
            )
            statuses.append(response.status_code)

    assert statuses.count(200) == 30
    assert statuses.count(429) == 2
    limiter.enabled = False


def test_lint_rate_limit_uses_client_before_trusted_proxy_hops(monkeypatch):
    limiter = _enable_lint_rate_limit(monkeypatch)
    monkeypatch.setattr(settings, "TRUSTED_PROXY_HOSTS", "127.0.0.1,10.0.0.0/8")
    monkeypatch.setattr(settings, "TRUST_PRIVATE_PROXIES", False)
    payload = {"text": "Một văn bản kiểm tra."}
    statuses = []
    with TestClient(app, client=("127.0.0.1", 50000)) as proxy_client:
        for index in range(32):
            response = proxy_client.post(
                "/api/lint",
                json=payload,
                headers={"X-Forwarded-For": f"198.51.100.{index}, 10.0.0.3"},
            )
            statuses.append(response.status_code)

    assert statuses.count(200) == 32
    assert statuses.count(429) == 0
    limiter.enabled = False
