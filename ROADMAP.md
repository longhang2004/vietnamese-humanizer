[Tiếng Việt](ROADMAP.vi.md) | **English**

# Roadmap

Updated: 2026-11-06. The latest tagged product release is **0.6.0**. Work deployed from `main` is listed separately; a deployment does not create a new release.

## Available today

- Release 0.6.0 contains four writing skills, 44 linter patterns, 103 corpus examples and 124 benchmark cases. The six writing profiles are clear prose, work communication, technical documentation, administrative writing, social posts and marketing, alongside the default preservation mode. Channel, register, pronouns and editing depth remain independent choices.
- The rule-based checker, optional AI rewrite with context/style controls, `/start` onboarding and generated Claude/Gemini downloads, chatbot prompts and combined guide are implemented. The ChatGPT plugin package is prepared; public listing, account-level imports and nontechnical-user trials remain outstanding. See the [distribution guide](docs/user-distribution.md).
- Current `main` and the deployed web include the dark project landing, `/check` workspace, examples, guide/about pages, capability-aware contributions and six genuine paired AI demonstrations. Repo-local Impeccable 4.8.0, formatting and UI checks support further frontend work. These changes are described under Unreleased in the [changelog](CHANGELOG.md).
- The blind A/B review pilot is implemented in the current source: a capability-gated `/review` page, six frozen public cases, opaque assignments with a persisted A/B order, durable votes with retry-safe receipts, and private CLI summary/CSV/JSONL export. It is `AB_REVIEW_ENABLED=false` by default in source; the deployed environment enables it explicitly. Votes are anonymous web feedback with session keys, not verified reviewer identities.
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
