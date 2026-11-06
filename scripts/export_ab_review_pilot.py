"""Freeze the genuine public AI pairs for the database-backed review pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "web/frontend/content/comparisons.json"
TARGET = ROOT / "web/backend/app/data/ab_review_pilot.json"


def render() -> str:
    raw = SOURCE.read_bytes()
    recorded = json.loads(raw)
    provenance = {key: value for key, value in recorded.items() if key != "cases"}
    provenance["sha256"] = hashlib.sha256(raw).hexdigest()
    cases = []
    for case in recorded["cases"]:
        cases.append({
            "id": case["id"],
            "topic": case["topic"],
            "profile": case["profile"],
            "instruction": case["prompt"],
            "input_text": case["input"],
            "baseline": case["without"],
            "with_skills": case["with"],
            "metadata": {"tone": case["tone"]},
        })
    pilot = {
        "study": {
            "id": "public-pilot-2026-11-04",
            "version": 1,
            "title": "Góp đánh giá văn phong tiếng Việt",
            "disclosure": (
                "Đợt thử gồm sáu cặp AI đã công khai. "
                "Lựa chọn của bạn được lưu để cải thiện bộ skill."
            ),
            "provenance": "anonymous_web",
            "source": provenance,
        },
        "cases": cases,
    }
    return json.dumps(pilot, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        if not TARGET.is_file() or TARGET.read_text(encoding="utf-8") != expected:
            print("A/B public pilot is missing or differs from its recorded source.")
            return 1
        print("A/B public pilot: all six recorded pairs and provenance match.")
        return 0
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(expected, encoding="utf-8")
    print(f"Wrote {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
