"""Frontend metadata must use the canonical product identity."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "web" / "frontend"


def test_frontend_uses_canonical_branding_without_a_runtime_version() -> None:
    layout = (FRONTEND / "app" / "layout.tsx").read_text(encoding="utf-8")
    package = json.loads((FRONTEND / "package.json").read_text(encoding="utf-8"))
    package_lock = json.loads((FRONTEND / "package-lock.json").read_text(encoding="utf-8"))

    assert "Vietnamese Writing Skills" in layout
    assert "Writing Skills & Humanizer" not in layout
    assert "Vietnamese Humanizer & Linter" not in layout
    assert "v0.4.0" not in layout
    assert "v0.3.0" not in layout

    assert "version" not in package
    assert "version" not in package_lock["packages"][""]


def test_frontend_retains_vercel_analytics_without_custom_properties() -> None:
    layout = (FRONTEND / "app" / "layout.tsx").read_text(encoding="utf-8")
    package = json.loads((FRONTEND / "package.json").read_text(encoding="utf-8"))

    assert package["dependencies"]["@vercel/analytics"]
    assert 'import { Analytics } from "@vercel/analytics/react";' in layout
    assert "<Analytics />" in layout
    assert "track(" not in layout
    assert "event(" not in layout
