from app.config import settings


def test_admin_unauthorized(client):
    response = client.get("/api/admin/contributions")
    assert response.status_code == 401

    response = client.get("/api/admin/contributions", headers={"X-Admin-Key": "wrong_key"})
    assert response.status_code == 401


def test_admin_flow(client, monkeypatch):
    admin_key = "secret_admin_test_key"
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
