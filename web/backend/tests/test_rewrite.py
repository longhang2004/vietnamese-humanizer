from unittest.mock import Mock

from app.config import settings


def test_rewrite_disabled_returns_503_before_provider_call(client, monkeypatch):
    provider = Mock(
        return_value={
            "rewrite": "sentinel rewrite",
            "review_status": "unreviewed",
            "disclaimer": "sentinel disclaimer",
        }
    )
    monkeypatch.setattr("app.routers.rewrite.generate_rewrite", provider)
    payload = {
        "text": "Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới.",
        "skill": "humanizer-vi",
    }

    response = client.post("/api/rewrite", json=payload)

    assert response.status_code == 503
    assert response.json() == {"detail": "Capability is disabled."}
    provider.assert_not_called()


def test_rewrite_disabled_rejects_malformed_json_before_parsing_or_provider_call(
    client, monkeypatch
):
    provider = Mock()
    monkeypatch.setattr("app.routers.rewrite.generate_rewrite", provider)

    response = client.post(
        "/api/rewrite",
        content=b'{"text":',
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 503
    assert response.json() == {"detail": "Capability is disabled."}
    provider.assert_not_called()


def test_rewrite_missing_gemini_key(client, monkeypatch):
    monkeypatch.setattr(settings, "REWRITE_ENABLED", True)
    monkeypatch.setattr(settings, "GEMINI_API_KEY", None)
    payload = {
        "text": "Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới.",
        "skill": "humanizer-vi",
    }
    response = client.post("/api/rewrite", json=payload)
    assert response.status_code == 503
    assert "GEMINI_API_KEY" in response.json()["detail"]


def test_rewrite_with_gemini_key(client, monkeypatch, mock_gemini):
    monkeypatch.setattr(settings, "REWRITE_ENABLED", True)
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "dummy_test_key")
    payload = {
        "text": "Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới.",
        "skill": "humanizer-vi",
        "issue_ids": ["VI-HUM-L02"],
    }
    response = client.post("/api/rewrite", json=payload)
    assert response.status_code == 200
    assert response.json() == {
        "rewrite": "Bản dịch/viết lại đã được gọt giũa tự nhiên hơn.",
        "review_status": "unreviewed",
        "disclaimer": "Gợi ý do model sinh, cần người đọc kiểm chứng bảo toàn dữ kiện.",
    }


def test_rewrite_sends_full_skill_prompt_to_supported_model(monkeypatch, mock_gemini):
    from app.services.rewriter import generate_rewrite

    monkeypatch.setattr(settings, "GEMINI_API_KEY", "dummy_test_key")
    generate_rewrite("Trong bối cảnh không ngừng phát triển.", "humanizer-vi")

    kwargs = mock_gemini.models.generate_content.call_args.kwargs
    prompt = kwargs["contents"]
    assert kwargs["model"] == "gemini-2.5-flash"
    assert "Anti-goals" in prompt
    assert "Đầu ra" in prompt
    assert "gemini-2.0-flash" not in str(kwargs)


def test_rewrite_fallback_skips_retired_flash(monkeypatch, mock_gemini):
    from unittest.mock import MagicMock

    from app.services.rewriter import generate_rewrite

    monkeypatch.setattr(settings, "GEMINI_API_KEY", "dummy_test_key")
    success = MagicMock()
    success.text = "Bản viết lại."
    mock_gemini.models.generate_content.side_effect = [RuntimeError("unavailable"), success]

    generate_rewrite("Trong bối cảnh không ngừng phát triển.")

    models = [
        call.kwargs["model"] for call in mock_gemini.models.generate_content.call_args_list
    ]
    assert models[0] == "gemini-2.5-flash"
    assert "gemini-2.0-flash" not in models
    assert models[-1].startswith("gemini-2.5")


def test_rewrite_provider_failure_does_not_expose_exception_details(client, monkeypatch):
    secret = "gemini-secret-token"
    raw_fragment = "[Original Text] confidential customer fragment"
    provider = Mock(side_effect=RuntimeError(f"{secret}: {raw_fragment}"))
    monkeypatch.setattr(settings, "REWRITE_ENABLED", True)
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "dummy_test_key")
    monkeypatch.setattr("app.routers.rewrite.generate_rewrite", provider)
    payload = {
        "text": "Trong bối cảnh không ngừng phát triển, doanh nghiệp cần đổi mới.",
        "skill": "humanizer-vi",
    }

    response = client.post("/api/rewrite", json=payload)

    assert response.status_code == 500
    assert response.json() == {"detail": "Không thể xử lý yêu cầu viết lại."}
    assert secret not in response.text
    assert raw_fragment not in response.text
