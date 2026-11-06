"""The public pilot must preserve the genuine recorded AI outputs."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ab_review_pilot_preserves_the_recorded_pairs_and_provenance() -> None:
    path = ROOT / "web/backend/app/data/ab_review_pilot.json"
    assert path.is_file(), "The A/B pilot snapshot has not been generated."
    source_bytes = (ROOT / "web/frontend/content/comparisons.json").read_bytes()
    source = json.loads(source_bytes)
    pilot = json.loads(path.read_text(encoding="utf-8"))

    assert pilot["study"]["id"] == "public-pilot-2026-11-04"
    assert pilot["study"]["provenance"] == "anonymous_web"
    assert pilot["study"]["source"]["sha256"] == hashlib.sha256(source_bytes).hexdigest()
    assert pilot["study"]["source"]["skillCommit"] == source["skillCommit"]
    assert pilot["study"]["source"]["modelVersion"] == source["modelVersion"]
    assert len(pilot["cases"]) == len(source["cases"]) == 6
    for actual, recorded in zip(pilot["cases"], source["cases"], strict=True):
        assert actual["id"] == recorded["id"]
        assert actual["instruction"] == recorded["prompt"]
        assert actual["input_text"] == recorded["input"]
        assert actual["baseline"] == recorded["without"]
        assert actual["with_skills"] == recorded["with"]
        assert actual["profile"] == recorded["profile"]
