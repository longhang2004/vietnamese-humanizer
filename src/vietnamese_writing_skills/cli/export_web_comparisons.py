"""Publish recorded AI outputs verbatim; never generate or edit the examples."""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNS = ROOT / "docs/research/2026-11-04-web-comparisons"
OUTPUT = ROOT / "web/frontend/content/comparisons.json"


def render() -> str:
    briefs = json.loads((RUNS / "briefs.json").read_text(encoding="utf-8"))
    baseline = json.loads((RUNS / "baseline.json").read_text(encoding="utf-8"))
    guided = json.loads((RUNS / "with-skills.json").read_text(encoding="utf-8"))
    ids = [case["id"] for case in briefs["cases"]]
    outputs = []
    for run in (baseline, guided):
        rows = run["cases"]
        if [row["id"] for row in rows] != ids or len(set(ids)) != len(ids):
            raise ValueError("All recorded cases must appear exactly once, in brief order")
        if not all(isinstance(row["output"], str) and row["output"].strip() for row in rows):
            raise ValueError("Every case needs its recorded output")
        outputs.append({row["id"]: row["output"] for row in rows})
    references = guided["references_read"]
    for name in references:
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT / "skills/humanizer-vi"):
            raise ValueError("Only humanizer references belong in source metadata")
    sources = [RUNS / name for name in ("briefs.json", "baseline.json", "with-skills.json")]
    sources += [ROOT / name for name in references]
    data = {
        "generatedOn": briefs["created_on"],
        "generator": "Codex subagents",
        "modelVersion": "Exact provider version is not exposed by the subagent tool",
        "skillCommit": guided["skill_commit"],
        "method": (
            "Two separate agent contexts, identical requests and drafts; "
            "all six pairs published verbatim. Shared host instructions apply to both "
            "conditions. No fixed sampling seed or independent human evaluation."
        ),
        "sourceDirectory": "docs/research/2026-11-04-web-comparisons",
        "sourceHashes": {
            path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sources
        },
        "cases": [
            {**case, "without": outputs[0][case["id"]], "with": outputs[1][case["id"]]}
            for case in briefs["cases"]
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            print("Recorded web examples are out of sync")
            return 1
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(expected, encoding="utf-8")
    print("Web examples: all six recorded pairs are unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
