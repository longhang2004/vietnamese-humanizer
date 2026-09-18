[Tiếng Việt](ROADMAP.vi.md) | **English**

# Roadmap

Shipped through 0.4.x: four skills, a deterministic linter, web API/frontend, and a reviewed example corpus. The next cut should reduce remaining false positives and get native-speaker review before adding more patterns.

## Next

- Add native-speaker evaluations across regions and domains; log disagreement instead of forcing a single answer.
- Keep expanding `no_change` cases for rules that still over-trigger, together with true positives for the same rules.
- Add domain glossaries and longer multi-paragraph fixtures.
- Calibrate thresholds on licensed, verified corpus data.

## Later

- Support custom project style guide configuration via the CLI.
- Add multi-model and human-annotator baseline benchmarks.
- Report precision by pattern, domain, and register.
- Research bilingual text and subtitles.

## 1.0

- Stabilize data schemas and versioning policy.
- Publish inter-annotator evaluated benchmarks.
- Provide integration docs for diverse agent clients.

*The roadmap explicitly excludes features designed for evading AI detectors.*
