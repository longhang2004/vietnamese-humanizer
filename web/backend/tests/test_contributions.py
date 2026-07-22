from app.config import settings
from app.db.database import get_db
from app.db.models import Contribution
from app.limiter import limiter
from app.main import app


def test_contribution_disabled_returns_503_before_database_access(client, db_session):
    database_dependency_entered = False

    def tracked_get_db():
        nonlocal database_dependency_entered
        database_dependency_entered = True
        yield db_session

    app.dependency_overrides[get_db] = tracked_get_db
    payload = {
        "input_text": "Văn bản không được lưu khi tính năng bị tắt.",
        "suggestion": "Không lưu văn bản này.",
        "skill": "humanizer-vi",
        "consent": True,
    }

    response = client.post("/api/contributions", json=payload)

    assert response.status_code == 503
    assert response.json() == {"detail": "Capability is disabled."}
    assert database_dependency_entered is False
    assert db_session.query(Contribution).count() == 0


def test_contribution_disabled_rejects_malformed_json_before_database_access(
    client, db_session
):
    database_dependency_entered = False

    def tracked_get_db():
        nonlocal database_dependency_entered
        database_dependency_entered = True
        yield db_session

    app.dependency_overrides[get_db] = tracked_get_db

    response = client.post(
        "/api/contributions",
        content="{",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 503
    assert response.json() == {"detail": "Capability is disabled."}
    assert database_dependency_entered is False
    assert db_session.query(Contribution).count() == 0


def test_contribution_without_consent(client, monkeypatch):
    monkeypatch.setattr(settings, "CONTRIBUTIONS_ENABLED", True)
    payload = {
        "input_text": "Cơ quan chức năng tiến hành kiểm tra.",
        "suggestion": "Nhà chức trách kiểm tra.",
        "skill": "humanizer-vi",
        "consent": False,
    }
    response = client.post("/api/contributions", json=payload)
    assert response.status_code == 400
    assert "consent=true" in response.json()["detail"]


def test_contribution_success(client, monkeypatch):
    monkeypatch.setattr(settings, "CONTRIBUTIONS_ENABLED", True)
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


def test_contribution_invalid_skill(client, monkeypatch):
    monkeypatch.setattr(settings, "CONTRIBUTIONS_ENABLED", True)
    payload = {
        "input_text": "Văn bản mẫu",
        "suggestion": "Văn bản sửa",
        "skill": "invalid-skill",
        "consent": True,
    }
    response = client.post("/api/contributions", json=payload)
    assert response.status_code == 400
    assert "Kỹ năng không hợp lệ" in response.json()["detail"]


def test_contribution_rate_limit(client, monkeypatch):
    monkeypatch.setattr(settings, "CONTRIBUTIONS_ENABLED", True)
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
