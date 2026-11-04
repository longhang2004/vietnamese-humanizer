[Tiếng Việt](ROADMAP.vi.md) | **English**

# Roadmap

Shipped through 0.5.0: four skills, a deterministic linter, web API/frontend, naturalness and conversational guidance, rewrite context/style controls, and 70 benchmark cases including 30 long cases in matched pairs. Corpus review is agent-based; the next cut should obtain independent native-speaker evaluation and reduce remaining false positives before adding more patterns.

## Next

- Unreleased: `/start` onboarding and generated user downloads. Complete live platform import checks, nontechnical-user trials, and the ChatGPT plugin submission described in the [distribution guide](docs/user-distribution.md).
- Unreleased implementation: separate clear-prose, work-communication, and technical profiles, plus 24 paired cases and a profile/system report. Validate these with the [native-speaker protocol](benchmarks/profile-review.md) before claiming quality gains.
- Add native-speaker evaluations across regions and domains; log disagreement instead of forcing a single answer.
- Run the [same-topic learning loop](docs/style-learning-loop.md) on held-out topics. A four-variant [agent pilot](docs/research/2026-11-03-same-topic-pilot.md) is recorded separately from the benchmark; research marketing/social, dialogue, spoken scripts, and opt-in light humor next.
- Keep expanding `no_change` cases for rules that still over-trigger, together with true positives for the same rules.
- Add domain glossaries and independently reviewed multi-paragraph fixtures.
- Calibrate thresholds on licensed, verified corpus data.

## Later

- Expand administrative writing and opt-in cheerful/humorous tones after reviewing the first three profiles.
- Support custom project style guide configuration via the CLI.
- Add multi-model and human-annotator baseline benchmarks.
- Report precision by pattern, domain, and register.
- Research bilingual text and subtitles.

## 1.0

- Stabilize data schemas and versioning policy.
- Publish inter-annotator evaluated benchmarks.
- Provide integration docs for diverse agent clients.

*The roadmap explicitly excludes features designed for evading AI detectors.*
