"""The public showcase must preserve the actual recorded generations."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_web_showcase_matches_every_recorded_generation() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/export_web_comparisons.py"), "--check"],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    public = json.loads((ROOT / "web/frontend/content/comparisons.json").read_text())
    for condition, field in (("baseline", "without"), ("with-skills", "with")):
        recorded = json.loads(
            (ROOT / f"docs/research/2026-11-04-web-comparisons/{condition}.json").read_text()
        )
        assert [(case["id"], case[field]) for case in public["cases"]] == [
            (case["id"], case["output"]) for case in recorded["cases"]
        ]
