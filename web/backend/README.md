# Vietnamese Writing Skills backend API

This FastAPI service exposes deterministic lint and metadata endpoints. Rewrite, contribution staging, and contribution administration are separate, fail-closed capabilities.

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
| Lint and metadata | Optional `FRONTEND_ORIGIN` and `LINT_MAX_CHARS` | Always available. The default request limit is 20,000 characters. |
| Rewrite | `REWRITE_ENABLED=true` and non-empty `GEMINI_API_KEY` | Text is sent to the configured Gemini integration; the generated result is marked unreviewed. |
| Contributions | `CONTRIBUTIONS_ENABLED=true` and `DATABASE_URL` | Stores submissions for review only. A submission does not automatically become corpus or training data. |
| Admin | `ADMIN_API_ENABLED=true`, `DATABASE_URL`, and `ADMIN_API_KEY` | The key must be non-placeholder and at least 32 characters. Clients send it as `X-Admin-Key`. |

Disabled capability routes return `503`. Invalid enabled rewrite/admin configuration fails backend startup. Admin export returns approved staged records but never writes `examples/` or `benchmarks/`.

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
