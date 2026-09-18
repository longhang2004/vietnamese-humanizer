import importlib
import os
import sys
import types
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.capabilities import (
    public_capabilities,
    require_admin_enabled,
    require_contributions_enabled,
    require_rewrite_enabled,
    validate_capability_settings,
)
from app.config import Settings, settings
from app.main import app
from app.proxy import forwarded_client_host, proxy_peer_is_trusted

CAPABILITY_ENV_VARS = (
    "REWRITE_ENABLED",
    "CONTRIBUTIONS_ENABLED",
    "ADMIN_API_ENABLED",
    "GEMINI_API_KEY",
    "ADMIN_API_KEY",
)


def test_capability_test_state_isolated_from_process_environment():
    assert all(os.getenv(name) is None for name in CAPABILITY_ENV_VARS)
    assert settings.REWRITE_ENABLED is False
    assert settings.CONTRIBUTIONS_ENABLED is False
    assert settings.ADMIN_API_ENABLED is False
    assert settings.GEMINI_API_KEY is None
    assert settings.ADMIN_API_KEY is None


def test_isolated_default_lifespan_does_not_initialize_database():
    with patch("app.main.Base.metadata.create_all") as create_all, TestClient(app):
        pass

    create_all.assert_not_called()


def test_capability_settings_default_to_disabled_without_secrets():
    config = Settings(_env_file=None)

    assert config.REWRITE_ENABLED is False
    assert config.CONTRIBUTIONS_ENABLED is False
    assert config.ADMIN_API_ENABLED is False
    assert config.GEMINI_API_KEY is None
    assert config.ADMIN_API_KEY is None
    assert config.TRUSTED_PROXY_HOSTS == "127.0.0.1,localhost,::1"
    assert config.TRUST_PRIVATE_PROXIES is False


def test_testclient_peer_is_not_a_trusted_proxy_by_default(monkeypatch):
    monkeypatch.setattr(settings, "TRUSTED_PROXY_HOSTS", "127.0.0.1,localhost,::1")
    monkeypatch.setattr(settings, "TRUST_PRIVATE_PROXIES", False)
    assert proxy_peer_is_trusted("testclient") is False
    assert proxy_peer_is_trusted("127.0.0.1") is True
    assert proxy_peer_is_trusted("10.0.0.4") is False
    assert proxy_peer_is_trusted("10.0.0.8") is False


def test_trusted_proxy_hosts_accept_cidr(monkeypatch):
    monkeypatch.setattr(settings, "TRUSTED_PROXY_HOSTS", "10.0.0.0/8")
    monkeypatch.setattr(settings, "TRUST_PRIVATE_PROXIES", False)
    assert proxy_peer_is_trusted("10.0.0.8") is True
    assert proxy_peer_is_trusted("192.168.0.9") is False


def test_forwarded_client_skips_trusted_hops(monkeypatch):
    monkeypatch.setattr(settings, "TRUSTED_PROXY_HOSTS", "127.0.0.1,10.0.0.0/8")
    monkeypatch.setattr(settings, "TRUST_PRIVATE_PROXIES", False)
    assert forwarded_client_host("127.0.0.1", "8.8.8.8, 10.0.0.3") == "8.8.8.8"
    assert forwarded_client_host("8.8.8.8", "198.51.100.1") == "8.8.8.8"


def test_proxy_imports_on_uvicorn_without_private_trusted_hosts(monkeypatch):
    stub = types.ModuleType("uvicorn.middleware.proxy_headers")

    class ProxyHeadersMiddleware:
        def __init__(self, app, trusted_hosts="127.0.0.1"):
            self.app = app

    stub.ProxyHeadersMiddleware = ProxyHeadersMiddleware
    original = sys.modules.get("app.proxy")
    monkeypatch.setitem(sys.modules, "uvicorn.middleware.proxy_headers", stub)
    sys.modules.pop("app.proxy", None)
    try:
        module = importlib.import_module("app.proxy")
        monkeypatch.setattr(module.settings, "TRUSTED_PROXY_HOSTS", "127.0.0.1,10.0.0.0/8")
        monkeypatch.setattr(module.settings, "TRUST_PRIVATE_PROXIES", False)
        assert module.proxy_peer_is_trusted("127.0.0.1") is True
        assert module.proxy_peer_is_trusted("10.0.0.8") is True
        assert module.forwarded_client_host("127.0.0.1", "8.8.8.8, 10.0.0.3") == "8.8.8.8"
    finally:
        if original is not None:
            sys.modules["app.proxy"] = original


def test_declared_uvicorn_minimum_remains_0_30():
    pyproject = (Path(__file__).resolve().parents[1] / "pyproject.toml").read_text(
        encoding="utf-8"
    )
    requirements = (Path(__file__).resolve().parents[1] / "requirements.txt").read_text(
        encoding="utf-8"
    )
    assert '"uvicorn>=0.30.0"' in pyproject
    assert "uvicorn>=0.30.0" in requirements


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

    with patch("app.main.Base.metadata.create_all") as create_all, TestClient(app):
        pass

    assert create_all.call_count == expected_calls


def test_lifespan_validates_before_database_initialization(monkeypatch):
    monkeypatch.setattr(settings, "REWRITE_ENABLED", True)
    monkeypatch.setattr(settings, "GEMINI_API_KEY", None)
    monkeypatch.setattr(settings, "CONTRIBUTIONS_ENABLED", True)
    monkeypatch.setattr(settings, "ADMIN_API_ENABLED", False)

    with (
        patch("app.main.Base.metadata.create_all") as create_all,
        pytest.raises(ValueError, match="GEMINI_API_KEY"),
        TestClient(app),
    ):
        pass

    create_all.assert_not_called()
