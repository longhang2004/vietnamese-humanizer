# Vietnamese Writing Skills backend API

This FastAPI service exposes deterministic lint and metadata endpoints. Rewrite, contribution staging, A/B review, and contribution administration are separate, fail-closed capabilities.

## Rewrite context and output modes

`POST /api/rewrite` retains `text`, `skill`, and `issue_ids`, and accepts optional `context` (up to 5,000 characters) and `style`:

```json
{
  "text": "Nhờ anh gửi bản nháp trước 15:00.",
  "skill": "humanizer-vi",
  "context": "Email nhắc công việc trong nhóm.",
  "style": {
    "profile": "business",
    "channel": "email",
    "register": "professional",
    "audience": "đồng nghiệp",
    "relationship": "đã thống nhất xưng tôi–anh",
    "pronouns": "tôi–anh",
    "edit_level": "light",
    "reduce_hype": false
  }
}
```

Channel options: `auto`, `document`, `email`, `chat`, `spoken_script`. Register options: `preserve`, `formal`, `professional`, `friendly`, `conversational`. Editing depth: `light`, `moderate`, `deep`. Defaults are `auto`, `preserve`, `light`, and no hype reduction. Audience/relationship are limited to 300 characters each; pronouns to 200. Every depth preserves facts and commitments. Hype reduction explicitly permits softening formulaic praise/empathy, not changing scope or factual claims.

Writing profile options: `preserve` (default), `plain` (clear prose), `business` (work communication), `technical` (technical documentation), `administrative` (supplied administrative prose), `social` (personal/community posts), `marketing` (commercial copy). Profile guidance is loaded for any selected skill without widening that skill's task. The profile does not override channel, register, pronouns, or edit depth; `technical` with `friendly` remains valid. A business profile cannot invent missing owners or deadlines. Omitted profiles keep the existing behavior. See the [profile guide](../../skills/humanizer-vi/references/writing-profiles.md).

Responses retain `rewrite`, `review_status`, and `disclaimer`, and add `output_mode` and `comments`. `clean_rewrite` contains replacement text; `no_change` returns the original exactly. `review_comment` and `needs_author_decision` return an empty `rewrite` and actionable `comments`. Consumers must inspect the mode before treating a result as a replacement. Invalid provider JSON or empty replacement text fails instead of masquerading as a successful unchanged result.

The prompt loads repository-owned reference filenames, with conversational guidance for chat/spoken-script channels or conversational register, the selected writing-profile reference, and the long-document workflow for deep humanizer edits. Structured output validates shape, not semantic preservation. Tests mock provider calls; independent human evaluation is still required for quality claims.

## Quickstart

The primary repository quickstart sets up and runs both backend and frontend with optional capabilities disabled:

```bash
python3 scripts/dev.py demo
```

Run that command from the repository root. For backend-only work after `python3 scripts/dev.py setup`:

```bash
cd web/backend
../../.venv/bin/python -m uvicorn app.main:app --reload --port 8000
```

The health endpoint is `http://localhost:8000/api/health`; OpenAPI is at `http://localhost:8000/docs`.

## Capability configuration

Copy `.env.example` to `.env` for manual backend runs. All four optional feature flags default to `false`.

| Capability | Required variables | Notes |
| --- | --- | --- |
| Lint and metadata | Optional `FRONTEND_ORIGIN` | Always available. The request limit is fixed at 20,000 characters; configurability is deferred. `TRUSTED_PROXY_HOSTS` defaults to loopback and accepts IP or CIDR; private peers are not trusted unless listed or `TRUST_PRIVATE_PROXIES=true`. The client IP is the first untrusted hop walking `X-Forwarded-For` right-to-left. |
| Rewrite | `REWRITE_ENABLED=true` and non-empty `GEMINI_API_KEY` | Text is sent to the configured Gemini integration; the generated result is marked unreviewed. |
| Contributions | `CONTRIBUTIONS_ENABLED=true` | Stores submissions for review only. A submission does not automatically become corpus or training data. |
| A/B review | `AB_REVIEW_ENABLED=true` | Serves a frozen six-case pilot and commits anonymous browser ballots to `DATABASE_URL`. No model/provider call or admin API is needed. |
| Admin | `ADMIN_API_ENABLED=true` and `ADMIN_API_KEY` | The key must be non-placeholder and at least 32 characters. Clients send it as `X-Admin-Key`. |

Disabled capability routes return `503`. Invalid enabled rewrite/admin key configuration fails backend startup. `DATABASE_URL` is not required by startup validation: when omitted, the effective default is local SQLite at `sqlite:///./dev.db`. Deployments should set `DATABASE_URL` to durable, managed database storage rather than rely on the local SQLite file. Admin export returns approved staged records but never writes `examples/` or `benchmarks/`.

The checked-in Render blueprint explicitly enables contributions and admin but does not set `REWRITE_ENABLED=true`. A provider key by itself therefore does not enable rewrite. The blueprint documents intended project configuration; it does not verify live deployment settings.

## Blind A/B review and private queries

Set `AB_REVIEW_ENABLED=true` and a durable managed `DATABASE_URL` in the backend deployment to expose the review pilot. Health includes `capabilities.ab_review`; it defaults to false. Startup creates the additional tables when reviews alone are enabled. The bundled `app/data/ab_review_pilot.json` is seeded on the first assignment request using that request's database session. It contains six genuine, already-public comparison pairs; this is a public pilot, not a held-out independent benchmark. Its recorded source says the exact provider model version was not exposed. No version is inferred or invented.

`POST /api/ab-review/assignments` takes `{ "session_id": "optional UUID" }` (or `{}`). It returns the session UUID, public study/disclosure, one opaque assignment with the source and verbatim A/B outputs, and `completed`, `total`, `skipped`. An unfinished assignment resumes with its persisted display order. After all six ballots, `assignment` is null. The session UUID groups a browser's activity; it is not verified reviewer identity.

`POST /api/ab-review/votes` takes `session_id`, `assignment_id`, `choice` (`a`, `b`, `tie`, `skip`) and optional `reasons` (unique `readability`, `register`, `meaning`, `restraint`). Skip must have no reasons. Responses are sent after commit. An identical retry returns the original receipt and counts, including after further progress or study closure; conflicting retries return 409. Another session's assignment is rejected. Closed studies reject new assignments and votes with 409. Disabled routes return 503 before accessing the database. The endpoints allow 30 assignment requests and 20 vote requests per minute under the existing limiter.

The four tables are `ab_studies`, `ab_cases`, `ab_assignments`, `ab_votes`. The database preserves each version's original inputs/outputs, source and skill hashes, recorded metadata, A/B mapping and normalized winner. A changed bundled snapshot with an existing study/version is rejected; create a new version for changed content. All browser votes carry `anonymous_web` provenance and must stay distinct from verified independent reviews. Public responses expose neither condition mapping nor source model metadata. There are no public review export or administrative endpoints.

Run the private CLI from `web/backend` in an environment with authorized `DATABASE_URL` access. These commands also work while the public capability is off:

```bash
# Optional: initialize tables and freeze the bundled study before public traffic.
../../.venv/bin/python -m app.ab_review_cli seed

../../.venv/bin/python -m app.ab_review_cli summary \
  --study public-pilot-2026-11-04 --version 1
../../.venv/bin/python -m app.ab_review_cli export --format jsonl \
  --study public-pilot-2026-11-04 --version 1 --output review-votes.jsonl
../../.venv/bin/python -m app.ab_review_cli export --format csv \
  --profile business --since 2026-11-06T00:00:00Z --until 2026-12-01T00:00:00Z \
  --output business-votes.csv
../../.venv/bin/python -m app.ab_review_cli summary \
  --skill-commit 845c3795f26346c4f5801e35365d65ff939a8e08
../../.venv/bin/python -m app.ab_review_cli close-study \
  --study public-pilot-2026-11-04 --version 1
```

Export/summary support `--study`, `--version`, `--topic`, `--profile`, `--model` (exact recorded `modelVersion`), `--skill-commit`, `--since` (inclusive) and `--until` (exclusive). Times use UTC; timezone-free inputs are interpreted as UTC. CSV JSON-encodes nested metadata/reasons; JSONL retains their structure. Exports include the frozen texts, source metadata/hashes, skill commit, session/assignment, A/B conditions, raw choice, normalized winner, reasons, timestamps and provenance. Keep these exports private because they reveal the hidden mapping and session grouping.

Summary reports A/B choices, normalized outcomes, ties, skipped cases, reason counts and choice counts by which condition appeared first. Its preference denominator is every non-skipped ballot, including ties; baseline, with-skills and tie rates use that same denominator. Empty denominators produce null rates. `anonymous_sessions` counts random session keys, not independently verified people. Closing preserves every snapshot and existing ballot for later analysis.

For a direct SQL check of outcomes and display position:

```sql
SELECT a.study_id, a.study_version, c.profile, a.a_condition,
       v.choice, v.winner, v.provenance, COUNT(*) AS ballots
FROM ab_votes AS v
JOIN ab_assignments AS a ON a.id = v.assignment_id
JOIN ab_cases AS c ON c.study_id = a.study_id
  AND c.study_version = a.study_version AND c.id = a.case_id
WHERE a.study_id = 'public-pilot-2026-11-04' AND a.study_version = 1
GROUP BY a.study_id, a.study_version, c.profile, a.a_condition,
         v.choice, v.winner, v.provenance;
```

## Data and analytics boundary

Project backend code does not store lint requests as contributions. Contribution storage only occurs after the user submits the contribution endpoint while that capability is enabled. Corpus inclusion remains a manual pull-request and review step.

The frontend retains and renders Vercel Analytics, but project code defines no custom events carrying user IDs, document/lint/rewrite/contribution text, or text-derived properties. This is not a claim about third-party retention, hosting logs, encryption, APM, or operational deployment behavior.

## Checks

From the repository root, the full check includes root, backend, frontend, build, and packaging validation:

```bash
python3 scripts/dev.py check
python3 scripts/dev.py smoke --skip-setup
```

For a focused backend run after setup:

```bash
cd web/backend
../../.venv/bin/python -m ruff check .
../../.venv/bin/python -m pytest
```

See [`../README.md`](../README.md) for the complete web setup and [`../../docs/maintainer-guide.md`](../../docs/maintainer-guide.md) for maintenance and release guidance.
