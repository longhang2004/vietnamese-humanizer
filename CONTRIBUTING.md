**English** | [Tiếng Việt](CONTRIBUTING.vi.md)

# Contributing

Thank you for helping Vietnamese Writing Skills reflect a wider range of Vietnamese usage.

## Before opening a pull request

1. Search for similar IDs, names, and signals in `docs/generated-patterns.md`.
2. Read `docs/pattern-authoring-guide.md`.
3. Remove personal information and verify that examples can be legally used.
4. Update the relevant data, package code, tests, and documentation.
5. Run the generators, validators, tests, and build commands listed in the README.
6. Record user-visible changes in `CHANGELOG.md`.

## New examples

Every example must include:

- complete input and context so the output can be verified;
- output that adds no facts, metrics, sources, causes, or experiences;
- consistent `output_mode`, `gold_output_mode`, and `gold_rewrite` values;
- `must_preserve` and `must_not_add` constraints;
- an existing pattern ID;
- `preservation_review` with one of these provenance states: `unreviewed`, `agent-reviewed`, `maintainer-reviewed`, or `independently-reviewed`;
- review notes when the example has been reviewed.

An `unreviewed` example must not be marked as a gold rewrite. `review_comment` and `needs_author_decision` may be gold output modes, but they are not gold rewrites. Do not claim that a detail “appears elsewhere in the article” unless that content is included in the context.

## New patterns

A pattern needs a finding type, scope, aggregation, severity, confidence, false-positive risk, two bad examples, two good examples with modes, exceptions, tests, and an example that does not introduce facts. State the observation source and discuss legitimate uses of the structure.

A pattern based on one person's intuition may be opened as a proposal to collect examples, but it should not enter the stable catalog yet.

## Conventions

- IDs use the `VI-HUM`, `VI-TRA`, `VI-GRA`, or `VI-STY` namespace.
- `name` uses lowercase ASCII and hyphens.
- User-facing Vietnamese documentation is written in Vietnamese; identifiers and technical terms may remain in English.
- Do not add AI-detection scores, detector-bypass claims, or heuristics intended to evade checks.
- Do not treat regional variation as an error without a specific register constraint.
- Importable logic belongs in `vietnamese_writing_skills`; `scripts/` contains compatibility wrappers only.

## Reporting errors and evaluation results

For a false positive, provide the shortest passage that preserves enough context, plus its domain, register, finding type, expected output, and why the structure is legitimate. Do not submit sensitive data.

## Release checklist

Before pushing a release tag:

1. Confirm that CI is green on `main`.
2. Confirm that `pyproject.toml`, `vietnamese_writing_skills.__version__`, and `CHANGELOG.md` agree on the version.
3. Run the full repository checks, build wheel and sdist, and run `twine check dist/*`.
4. Confirm that the GitHub `pypi` environment and PyPI Trusted Publisher target `.github/workflows/release.yml`.
5. Review the wheel contents and install it in a clean virtual environment.
6. Push the matching `vX.Y.Z` tag only after all checks pass.
