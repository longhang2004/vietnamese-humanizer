from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.config import settings
from app.db.database import get_db
from app.main import app
from app.routers import admin


@pytest.mark.parametrize(
    ("method", "path", "json_body"),
    [
        ("GET", "/api/admin/contributions", None),
        (
            "PATCH",
            "/api/admin/contributions/missing-id",
            {"status": "approved", "review_note": "Không được xử lý"},
        ),
        ("GET", "/api/admin/contributions/export?status=approved", None),
    ],
)
def test_admin_disabled_returns_503_before_authentication_or_database_access(
    client, db_session, method, path, json_body
):
    database_dependency_entered = False

    def tracked_get_db():
        nonlocal database_dependency_entered
        database_dependency_entered = True
        yield db_session

    app.dependency_overrides[get_db] = tracked_get_db

    response = client.request(method, path, json=json_body)

    assert response.status_code == 503
    assert response.json() == {"detail": "Capability is disabled."}
    assert database_dependency_entered is False


def test_admin_disabled_rejects_malformed_json_before_database_access(client, db_session):
    database_dependency_entered = False

    def tracked_get_db():
        nonlocal database_dependency_entered
        database_dependency_entered = True
        yield db_session

    app.dependency_overrides[get_db] = tracked_get_db

    response = client.patch(
        "/api/admin/contributions/missing-id",
        content="{",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 503
    assert response.json() == {"detail": "Capability is disabled."}
    assert database_dependency_entered is False


def test_admin_unauthorized(client, monkeypatch):
    monkeypatch.setattr(settings, "ADMIN_API_ENABLED", True)
    monkeypatch.setattr(settings, "ADMIN_API_KEY", "a" * 32)

    response = client.get("/api/admin/contributions")
    assert response.status_code == 401

    response = client.get("/api/admin/contributions", headers={"X-Admin-Key": "wrong_key"})
    assert response.status_code == 401


def test_admin_flow(client, monkeypatch):
    admin_key = "secret-admin-test-key-at-least-32"
    monkeypatch.setattr(settings, "CONTRIBUTIONS_ENABLED", True)
    monkeypatch.setattr(settings, "ADMIN_API_ENABLED", True)
    monkeypatch.setattr(settings, "ADMIN_API_KEY", admin_key)
    headers = {"X-Admin-Key": admin_key}

    # 1. Create a contribution first
    contrib_payload = {
        "input_text": "Văn bản thử nghiệm admin",
        "suggestion": "Văn bản sửa admin",
        "skill": "humanizer-vi",
        "pattern_ids": ["VI-HUM-L02"],
        "consent": True,
    }
    contrib_resp = client.post("/api/contributions", json=contrib_payload)
    assert contrib_resp.status_code == 200
    contrib_id = contrib_resp.json()["id"]

    # 2. List pending contributions
    list_resp = client.get("/api/admin/contributions?status=pending", headers=headers)
    assert list_resp.status_code == 200
    pending_items = list_resp.json()
    assert any(item["id"] == contrib_id for item in pending_items)

    # 3. Patch contribution status to approved
    patch_resp = client.patch(
        f"/api/admin/contributions/{contrib_id}",
        json={"status": "approved", "review_note": "Đã kiểm duyệt tốt"},
        headers=headers,
    )
    assert patch_resp.status_code == 200
    patched_data = patch_resp.json()
    assert patched_data["status"] == "approved"
    assert patched_data["review_note"] == "Đã kiểm duyệt tốt"

    # 4. Export approved contributions
    export_resp = client.get("/api/admin/contributions/export?status=approved", headers=headers)
    assert export_resp.status_code == 200
    export_data = export_resp.json()
    assert len(export_data) >= 1
    assert any(item["id"] == contrib_id for item in export_data)


def test_admin_authentication_uses_compare_digest(client, monkeypatch):
    admin_key = "constant-time-admin-key-at-least-32"
    compare_digest = Mock(return_value=False)
    monkeypatch.setattr(settings, "ADMIN_API_ENABLED", True)
    monkeypatch.setattr(settings, "ADMIN_API_KEY", admin_key)
    monkeypatch.setattr(
        admin,
        "secrets",
        SimpleNamespace(compare_digest=compare_digest),
        raising=False,
    )

    response = client.get(
        "/api/admin/contributions",
        headers={"X-Admin-Key": "wrong_key"},
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Unauthorized: X-Admin-Key header missing or invalid."
    }
    compare_digest.assert_called_once_with(b"wrong_key", admin_key.encode())


def test_admin_authentication_accepts_matching_unicode_keys(monkeypatch):
    admin_key = "khóa-quản-trị-bí-mật-đủ-dài-🔐"
    monkeypatch.setattr(settings, "ADMIN_API_KEY", admin_key)

    assert admin.verify_admin_key(admin_key) is None


def test_admin_authentication_rejects_mismatched_unicode_keys_with_existing_401(
    monkeypatch,
):
    monkeypatch.setattr(settings, "ADMIN_API_KEY", "khóa-quản-trị-bí-mật-đủ-dài-🔐")

    with pytest.raises(HTTPException) as exc_info:
        admin.verify_admin_key("khóa-quản-trị-không-đúng-🔓")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Unauthorized: X-Admin-Key header missing or invalid."
