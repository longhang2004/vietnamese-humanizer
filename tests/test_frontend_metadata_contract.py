"""Frontend metadata must use the canonical product identity."""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "web" / "frontend"
PRODUCT_NAME = "Vietnamese Writing Skills"
PRODUCT_TITLE = "Vietnamese Writing Skills - Rà soát & Gọt giũa Văn phong Tiếng Việt"
PRODUCT_METADATA_TITLE = (
    "Vietnamese Writing Skills - Công cụ Rà soát & Gọt giũa Văn phong Tiếng Việt"
)


def read_root_project() -> dict[str, object]:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]


def test_frontend_uses_canonical_branding_without_a_runtime_version() -> None:
    layout = (FRONTEND / "app" / "layout.tsx").read_text(encoding="utf-8")
    package = json.loads((FRONTEND / "package.json").read_text(encoding="utf-8"))
    package_lock = json.loads((FRONTEND / "package-lock.json").read_text(encoding="utf-8"))
    root_project = read_root_project()

    assert root_project["name"] == "vietnamese-writing-skills"
    assert root_project["version"] == "0.4.4"

    assert f'default: "{PRODUCT_TITLE}"' in layout
    assert f'template: "%s | {PRODUCT_NAME}"' in layout
    assert layout.count(f'title: "{PRODUCT_METADATA_TITLE}"') == 2
    assert f'siteName: "{PRODUCT_NAME}"' in layout
    assert f'name: "{PRODUCT_NAME}"' in layout
    assert re.search(rf">\s*{re.escape(PRODUCT_NAME)}\s*</span>", layout)
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
