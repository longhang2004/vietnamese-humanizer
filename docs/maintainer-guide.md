# Maintainer guide

This guide covers the commands and safety boundaries implemented in the repository. Run commands from the repository root unless a section says otherwise.

## Local development

Install Python 3.11+, Node.js 20+, and npm. The primary quickstart is:

```bash
python3 scripts/dev.py demo
```

`demo` runs the prerequisite check and the idempotent setup before starting the backend on port 8000 and the frontend on port 3000. It creates or repairs `.venv`, installs root and backend development dependencies, and runs `npm ci`. It forces rewrite, contributions, and admin off so the deterministic linter can be exercised without provider credentials or a database. Press Ctrl-C to stop both child processes.

Useful individual commands are:

```bash
python3 scripts/dev.py doctor
python3 scripts/dev.py setup
python3 scripts/dev.py smoke
python3 scripts/dev.py check
```

Use `--skip-setup` with `demo` or `smoke` only after dependencies are installed and current.

## Capabilities and environment variables

All optional backend capabilities fail closed. Configure them in `web/backend/.env` when running the backend manually; `scripts/dev.py demo` and `smoke` override the three feature flags to `false`.

| Capability | Default | Required configuration | Data boundary |
| --- | --- | --- | --- |
| Deterministic lint and metadata | On | `LINT_MAX_CHARS` optionally changes the 20,000-character request limit. `FRONTEND_ORIGIN` sets the allowed frontend origin. | The backend processes request text and returns findings. Project code does not turn lint input into a contribution. |
| Rewrite | Off | Set `REWRITE_ENABLED=true` and provide a non-empty `GEMINI_API_KEY`. | Rewrite text is sent to the configured Gemini integration. The response remains unreviewed. Do not enable this for sensitive text without evaluating the provider's current terms. |
| Contributions | Off | Set `CONTRIBUTIONS_ENABLED=true`. | Submissions are stored for maintainer review. They do not automatically become corpus or training data. Adding material to `examples/` or `benchmarks/` requires a manual pull request and review. |
| Admin review | Off | Set `ADMIN_API_ENABLED=true` and use a non-placeholder `ADMIN_API_KEY` of at least 32 characters. Send it in `X-Admin-Key`. | Admin routes list, update, and export staged contributions. Export does not write repository corpus files. |
| Frontend API target | Local example | Set `NEXT_PUBLIC_API_BASE_URL` in `web/frontend/.env.local`. | The browser sends API requests to this backend URL. |
| Frontend canonical URL | Deployment default | `NEXT_PUBLIC_SITE_URL` optionally changes the metadata base URL. | This affects generated page metadata, not backend capability gates. |

Startup validation does not require an explicit `DATABASE_URL`. If it is omitted, the effective setting is local SQLite at `sqlite:///./dev.db`. That default supports local development; a deployment should set `DATABASE_URL` to durable, managed database storage. `web/backend/render.yaml` does so by obtaining the URL from its declared database. The blueprint also explicitly enables contributions and admin but does not enable rewrite, so a configured `GEMINI_API_KEY` alone does not expose that route. Treat the checked-in blueprint as project configuration, not proof of the state or security properties of any live deployment.

## Analytics and sensitive text

Wave 1 retains the `@vercel/analytics` dependency and renders `<Analytics />`. Project code defines no custom analytics events and sends no user IDs, document/lint/rewrite/contribution text, or text-derived properties through custom events. Do not extend analytics with these values. No claim here covers provider retention, platform logs, encryption, APM, or a live deployment's settings.

Use synthetic text in bug reports, tests, conduct reports, and vulnerability reports. Remove credentials, personal information, confidential documents, and production data.

## Reviewing contributions

An enabled contribution begins with `pending` status in the configured database. Approval only changes its review status and makes it available to the authenticated export endpoint. It is still source material, not a validated corpus entry.

Before creating a corpus pull request:

1. Verify the contributor had the right to share the material and remove personal or confidential data.
2. Supply enough `context` to verify the edit.
3. Define `must_preserve`, `must_not_add`, output mode, pattern IDs, and honest review provenance.
4. Follow `CONTRIBUTING.md` and `docs/pattern-authoring-guide.md`.
5. Run the full repository check before requesting review.

## Quality and release workflow

Run the complete local quality gate:

```bash
python3 scripts/dev.py check
python3 scripts/dev.py smoke --skip-setup
git diff --check
```

`check` runs root Ruff and pytest, release consistency, all data validators, benchmark validation, generated-document verification, package build and isolated wheel checks, backend Ruff and pytest, frontend lint and TypeScript, and the frontend production build.

For a release, also follow the checklist in `CONTRIBUTING.md`: confirm CI, verify the version authorities and changelog, inspect the built distributions, and use the repository release workflow. Do not claim a GitHub environment, trusted publisher, branch rule, analytics setting, or deployment state without checking it in the system that owns that state.

## Security and community reports

Follow `SECURITY.md` for vulnerability reports and `CODE_OF_CONDUCT.md` for conduct reports. The project does not currently publish a dedicated private conduct inbox. For abuse on GitHub, use GitHub's official Report Abuse form; to request project follow-up, ask `@longhang2004` for a private way to continue using a minimal public issue without sensitive details.
