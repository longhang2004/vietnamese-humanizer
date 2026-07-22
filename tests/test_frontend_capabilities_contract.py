"""Frontend optional features must follow the backend capability contract."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "web" / "frontend"


def read_frontend(path: str) -> str:
    return (FRONTEND / path).read_text(encoding="utf-8")


def test_frontend_defines_and_fetches_the_health_capability_contract() -> None:
    types = read_frontend("lib/types.ts")
    api = read_frontend("lib/api.ts")

    assert "export interface HealthResponse" in types
    assert "capabilities:" in types
    assert "rewrite: boolean" in types
    assert "contributions: boolean" in types
    assert "export async function fetchHealth()" in api
    assert "`${API_BASE}/api/health`" in api
    assert "handleResponse<HealthResponse>(res)" in api


def test_optional_frontend_features_fail_closed_without_blocking_lint() -> None:
    capability_nav = read_frontend("components/CapabilityNav.tsx")
    layout = read_frontend("app/layout.tsx")
    home = read_frontend("app/page.tsx")
    contribute = read_frontend("app/contribute/page.tsx")

    assert '"use client"' in capability_nav
    assert "rewrite: false" in capability_nav
    assert "contributions: false" in capability_nav
    assert "fetchHealth()" in capability_nav
    assert "health.capabilities.rewrite === true" in capability_nav
    assert "health.capabilities.contributions === true" in capability_nav
    assert "capabilities.contributions &&" in capability_nav

    assert "<CapabilityProvider>" in layout
    assert "<CapabilityNav />" in layout
    assert "<Analytics />" in layout

    assert "const capabilities = useCapabilities()" in home
    assert "capabilities.rewrite &&" in home
    assert "lintText(text, selectedSkills)" in home

    assert "const capabilities = useCapabilities()" in contribute
    assert "if (!capabilities.contributions)" in contribute
    assert "<ContributeForm skills={skills} />" in contribute


def test_frontend_keeps_analytics_root_only_without_custom_events() -> None:
    frontend_sources = "\n".join(
        path.read_text(encoding="utf-8")
        for path in FRONTEND.rglob("*")
        if path.suffix in {".ts", ".tsx"}
        and ".next" not in path.parts
        and "node_modules" not in path.parts
    )
    layout = read_frontend("app/layout.tsx")

    assert 'import { Analytics } from "@vercel/analytics/react";' in layout
    assert layout.count("<Analytics />") == 1
    assert "track(" not in frontend_sources
    assert "event(" not in frontend_sources
