# Vietnamese Writing Skills — Wave 1 Implementation Plan

## Goal

Standardize version/deployment behavior, provide a one-command local experience,
and add safe defaults without breaking existing package, import, CLI, or route
identifiers.

## Global constraints

- Product version authority is `pyproject.toml:[project].version`.
- Keep repository/product/distribution/import/CLI names unchanged.
- Keep `@vercel/analytics`, its import, and `<Analytics />` in Wave 1.
- Do not add custom analytics events, user identifiers, document text, rewrite
  text, lint text, contribution text, or text-derived analytics properties.
- Contributions, rewrite, and admin default off; production contribution/admin
  enablement must be explicit.
- All existing routes stay mounted and appear in OpenAPI. A disabled capability
  returns a stable HTTP 503.
- Do not add Docker, migrations, API v1, config/glossary runtime, provider
  timeout/retry policy, or semantic/preservation verification in Wave 1.
- Preserve public package/import/CLI contracts.
- Use test-driven development and stop after Task 11 for review.

## Task 1 — W1-01 Core runtime version

**Files:** `src/vietnamese_writing_skills/__init__.py`, `tests/test_package.py`.

- Write a test proving the runtime version comes from distribution metadata and
  demonstrate that the current implementation fails it.
- Use `importlib.metadata.version("vietnamese-writing-skills")`.
- Run the focused test and the complete core test suite.
- Commit: `refactor(version): derive runtime version from package metadata`.

## Task 2 — W1-02 Release consistency checker

**Files:** create `scripts/check_release_consistency.py` and
`tests/test_release_contract.py`; modify `web/backend/pyproject.toml` and
`web/backend/requirements.txt`.

- Read the root project version and verify that backend version and core
  dependency mirrors are exact matches.
- First prove the current `>=0.2.0` and `==0.2.0` values fail the contract.
- Pin both backend dependency mirrors to the tested product version `0.4.1`.
- Remove `pytest` and `httpx` from production requirements.
- Commit: `fix(release): align backend with product version`.

## Task 3 — W1-03 API and deployment version parity

**Files:** `web/backend/app/main.py`, `web/backend/render.yaml`,
`web/backend/tests/test_lint.py`.

- FastAPI version must come from the core runtime.
- Health, lint, and OpenAPI must expose the same version.
- Render must explicitly set `CONTRIBUTIONS_ENABLED=true` and
  `ADMIN_API_ENABLED=true`; do not enable rewrite implicitly.
- Run the backend suite.
- Commit: `fix(web): align API and deployment runtime version`.

## Task 4 — W1-04 Frontend canonical branding

**Files:** `web/frontend/app/layout.tsx`, `web/frontend/package.json`,
`web/frontend/package-lock.json`; create
`tests/test_frontend_metadata_contract.py`.

- Remove hard-coded version labels and alternate branding “Writing Skills &
  Humanizer”.
- Remove the independent private npm-package version when it is not used as a
  runtime version.
- Keep `@vercel/analytics`, the import, and `<Analytics />` unchanged in
  function.
- Add no custom event or text-derived property.
- Run the root contract test plus frontend lint, typecheck, and build.
- Commit: `refactor(frontend): use canonical product metadata`.

## Task 5 — W1-05 Capabilities, health, and conditional DB initialization

**Files:** create `web/backend/app/capabilities.py` and
`web/backend/tests/test_config.py`; modify `web/backend/app/config.py`,
`web/backend/app/main.py`, `web/backend/app/routers/health.py`,
`web/backend/tests/test_lint.py`, and `web/backend/.env.example`.

- `REWRITE_ENABLED`, `CONTRIBUTIONS_ENABLED`, and `ADMIN_API_ENABLED` default to
  false. `GEMINI_API_KEY` and `ADMIN_API_KEY` default to `None`.
- Enabling rewrite requires a Gemini key.
- Enabling admin requires a non-empty, non-placeholder key of at least 32
  characters.
- Implement `validate_capability_settings`, `require_rewrite_enabled`,
  `require_contributions_enabled`, `require_admin_enabled`, and
  `public_capabilities`.
- Call `Base.metadata.create_all` only when contributions or admin are enabled.
- Health adds effective public capabilities `rewrite` and `contributions`.
- Keep every route mounted in every environment.
- Commit: `feat(web): add fail-closed capability controls`.

## Task 6 — W1-06 Rewrite containment

**Files:** `web/backend/app/routers/rewrite.py`,
`web/backend/tests/test_rewrite.py`.

- Disabled rewrite returns HTTP 503 before any provider call.
- Enabled happy path preserves the response contract.
- Provider exceptions must not expose secrets or raw fragments to clients.
- Generic failures use a neutral message.
- Timeout, retry, and preservation checks remain deferred to Wave 4.
- Commit: `fix(rewrite): fail closed when capability is disabled`.

## Task 7 — W1-07 Contribution and admin containment

**Files:** `web/backend/app/routers/contributions.py`,
`web/backend/app/routers/admin.py`,
`web/backend/tests/test_contributions.py`, `web/backend/tests/test_admin.py`.

- Disabled contribution/admin requests return HTTP 503.
- The capability dependency runs before any DB dependency.
- A disabled submission creates no row.
- The enabled submit → list → approve → export flow remains valid.
- Compare admin keys with `secrets.compare_digest`.
- Do not change the DB schema or export format.
- Commit: `fix(contributions): require explicit storage and admin enablement`.

## Task 8 — W1-08 Capability-aware frontend

**Files:** create `web/frontend/components/CapabilityNav.tsx`; modify
`web/frontend/lib/types.ts`, `web/frontend/lib/api.ts`,
`web/frontend/app/layout.tsx`, `web/frontend/app/page.tsx`, and
`web/frontend/app/contribute/page.tsx`; create
`tests/test_frontend_capabilities_contract.py`.

- Add `HealthResponse` and `fetchHealth()`.
- Show contribution navigation/form only when contributions are enabled.
- Render the rewrite panel only when rewrite is enabled.
- If health fails, fail closed for optional capabilities while lint remains
  usable.
- Keep `<Analytics />` in the root layout.
- Run root contract tests and frontend lint, typecheck, and build.
- Commit: `feat(frontend): reflect backend capabilities`.

## Task 9 — W1-09 Native demo runner

**Files:** create `scripts/dev.py`, `tests/test_dev_script.py`.

- Commands: `doctor`, `setup`, `demo [--skip-setup]`, `check`, and
  `smoke [--skip-setup]`.
- `doctor` checks Python >=3.11, Node >=20, npm, and required ports.
- `setup` creates `.venv`, installs root/backend editable, and runs `npm ci`.
- `demo` performs idempotent setup by default, starts Uvicorn and Next, polls
  readiness, and always cleans up.
- `check` runs all repository checks.
- `smoke` checks health, frontend, and synthetic lint with a 60-second timeout
  and always cleans up.
- Use subprocess argument lists with `shell=False`.
- Commit: `feat(dev): add one-command local demo runner`.

## Task 10 — W1-10 Web integration CI

**Files:** `.github/workflows/web-ci.yml`.

- Add triggers for root `pyproject.toml`, `src/**`, `patterns/**`, `skills/**`,
  `examples/**`, `benchmarks/**`, and `scripts/dev.py`.
- Run backend on Python 3.11 and 3.13.
- Run the release consistency checker.
- Add an integration job using Python 3.13 and Node 20 that runs
  `scripts/dev.py smoke --skip-setup`.
- Do not provide a model key; optional capabilities stay disabled.
- Commit: `ci: cover core-to-web integration failures`.

## Task 11 — W1-11 Documentation and community artifacts

**Files:** create `CODE_OF_CONDUCT.md`, `CODE_OF_CONDUCT.vi.md`,
`.github/CODEOWNERS`, and `docs/maintainer-guide.md`; update root/web/backend
READMEs, both SECURITY documents, `web/PLAN.md`, and `web/GEMINI_PROMPT.md`.

- Make `python3 scripts/dev.py demo` the primary quickstart.
- Document environment variables by capability.
- State that contributions do not automatically become corpus data.
- State that Vercel Analytics is retained and the project does not send
  document text through custom analytics events.
- Do not claim unverified retention or provider behavior.
- Mark versions in old web plans/prompts as historical, not runtime authority.
- Commit: `docs: document safe setup and maintainer workflow`.

## Final verification

Run core Ruff, pytest, release checker, all validators, benchmark validation,
generated-doc check, and package build; backend Ruff and pytest; frontend lint,
TypeScript, and build; `scripts/dev.py smoke --skip-setup`; and
`git diff --check`. Then obtain an independent whole-branch review from merge
base `70eea2c` and stop after Wave 1.
