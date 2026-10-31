import json
from unittest.mock import Mock

import pytest

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
        "output_mode": "clean_rewrite",
        "comments": [],
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
    success.text = json.dumps(
        {
            "output_mode": "clean_rewrite",
            "rewrite": "Bản viết lại.",
            "comments": [],
        }
    )
    mock_gemini.models.generate_content.side_effect = [RuntimeError("unavailable"), success]

    generate_rewrite("Trong bối cảnh không ngừng phát triển.")

    models = [call.kwargs["model"] for call in mock_gemini.models.generate_content.call_args_list]
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


def test_rewrite_passes_context_and_profile_to_provider(client, monkeypatch, mock_gemini):
    monkeypatch.setattr(settings, "REWRITE_ENABLED", True)
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test_key")
    style = {
        "channel": "chat",
        "register": "friendly",
        "audience": "đồng nghiệp",
        "relationship": "đã làm việc cùng nhóm",
        "pronouns": "mình–bạn",
        "edit_level": "moderate",
        "reduce_hype": True,
    }
    response = client.post(
        "/api/rewrite",
        json={
            "text": "Bạn gửi lại bản nháp giúp mình.",
            "context": "Hạn là 15:00.",
            "style": style,
            "issue_ids": [],
        },
    )
    assert response.status_code == 200
    kwargs = mock_gemini.models.generate_content.call_args.kwargs
    prompt = kwargs["contents"]
    request = json.loads(prompt.split("[Editing Request JSON]\n", 1)[1])
    assert request["style"] == style
    assert request["context"] == "Hạn là 15:00."
    assert request["original_text"] == "Bạn gửi lại bản nháp giúp mình."
    assert request["detected_issues"] == []
    assert "[Reference: naturalness.md]" in prompt
    assert "[Reference: conversational.md]" in prompt
    assert kwargs["config"].response_mime_type == "application/json"


def test_default_profile_keeps_conversation_reference_out(monkeypatch, mock_gemini):
    from app.services.rewriter import generate_rewrite

    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test_key")
    generate_rewrite("Nhóm đã nhận bản nháp.")
    prompt = mock_gemini.models.generate_content.call_args.kwargs["contents"]
    request = json.loads(prompt.split("[Editing Request JSON]\n", 1)[1])
    assert request["style"]["register"] == "preserve"
    assert request["style"]["reduce_hype"] is False
    assert "[Reference: conversational.md]" not in prompt


@pytest.mark.parametrize("mode", ["review_comment", "needs_author_decision"])
def test_review_modes_never_expose_replacement_text(mode, monkeypatch, mock_gemini):
    from app.services.rewriter import generate_rewrite

    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test_key")
    mock_gemini.models.generate_content.return_value.text = json.dumps(
        {
            "output_mode": mode,
            "rewrite": "Không được dùng làm replacement.",
            "comments": ["  Cần làm rõ người chịu trách nhiệm.  "],
        }
    )
    result = generate_rewrite("Họ sẽ kiểm tra.")
    assert result.output_mode == mode
    assert result.rewrite == ""
    assert result.comments == ["Cần làm rõ người chịu trách nhiệm."]


def test_no_change_returns_original_byte_for_byte(monkeypatch, mock_gemini):
    from app.services.rewriter import generate_rewrite

    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test_key")
    original = "  Nhóm vẫn chưa chốt.\n\nGiữ 15:00.\n"
    mock_gemini.models.generate_content.return_value.text = json.dumps(
        {
            "output_mode": "no_change",
            "rewrite": "Model accidentally changed this.",
            "comments": [],
        }
    )
    result = generate_rewrite(original)
    assert result.output_mode == "no_change"
    assert result.rewrite == original


@pytest.mark.parametrize(
    "result",
    [
        "not JSON",
        '{"output_mode":"clean_rewrite","rewrite":"  ","comments":[]}',
        '{"output_mode":"review_comment","rewrite":"","comments":[" "]}',
    ],
)
def test_invalid_provider_result_fails_instead_of_pretending_success(
    result, client, monkeypatch, mock_gemini
):
    monkeypatch.setattr(settings, "REWRITE_ENABLED", True)
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test_key")
    mock_gemini.models.generate_content.return_value.text = result
    response = client.post("/api/rewrite", json={"text": "Một văn bản cần kiểm tra."})
    assert response.status_code == 500
    assert mock_gemini.models.generate_content.call_count == 2
    assert response.json() == {"detail": "Không thể xử lý yêu cầu viết lại."}


@pytest.mark.parametrize(
    "extra",
    [
        {"style": {"channel": "../../other-skill"}},
        {"style": {"register": "invented"}},
        {"style": {"pronouns": "x" * 201}},
        {"context": "x" * 5001},
    ],
)
def test_invalid_style_is_rejected_before_provider(extra, client, monkeypatch):
    monkeypatch.setattr(settings, "REWRITE_ENABLED", True)
    provider = Mock()
    monkeypatch.setattr("app.routers.rewrite.generate_rewrite", provider)
    response = client.post("/api/rewrite", json={"text": "Bản nháp.", **extra})
    assert response.status_code == 422
    provider.assert_not_called()
