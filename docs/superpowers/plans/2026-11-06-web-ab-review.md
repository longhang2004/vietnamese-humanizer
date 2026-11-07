# Web A/B Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the approved blind review pilot with durable database votes and private query/export.

**Architecture:** FastAPI/SQLAlchemy own a frozen study, cases, presentation assignments and votes. A capability-gated Next.js page consumes opaque assignments; a private CLI exports rows and summaries. Seed six genuine recorded pairs as an explicitly public pilot, without provider calls or fabricated ratings.

**Tech Stack:** Existing Python/FastAPI/SQLAlchemy/Pydantic, React/Next.js, native controls and CSS modules. No new dependency.

**Spec:** [Approved design](../../plans/2026-11-06-web-ab-review-design.md), approved by user on 2026-11-06.

## Global Constraints

- Work in the requested repository on dedicated branch `codex/roadmap-ab-review`; tracked state is clean at `e521dc0`. Preserve the unrelated untracked interview guide. All terminal work uses Ubuntu WSL Bash; git uses `-c core.fileMode=false`.
- Keep the four existing skills, real comparison records and generated downloads unchanged. Preserve meaning, provenance, capability gates and current styling.
- `AB_REVIEW_ENABLED` defaults false; public health adds `ab_review`. No public export, condition mapping, model identity or vote-level report endpoints.
- No automatic model calls and no synthetic production votes. Pilot source model version is unknown as recorded; preserve that fact.
- Public feedback provenance is `anonymous_web`, distinct from verified independent review. Store votes and immutable case snapshots long term as approved.

## Review Focus

- Network retry after a committed vote returns the same receipt, not a second row; conflicting resubmission is rejected.
- Browser storage unavailable or corrupt leaves a usable in-memory session; stale requests cannot replace a newer case.
- Closed study, disabled capability and another session's assignment cannot accept a new vote.
- A/B display order never becomes an inference from variant/model fields in public payloads; export preserves actual order and normalized outcome.
- Assignment refresh and simultaneous requests preserve one case/order per session; skip stays outside the preference denominator.

## Interfaces shared by backend and frontend

`POST /api/ab-review/assignments`, body `{session_id?: UUID}`. Response:

```json
{"session_id":"uuid","study":{"id":"public-pilot-2026-11-04","version":1,"title":"...","disclosure":"..."},"assignment":{"id":"uuid","case_id":"...","topic":"...","profile":"...","instruction":"...","input_text":"...","a":"verbatim output","b":"verbatim output"},"completed":0,"skipped":0,"total":6}
```

`assignment` is null when all cases are completed. If a session has an unfinished assignment, return that same assignment. Client persists one UUID session locally (with in-memory fallback); server generates one if omitted. Session IDs are anonymous browser grouping, not authenticated identities.

`POST /api/ab-review/votes`, body `{session_id, assignment_id, choice, reasons}`. `choice` is `a|b|tie|skip`; reasons are unique values from `readability|register|meaning|restraint`, optional, at most four. Skip has empty reasons. Response `{id, message, completed, skipped, total}`; idempotent identical retries return the original response. Reject unknown fields, invalid values and conflicting duplicate votes. Gate with existing capability route mechanism and rate limiter. `completed` counts all ballots including skips; `skipped` is stored skips for this session/study, so submitted comparisons equal `completed - skipped` on resume.

Seed file `web/backend/app/data/ab_review_pilot.json` contains `{study:{id,version,title,disclosure,provenance,source},cases:[{id,topic,profile,instruction,input_text,baseline,with_skills,metadata}]}`. Root creates it from unchanged `web/frontend/content/comparisons.json`; every output stays verbatim. Metadata includes source hashes, source skill commit and recorded generator/model limitation.

## Task 1: Persistence, API and private export

**Owner:** Backend implementer. Files confined to `web/backend`, except the root-owned seed JSON. Read spec and this complete contract first.

- [x] Add a failing API test: enabling the new capability allows an assignment and a vote, and querying SQLite shows exactly one normalized persisted ballot with preserved outputs/order.
- [x] Implement `ABStudy`, `ABCase`, `ABAssignment`, `ABVote` with unique/FK constraints in existing model conventions; add `app/services/ab_reviews.py`, schemas and router. Seed lazily/idempotently using the request session so tests can override the DB. Reject content drift for an existing study version, handle concurrent seed/assignment/vote inserts through DB constraints, and close sessions normally.
- [x] Add `AB_REVIEW_ENABLED`, capability guard/health field, router registration and additive `create_all` startup coverage when reviews alone are enabled. Update isolated test defaults and existing expected health payloads appropriately. Default-off must never instantiate a DB session through review routes.
- [x] Exercise both A/B orders, resume, identical and conflicting retries, completion, skip denominator, invalid/mismatched ownership, extra fields, disabled/closed studies and real SQLite persistence. Verify a red test before implementation and all backend tests after.
- [x] Add a private CLI (`python -m app.ab_review_cli`) for CSV/JSONL export, summary, study closing and optional explicit seeding. Use backend `DATABASE_URL`; do not create a public admin surface or enable existing admin API. Export metadata, order, choice, normalized winner, reasons and provenance. Include query examples and deployment flag in backend docs/env example.
- [x] Run backend Ruff/pytest. Return validation evidence and changed paths; root owns commits.

## Task 2: Review surface and capability-aware entry

**Owner:** Frontend implementer. Files confined to `web/frontend`, except existing comparison content/downloads (read only).

- [x] Read repo Impeccable, PRODUCT/DESIGN and the new review surface brief. Read installed Next.js docs before editing. Layout/interaction is pinned by the approved design; reuse the current identity and components.
- [x] Write failing UI tests for the request/ballot contract, retained selection on error and successful retry, completion, local-storage failure, closed/unavailable capability and stale requests.
- [x] Add `components/ABReview.tsx`, its CSS module, `app/review/page.tsx` and metadata, API types/helpers, optional `ab_review` health field with false fallback. Keep old health fixtures compatible.
- [x] Render source and brief, equal neutral A/B outputs, native radio A/B/tie/skip, optional reason checkboxes, explicit submit, persisted-only success and next-case action. Disable double submission and preserve choices on failure; no provider/model/condition label is shown. Use semantic status/alert and keyboard-friendly controls.
- [x] Add a capability-aware entry from the examples page and optionally footer; avoid widening the global header navigation or changing its breakpoints. Disabled/unavailable routes show clear recovery and never send votes. Preserve raw comparisons.
- [x] Run scoped tests/ESLint/TypeScript; root formats and runs whole frontend checks/build once combined.

## Task 3: Integration, review and deployment

**Owner:** Root.

- [x] Generate genuine pilot snapshot plus provenance/hash checks; review Task 1 and Task 2 against spec/contracts and resolve material issues.
- [x] Run full frontend format/lint/tests/build, backend tests/Ruff, relevant root contracts and the real comparison/download drift checks. The earlier GitHub Actions billing lock is resolved: `CI` and `Web CI` both run successfully on `4bc3a227` for `main`.
- [x] Run an isolated local SQLite API/frontend and inspect desktop/mobile, a real local vote and retry/resume/completion. Verify rows and CLI exports. Never send fake ratings to production. Capture valid screenshots and obtain the shipped fresh finish review; document the extension and resolve required findings.
- [x] Update roadmap/design status to implemented once true, document query/export commands and study limits, commit/push the complete feature. Enable the approved capability in the production backend, verify deployments, health/assignment behavior without casting a production vote, and hand over the working review URL plus SQL/export instructions.

## Execution rulings

- User approved design and explicitly requested implementation; proceed continuously without a second execution-method approval.
- Use the existing dedicated feature branch in the requested workspace. Tracked user work is absent and the unrelated guide is excluded; preserve the installed local dependencies and verify file ownership between implementers.
- Static study snapshots and four tables are sufficient for two conditions; no experiment platform, accounts, realtime generation or public dashboard is added.
