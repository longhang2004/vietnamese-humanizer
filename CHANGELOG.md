[Tiếng Việt](CHANGELOG.vi.md) | **English**

# Changelog

Follows Keep a Changelog structure. Semantic Versioning is not yet guaranteed before v1.0.

## [Unreleased]

## [0.4.0] - 2026-07-22

### Added

- Redesigned the entire Web UI (Next.js Frontend) following Anti-Slop (`taste-skill`) and Design System (`ui-ux-pro-max-skill`) principles.
- Integrated modern Google Fonts: `Plus Jakarta Sans` (sans-serif) and `JetBrains Mono` (monospace).
- Added real-time character/word counter, quick text clear button, and sample text loader.
- Interactive Skill Selector Cards and visual finding list with severity badges, monospace tags, and rewrite suggestions.
- Pattern detail modal with backdrop blur (`backdrop-blur-sm`).
- Standardized all UI microcopy according to `vietnamese-writing-skills` guidelines for clear, natural Vietnamese.

### Fixed

- Explicitly pass repository context to GitHub Release workflow steps when checkout is disabled.

### Changed

- Refactored public documentation for direct and natural phrasing.

## [0.3.1] - 2026-07-22

### Added

- Integrated Vercel Analytics (`@vercel/analytics`) for web app visitor tracking.
- Updated PyPI release workflow with `skip-existing: true` to prevent HTTP 400 errors when files exist on PyPI.

## [0.3.0] - 2026-07-22

### Added

- Web Application "Vietnamese Writing Skills" (`web/`): includes FastAPI Backend and Next.js Frontend.
- Integrated Gemini AI (`gemini-2.5-flash`) for experimental natural rewrites and fact preservation.
- Staging database (PostgreSQL / Neon) to record community contribution cases.
- Comprehensive SEO optimization: OpenGraph banner, Twitter card, Favicon, JSON-LD Schema, and Canonical metadata.
- Contributor acknowledgment: **Lê Ngọc Phương Thư** (`lengocphuongthuct2006@gmail.com`) — Ideated and proposed the Web App version.

## [0.2.0] - 2026-07-21

### Added

- JSON Schema and validator for 100 agent-audited preservation examples, including output mode, gold rewrite/classification, and review provenance.
- Finding taxonomy, scope, and aggregation for all 40 patterns.
- Pattern example modes and generated docs displaying the mode of each good example.
- Expected output mode, manual review schema, blocker rate, multi-reviewer summary, and unreviewed count for benchmarks.
- `vietnamese_writing_skills` package, six console commands, and wheel resources.
- Bilingual English–Vietnamese documentation for README and contribution guides.
- VietQR donation support section in both READMEs.
- Tag-triggered release workflow with shared artifacts, GitHub Release, and PyPI Trusted Publishing via OIDC.
- Vulnerability reporting policy and Dependabot configuration for Python and GitHub Actions.
- Python 3.11–3.14 CI matrix, Twine artifact checking, and smoke tests for all six console commands.

### Changed

- Completed semantic preservation audit; removed hidden context and avoided unverified subject, scope, or year assumptions.
- Linter outputs error, warning, preference, and heuristic with confidence, scope, and summary by type.
- `scripts/` converted to legacy wrappers; importable logic moved to `src/`.
- README updated with canonical repository URL explaining repository, product, distribution, and import names.
- Generated docs display full taxonomy, strategy, exceptions, and false-positive risk.
- Added package metadata, project URLs, and Python 3.11–3.14 classifiers.
- Moved unfinished 0.2 roadmap items to 0.2.x / Post-0.2 series.

## [0.1.0] - 2026-07-20

Initial MVP ready for public review.
