# Vietnamese Writing Skills backend API

This FastAPI service exposes deterministic lint and metadata endpoints. Rewrite, contribution staging, and contribution administration are separate, fail-closed capabilities.

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

Writing profile options: `preserve` (default), `plain` (clear prose), `business` (work communication), `technical` (technical documentation). Profile guidance is loaded for any selected skill without widening that skill's task. The profile does not override channel, register, pronouns, or edit depth; `technical` with `friendly` remains valid. A business profile cannot invent missing owners or deadlines. Omitted profiles keep the existing behavior. See the [profile guide](../../skills/humanizer-vi/references/writing-profiles.md).

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

Copy `.env.example` to `.env` for manual backend runs. All three optional feature flags default to `false`.

| Capability | Required variables | Notes |
| --- | --- | --- |
| Lint and metadata | Optional `FRONTEND_ORIGIN` | Always available. The request limit is fixed at 20,000 characters; configurability is deferred. `TRUSTED_PROXY_HOSTS` defaults to loopback and accepts IP or CIDR; private peers are not trusted unless listed or `TRUST_PRIVATE_PROXIES=true`. The client IP is the first untrusted hop walking `X-Forwarded-For` right-to-left. |
| Rewrite | `REWRITE_ENABLED=true` and non-empty `GEMINI_API_KEY` | Text is sent to the configured Gemini integration; the generated result is marked unreviewed. |
| Contributions | `CONTRIBUTIONS_ENABLED=true` | Stores submissions for review only. A submission does not automatically become corpus or training data. |
| Admin | `ADMIN_API_ENABLED=true` and `ADMIN_API_KEY` | The key must be non-placeholder and at least 32 characters. Clients send it as `X-Admin-Key`. |

Disabled capability routes return `503`. Invalid enabled rewrite/admin key configuration fails backend startup. `DATABASE_URL` is not required by startup validation: when omitted, the effective default is local SQLite at `sqlite:///./dev.db`. Deployments should set `DATABASE_URL` to durable, managed database storage rather than rely on the local SQLite file. Admin export returns approved staged records but never writes `examples/` or `benchmarks/`.

The checked-in Render blueprint explicitly enables contributions and admin but does not set `REWRITE_ENABLED=true`. A provider key by itself therefore does not enable rewrite. The blueprint documents intended project configuration; it does not verify live deployment settings.

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
