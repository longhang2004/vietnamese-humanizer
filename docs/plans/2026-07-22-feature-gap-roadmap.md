# Vietnamese Writing Skills — Feature-Gap Roadmap

Date: 2026-07-22
Baseline: `main` at `70eea2c` / `v0.4.1`

## Decisions

- Canonical repository: `vietnamese-humanizer`.
- Canonical product: `Vietnamese Writing Skills`.
- Distribution/import/CLI remain `vietnamese-writing-skills`,
  `vietnamese_writing_skills`, and `viet-writing-*`.
- `pyproject.toml:[project].version` is the product version authority.
- Use a native task runner for local development; do not add Docker in Wave 1.
- Contributions remain available but are disabled by default outside explicitly
  configured environments.
- Rewrite and admin capabilities are disabled by default and fail closed.
- Keep Vercel Analytics during Wave 1. Do not add custom events, user identifiers,
  or text-derived properties.
- Stop after Wave 1 for review. Do not begin Waves 2–4 automatically.

## Delivery waves

### Wave 1 — Foundation and containment

Version/deployment parity, fail-closed capabilities, capability-aware UI, a
one-command native demo, web integration CI, canonical branding, and minimum
community/maintainer documentation. No schema migration, Docker, API v1, or
semantic rewrite verification.

### Wave 2 — Configurability

Add `.viet-writing.yml`, inheritance and precedence, rule/severity overrides,
allowlists, excludes, custom pattern files, and a domain glossary. Public APIs
must not accept arbitrary filesystem paths or regexes.

### Wave 3 — Privacy and measurable quality

Additive privacy migration, retention and deletion receipts, PII/publication
gates, run/output/review artifacts, independent reviewers, adjudication, and a
provenance-aware static quality report. Reassess Vercel Analytics before Wave 3
ends.

### Wave 4 — Reliable rewrite and ecosystem

Introduce `/api/v1`, typed error envelopes, provider deadlines and bounded
retries, protected spans and preservation diagnostics, `vi_mixed_safe`, and a
published pre-commit integration. Defer SDKs until the API survives one stable
release.

## Decision gates

- Before Wave 3: approve retention windows, quarantine/redaction behavior,
  deletion-token hashing, and the analytics/privacy decision.
- Before Wave 4: approve the legacy API window, operational logging fields, and
  benchmark/failure taxonomy prerequisites.
