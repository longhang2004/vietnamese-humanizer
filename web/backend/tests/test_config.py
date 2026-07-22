from unittest.mock import patch

from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest

from app.capabilities import (
    public_capabilities,
    require_admin_enabled,
    require_contributions_enabled,
    require_rewrite_enabled,
    validate_capability_settings,
)
from app.config import Settings, settings
from app.main import app


def test_capability_settings_default_to_disabled_without_secrets():
    config = Settings(_env_file=None)

    assert config.REWRITE_ENABLED is False
    assert config.CONTRIBUTIONS_ENABLED is False
    assert config.ADMIN_API_ENABLED is False
    assert config.GEMINI_API_KEY is None
    assert config.ADMIN_API_KEY is None


def test_rewrite_can_be_enabled_with_a_gemini_key():
    config = Settings(REWRITE_ENABLED=True, GEMINI_API_KEY="gemini-test-key", _env_file=None)

    validate_capability_settings(config)


@pytest.mark.parametrize("gemini_key", [None, "", "   "])
def test_rewrite_enabled_requires_a_non_empty_gemini_key(gemini_key):
    config = Settings(REWRITE_ENABLED=True, GEMINI_API_KEY=gemini_key, _env_file=None)

    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        validate_capability_settings(config)


def test_admin_can_be_enabled_with_a_strong_key():
    config = Settings(ADMIN_API_ENABLED=True, ADMIN_API_KEY="a" * 32, _env_file=None)

    validate_capability_settings(config)


@pytest.mark.parametrize(
    "admin_key",
    [
        None,
        "",
        " " * 32,
        "a" * 31,
        "change_this_secret_admin_key_at_least_32_chars",
        "replace-me-with-a-real-random-secret-now",
        "your_admin_api_key_here_replace_me_now",
    ],
)
def test_admin_enabled_rejects_missing_short_or_placeholder_keys(admin_key):
    config = Settings(ADMIN_API_ENABLED=True, ADMIN_API_KEY=admin_key, _env_file=None)

    with pytest.raises(ValueError, match="ADMIN_API_KEY"):
        validate_capability_settings(config)


def test_public_capabilities_include_only_effective_public_features(monkeypatch):
    monkeypatch.setattr(settings, "REWRITE_ENABLED", True)
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "   ")
    monkeypatch.setattr(settings, "CONTRIBUTIONS_ENABLED", True)
    monkeypatch.setattr(settings, "ADMIN_API_ENABLED", True)
    monkeypatch.setattr(settings, "ADMIN_API_KEY", "a" * 32)

    assert public_capabilities() == {
        "rewrite": False,
        "contributions": True,
    }


@pytest.mark.parametrize(
    ("dependency", "setting_name"),
    [
        (require_rewrite_enabled, "REWRITE_ENABLED"),
        (require_contributions_enabled, "CONTRIBUTIONS_ENABLED"),
        (require_admin_enabled, "ADMIN_API_ENABLED"),
    ],
)
def test_disabled_capability_dependencies_return_stable_503(
    monkeypatch, dependency, setting_name
):
    monkeypatch.setattr(settings, setting_name, False)

    with pytest.raises(HTTPException) as exc_info:
        dependency()

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Capability is disabled."


@pytest.mark.parametrize(
    ("dependency", "setting_name"),
    [
        (require_rewrite_enabled, "REWRITE_ENABLED"),
        (require_contributions_enabled, "CONTRIBUTIONS_ENABLED"),
        (require_admin_enabled, "ADMIN_API_ENABLED"),
    ],
)
def test_enabled_capability_dependencies_allow_requests(
    monkeypatch, dependency, setting_name
):
    monkeypatch.setattr(settings, setting_name, True)

    assert dependency() is None


@pytest.mark.parametrize(
    ("contributions_enabled", "admin_enabled", "expected_calls"),
    [
        (False, False, 0),
        (True, False, 1),
        (False, True, 1),
        (True, True, 1),
    ],
)
def test_lifespan_initializes_database_only_for_storage_capabilities(
    monkeypatch, contributions_enabled, admin_enabled, expected_calls
):
    monkeypatch.setattr(settings, "REWRITE_ENABLED", False)
    monkeypatch.setattr(settings, "CONTRIBUTIONS_ENABLED", contributions_enabled)
    monkeypatch.setattr(settings, "ADMIN_API_ENABLED", admin_enabled)
    monkeypatch.setattr(settings, "ADMIN_API_KEY", "a" * 32 if admin_enabled else None)

    with patch("app.main.Base.metadata.create_all") as create_all:
        with TestClient(app):
            pass

    assert create_all.call_count == expected_calls


def test_lifespan_validates_before_database_initialization(monkeypatch):
    monkeypatch.setattr(settings, "REWRITE_ENABLED", True)
    monkeypatch.setattr(settings, "GEMINI_API_KEY", None)
    monkeypatch.setattr(settings, "CONTRIBUTIONS_ENABLED", True)
    monkeypatch.setattr(settings, "ADMIN_API_ENABLED", False)

    with patch("app.main.Base.metadata.create_all") as create_all:
        with pytest.raises(ValueError, match="GEMINI_API_KEY"):
            with TestClient(app):
                pass

    create_all.assert_not_called()
