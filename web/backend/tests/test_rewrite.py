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
        "disclaimer": "Gợi ý do AI tạo. Hãy đối chiếu với bản gốc để kiểm tra dữ kiện và ý nghĩa.",
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


@pytest.mark.parametrize("profile", ["business", "administrative", "social", "marketing"])
def test_rewrite_passes_context_and_profile_to_provider(client, monkeypatch, mock_gemini, profile):
    monkeypatch.setattr(settings, "REWRITE_ENABLED", True)
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test_key")
    style = {
        "profile": profile,
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
    assert "[Reference: formulaic-prose.md]" in prompt
    assert "[Reference: conversational.md]" in prompt
    assert kwargs["config"].response_mime_type == "application/json"


def test_default_profile_keeps_conversation_reference_out(monkeypatch, mock_gemini):
    from app.services.rewriter import generate_rewrite

    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test_key")
    generate_rewrite("Nhóm đã nhận bản nháp.")
    prompt = mock_gemini.models.generate_content.call_args.kwargs["contents"]
    request = json.loads(prompt.split("[Editing Request JSON]\n", 1)[1])
    assert request["style"]["register"] == "preserve"
    assert request["style"]["profile"] == "preserve"
    assert request["style"]["reduce_hype"] is False
    assert "[Reference: conversational.md]" not in prompt
    assert "[Reference: writing-profiles.md]" not in prompt


@pytest.mark.parametrize("skill", ["humanizer-vi", "style-guide-vi"])
@pytest.mark.parametrize(
    "profile", ["plain", "business", "technical", "administrative", "social", "marketing"]
)
def test_writing_profile_loads_only_selected_guidance(skill, profile):
    from app.schemas import RewriteStyle
    from app.services.rewriter import PROFILE_REFERENCES, build_rewrite_prompt

    style = RewriteStyle(profile=profile, channel="email", register="friendly")
    prompt = build_rewrite_prompt("Nhóm chưa chốt lịch.", skill, [], "", style)
    request = json.loads(prompt.split("[Editing Request JSON]\n", 1)[1])
    assert request["style"]["profile"] == profile
    assert request["style"]["channel"] == "email"
    assert request["style"]["register"] == "friendly"
    assert request["style"]["edit_level"] == "light"
    assert "[Reference: writing-profiles.md]" in prompt
    for key, filename in PROFILE_REFERENCES.items():
        assert (f"[Reference: {filename}]" in prompt) is (key == profile)


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
        {"style": {"profile": "../../secrets"}},
        {"style": {"pronouns": "x" * 201}},
        {"style": {"voice_sample": "x" * 1501}},
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


def test_selective_reference_loading_reduces_default_payload():
    from app.schemas import RewriteStyle
    from app.services.rewriter import build_rewrite_prompt

    short_prompt = build_rewrite_prompt(
        "Nhóm chưa chốt lịch.", "humanizer-vi", None, "", RewriteStyle()
    )
    assert "[Reference: preservation-rules.md]" in short_prompt
    assert "[Reference: naturalness.md]" in short_prompt
    assert "[Reference: examples.md]" in short_prompt
    assert "[Reference: formulaic-prose.md]" not in short_prompt
    assert "[Reference: registers.md]" not in short_prompt
    assert "[Reference: workflow.md]" not in short_prompt
    assert "[Reference: conversational.md]" not in short_prompt

    long_text = " ".join(["Nhóm đã chốt lịch họp sáng mai."] * 12)
    long_prompt = build_rewrite_prompt(long_text, "humanizer-vi", None, "", RewriteStyle())
    assert "[Reference: formulaic-prose.md]" in long_prompt

    formulaic_prompt = build_rewrite_prompt(
        "Trong bài viết này, chúng ta sẽ cùng tìm hiểu cách cache hoạt động.",
        "humanizer-vi",
        None,
        "",
        RewriteStyle(),
    )
    assert "[Reference: formulaic-prose.md]" in formulaic_prompt

    profile_prompt = build_rewrite_prompt(
        "Giảm 10% đơn từ 2 sản phẩm.",
        "humanizer-vi",
        None,
        "",
        RewriteStyle(profile="marketing"),
    )
    assert "[Reference: marketing-writing.md]" in profile_prompt
    assert "[Reference: examples.md]" not in profile_prompt


def test_voice_sample_trimming_and_omission(monkeypatch, mock_gemini):
    from app.schemas import RewriteStyle
    from app.services.rewriter import build_rewrite_prompt

    with_sample = build_rewrite_prompt(
        "Nhóm chưa chốt lịch.",
        "humanizer-vi",
        [],
        "",
        RewriteStyle(voice_sample="  Mình vừa kiểm lại bảng chi phí sáng nay.  "),
    )
    request_with = json.loads(with_sample.split("[Editing Request JSON]\n", 1)[1])
    assert request_with["style"]["voice_sample"] == "Mình vừa kiểm lại bảng chi phí sáng nay."

    blank_sample = build_rewrite_prompt(
        "Nhóm chưa chốt lịch.",
        "humanizer-vi",
        [],
        "",
        RewriteStyle(voice_sample="   \n  "),
    )
    request_blank = json.loads(blank_sample.split("[Editing Request JSON]\n", 1)[1])
    assert "voice_sample" not in request_blank["style"]


def test_detected_issues_include_match_excerpts():
    from app.schemas import RewriteStyle
    from app.services.rewriter import build_rewrite_prompt

    prompt = build_rewrite_prompt(
        "Trong bài viết này, chúng ta sẽ cùng tìm hiểu cách lưu bản nháp.",
        "humanizer-vi",
        None,
        "",
        RewriteStyle(),
    )
    request = json.loads(prompt.split("[Editing Request JSON]\n", 1)[1])
    issues = request["detected_issues"]
    assert len(issues) >= 1
    first = issues[0]
    assert first["pattern_id"] == "VI-HUM-D01"
    assert first["finding_type"] == "preference"
    assert first["matches"][0]["line"] == 1
    assert "Trong bài viết này" in first["matches"][0]["matched_text"]
    assert first["matches"][0]["excerpt"]


@pytest.mark.parametrize(
    ("skill", "style_kwargs", "expected_temp"),
    [
        ("grammar-checker-vi", {}, 0.2),
        ("style-guide-vi", {"profile": "social"}, 0.2),
        ("humanizer-vi", {"profile": "technical"}, 0.25),
        ("humanizer-vi", {"profile": "administrative"}, 0.25),
        ("humanizer-vi", {"register": "formal"}, 0.25),
        ("humanizer-vi", {"profile": "social"}, 0.55),
        ("humanizer-vi", {"profile": "marketing"}, 0.55),
        ("humanizer-vi", {"channel": "chat"}, 0.55),
        ("humanizer-vi", {"profile": "plain"}, 0.4),
        ("humanizer-vi", {"profile": "business"}, 0.4),
        ("humanizer-vi", {}, 0.4),
    ],
)
def test_select_temperature_and_pass_to_model(
    skill, style_kwargs, expected_temp, monkeypatch, mock_gemini
):
    from app.schemas import RewriteStyle
    from app.services.rewriter import generate_rewrite, select_temperature

    style = RewriteStyle(**style_kwargs)
    assert select_temperature(skill, style) == expected_temp
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test_key")
    generate_rewrite("Bản nháp ngắn.", skill=skill, style=style)
    config = mock_gemini.models.generate_content.call_args.kwargs["config"]
    assert config.temperature == expected_temp


def test_preservation_check_stays_internal_to_model_schema(monkeypatch, mock_gemini):
    from app.services.rewriter import generate_rewrite

    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test_key")
    mock_gemini.models.generate_content.return_value.text = json.dumps(
        {
            "preservation_check": "Giữ mốc 15:00 và cặp xưng hô mình–bạn.",
            "output_mode": "clean_rewrite",
            "rewrite": "Bạn gửi bản nháp trước 15:00 nhé.",
            "comments": [],
        }
    )
    result = generate_rewrite("Vui lòng thực hiện việc gửi bản nháp trước 15:00.")
    dumped = result.model_dump()
    assert "preservation_check" not in dumped
    assert result.rewrite == "Bạn gửi bản nháp trước 15:00 nhé."
    assert result.comments == []


def test_deterministic_preservation_audit_flags_dropped_immutable_tokens(monkeypatch, mock_gemini):
    from app.schemas import RewriteStyle
    from app.services.rewriter import generate_rewrite

    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test_key")
    original = (
        "Chạy `app.py`, xem https://example.com/guide "
        "trước 15:00 ngày 20/11/2026 để giảm 10%."
    )
    mock_gemini.models.generate_content.return_value.text = json.dumps(
        {
            "output_mode": "clean_rewrite",
            "rewrite": "Xem hướng dẫn trước buổi chiều để được ưu đãi.",
            "comments": [],
        }
    )
    flagged = generate_rewrite(original, skill="humanizer-vi")
    assert flagged.output_mode == "clean_rewrite"
    assert len(flagged.comments) == 1
    assert "`app.py`" in flagged.comments[0]
    assert "https://example.com/guide" in flagged.comments[0]
    assert "15:00" in flagged.comments[0]
    assert "20/11/2026" in flagged.comments[0]
    assert "10%" in flagged.comments[0]

    skipped_style_guide = generate_rewrite(original, skill="style-guide-vi")
    assert skipped_style_guide.comments == []

    skipped_spoken = generate_rewrite(
        original,
        skill="humanizer-vi",
        style=RewriteStyle(channel="spoken_script"),
    )
    assert skipped_spoken.comments == []


def test_humor_and_satire_reference_loads_selectively():
    from app.schemas import RewriteStyle
    from app.services.rewriter import build_rewrite_prompt

    technical = build_rewrite_prompt(
        "Cụm máy chủ sao lưu lúc 02:00 mỗi ngày.",
        "humanizer-vi",
        None,
        "Tài liệu vận hành định kỳ.",
        RewriteStyle(profile="technical"),
    )
    assert "[Reference: humor-and-satire.md]" not in technical

    social = build_rewrite_prompt(
        "Cuối tháng tài khoản còn 38 nghìn.",
        "humanizer-vi",
        None,
        "",
        RewriteStyle(profile="social"),
    )
    assert "[Reference: humor-and-satire.md]" in social

    satire_by_context = build_rewrite_prompt(
        "Lễ tiết kiệm giấy gửi 300 thư mời in màu.",
        "humanizer-vi",
        None,
        "Giữ giọng trào phúng, khen ngược.",
        RewriteStyle(),
    )
    assert "[Reference: humor-and-satire.md]" in satire_by_context

    spoken_banter = build_rewrite_prompt(
        "Chờ chút, để mình mở hộp thử.",
        "humanizer-vi",
        None,
        "Lời dẫn vlog có chút dí dỏm.",
        RewriteStyle(channel="spoken_script"),
    )
    assert "[Reference: conversational.md]" in spoken_banter
    assert "[Reference: humor-and-satire.md]" in spoken_banter


def test_new_humanizer_patterns_trigger_matching_references():
    from app.schemas import RewriteStyle
    from app.services.rewriter import build_rewrite_prompt

    video_meta = build_rewrite_prompt(
        "Trong video ngày hôm nay, chúng ta sẽ cùng xem cách pin giảm dung lượng.",
        "humanizer-vi",
        None,
        "",
        RewriteStyle(),
    )
    assert "[Reference: formulaic-prose.md]" in video_meta
    assert "[Reference: conversational.md]" in video_meta

    joke_explainer = build_rewrite_prompt(
        "Cả nhóm họp 3 tiếng để đổi cỡ chữ từ 14 lên 16. "
        "Điều này quả thực là một tình huống dở khóc dở cười.",
        "humanizer-vi",
        None,
        "",
        RewriteStyle(),
    )
    assert "[Reference: formulaic-prose.md]" in joke_explainer
    assert "[Reference: humor-and-satire.md]" in joke_explainer
