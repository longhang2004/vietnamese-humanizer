[Tiếng Việt](ROADMAP.vi.md) | **English**

# Roadmap

Updated: 2026-11-27. The latest tagged product release is **0.8.0**. Further work on `main` is listed under `[Unreleased]` in the [changelog](CHANGELOG.md); a web deployment does not create a new release.

## Available today

- Release 0.8.0 includes four Vietnamese writing skills, 49 linter patterns, 103 corpus examples, and **161 benchmark cases** (expanding the 0.7.0 benchmark set with 10 spoken/banter/satire cases alongside the 12 voice-sample and linguistic cases). The six writing profiles are clear prose, work communication, technical documentation, administrative writing, social posts, and marketing, alongside the default preservation mode. Channel, register, pronouns, editing depth, and optional `voice_sample` remain independent choices.
- The rule-based checker, two-phase optional AI rewrite with multi-skill selection (`humanizer-vi`, `translationese-cleaner-vi`, `grammar-checker-vi`, `style-guide-vi`), selective context loading, token-preservation audit, `voice_sample` anchoring, inline word-level diff, and apply-to-editor loop on `/check`, plus `/start` onboarding with scenario presets and compact downloadable Claude/Gemini packs, are implemented. The benchmark CLI also supports exporting stripped blind evaluation packets (`--prepare-packet`).
- The web application uses the dual-ground archival editorial specimen cabinet UI (`/` asymmetric 12-column opening stage, `/check` workspace, examples, guide/about pages, capability-aware contributions, six genuine paired AI demonstrations, and the capability-gated `/review` blind A/B review pilot with `AB_REVIEW_ENABLED=false` by default in source; enabled explicitly in deployed environments). Votes remain anonymous web feedback with session keys, not verified reviewer identities.
- Corpus review is agent-based. There is no independently human-reviewed quality baseline. The six published AI pairs illustrate behavior; they are not a quality score.

## Next

- Run independent native-speaker evaluation across the six existing profiles using the [review protocol](benchmarks/profile-review.md). Keep anonymous web feedback distinct from a study with independently identified reviewers, and retain disagreements and ties. The blind A/B review pilot is the anonymous collection path; it still needs cases withheld from publication before it can support a real preference claim.
- Run the [same-topic learning loop](docs/style-learning-loop.md) on held-out topics. Keep the four-variant [agent pilot](docs/research/2026-11-03-same-topic-pilot.md) separate from benchmark results; use observed failures to improve the existing profile guidance.
- Keep expanding `no_change` cases for rules that still over-trigger, together with true positives for the same rules.
- Calibrate thresholds on licensed, verified corpus data.
- Complete live account import checks, trials with 5–10 nontechnical users and the remaining plugin-submission work described in the distribution guide.

## Later

- Support custom project style guide configuration via the CLI.
- Add domain glossaries and independently reviewed multi-paragraph fixtures.
- Add multi-model and human-annotator baseline benchmarks.
- Report precision by pattern, domain and register once reviewed data supports those estimates.
- Evaluate opt-in cheerful/humorous tones, spontaneous speech, bilingual text and subtitles. Existing chat and spoken-script guidance remains experimental; administrative, social and marketing profiles already exist.

## 1.0

- Stabilize data schemas and versioning policy.
- Publish inter-annotator evaluated benchmarks.
- Provide integration docs for diverse agent clients.

*The roadmap explicitly excludes features designed for evading AI detectors.*
