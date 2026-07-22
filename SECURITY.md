[Tiếng Việt](SECURITY.vi.md) | **English**

# Security Policy

## Supported versions

Security fixes target the latest release and `main`. Older releases may not receive backports. Check `pyproject.toml` and `CHANGELOG.md` for the current project version instead of relying on version examples in historical planning documents.

## Report a vulnerability privately

If GitHub presents the repository's [private report form](https://github.com/longhang2004/vietnamese-humanizer/security/advisories/new), use it for a suspected vulnerability. This link does not assert that a particular repository setting is enabled. If the form is unavailable, open a [minimal issue](https://github.com/longhang2004/vietnamese-humanizer/issues/new/choose) asking `@longhang2004` for a private follow-up; do not include exploit details or sensitive data in the public issue.

Include the affected version or commit, a minimal reproducible case, the expected impact, and any suggested mitigation. Remove credentials, personal information, and proprietary material from the report.

This project processes writing samples. Do not submit sensitive user text, confidential documents, or production data. Use a minimal synthetic example that preserves the relevant behavior instead.

False-positive reports, linguistic-quality feedback, and questions about expected editing behavior are not security vulnerabilities. Remove sensitive data, then use the repository's issue templates.

## Web data boundaries

- Deterministic lint requests send document text to the configured backend so it can return findings. Project code does not store lint input as a contribution.
- Rewrite is disabled by default. When an operator enables it and provides `GEMINI_API_KEY`, rewrite text is sent to the configured Gemini integration. Review the provider's current terms before enabling it; this project does not state provider retention or training behavior.
- Contributions are disabled by default. When enabled, a submitted contribution is stored in the configured database for maintainer review. It does not automatically become corpus or training data; adding it to `examples/` or `benchmarks/` requires the normal manual pull-request and review process.
- Vercel Analytics remains installed and rendered in the Wave 1 frontend. Project code sends no custom analytics events, user IDs, document/lint/rewrite/contribution text, or text-derived properties. This statement is limited to project code and makes no claim about provider retention, hosting logs, encryption, APM, or deployment configuration.
