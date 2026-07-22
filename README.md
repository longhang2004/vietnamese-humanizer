**English** | [Tiếng Việt](README.vi.md)

# Vietnamese Writing Skills

[![Live Web App](https://img.shields.io/badge/Web_App-Live_Demo-brightgreen?style=flat&logo=vercel)](https://vietnamese-humanizer-g1o9.vercel.app/)
[![CI](https://github.com/longhang2004/vietnamese-humanizer/actions/workflows/ci.yml/badge.svg)](https://github.com/longhang2004/vietnamese-humanizer/actions/workflows/ci.yml)
[![Python 3.11–3.14](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

🌐 **Live Web Application**: [https://vietnamese-humanizer-g1o9.vercel.app/](https://vietnamese-humanizer-g1o9.vercel.app/)

Tools for editing Vietnamese prose without changing its facts. They help make writing clearer, more natural, and consistent with its context.

This repository is named `vietnamese-humanizer` because that is its project URL. The product is called **Vietnamese Writing Skills** because it contains four skills, not just a humanizer. Its Python distribution is `vietnamese-writing-skills`; import it as `vietnamese_writing_skills`.

The project does not classify authorship, produce an "AI probability score," or offer detector-evasion advice. Its linter reports surface signals for a person to review.

## Four skills

| Skill | Use it when | Do not use it when |
| --- | --- | --- |
| `humanizer-vi` | Prose feels templated, clichéd, flat in rhythm, or uneven in voice | Inferring authorship, evading detectors, or doing only mechanical proofreading |
| `translationese-cleaner-vi` | Vietnamese copies English word order, metaphors, or nominalization too closely | Replacing established terms or weakening legal language |
| `grammar-checker-vi` | Checking spelling, punctuation, structure, or ambiguity | Imposing a style or changing code, URLs, or identifiers |
| `style-guide-vi` | Keeping pronouns, terms, numbers, and formatting consistent | Overriding a project style guide or changing facts |

## Fact-preserving example

Before:

> Trong bài viết này, chúng ta sẽ cùng tìm hiểu cách Redis lưu dữ liệu thường dùng trong bộ nhớ để giảm số lần truy cập nguồn dữ liệu chậm hơn.

After:

> Redis lưu dữ liệu thường dùng trong bộ nhớ, nhờ đó hệ thống ít phải truy cập nguồn dữ liệu chậm hơn.

This edit removes only the announcement. The input already states the Redis mechanism, so an editor must not replace it with a broad claim such as "Redis improves performance." Corpus entries must state any information outside the input in `context`.

## Four output modes

- `clean_rewrite`: A fact-preserving rewrite that can replace the input.
- `review_comment`: Feedback for an author when evidence or sources are missing, not replacement text.
- `needs_author_decision`: The input has multiple plausible readings, so the author decides before editing.
- `no_change`: The input is already suitable. Do not change it merely for variety.

An agent does not need to rewrite every input. It should decline to guess when the subject, scope, date, or level of obligation is unclear.

## Run the web app locally

Python 3.11+, Node.js 20.9+, and npm are required. From a source checkout, the primary quickstart is:

```bash
python3 scripts/dev.py demo
```

The command checks the local prerequisites, creates or repairs `.venv`, installs the root and backend development packages, runs `npm ci`, and starts the backend and frontend. It is safe to run again. Open `http://localhost:3000`; press Ctrl-C to stop both servers.

The local demo intentionally disables rewrite, contribution, and admin capabilities. Lint remains available without provider credentials or a database. See the [web guide](web/README.md) for capability-specific environment variables and the [maintainer guide](docs/maintainer-guide.md) for repository checks and release work.

## Install Agent Skills

The fastest way to add these skills to an AI agent (such as Cursor, Claude Code, Antigravity, Windsurf, or VS Code) is using `npx skills`:

```bash
# Add all 4 skills from this repository
npx skills add longhang2004/vietnamese-humanizer

# Or add a specific skill (e.g. humanizer-vi)
npx skills add longhang2004/vietnamese-humanizer --skill humanizer-vi
```

Alternatively, install manually from a git checkout:

```bash
git clone https://github.com/longhang2004/vietnamese-humanizer.git
cd vietnamese-humanizer
```

Point an Agent Skills-compatible client at the needed directory under `skills/`, or copy that directory into the client's skill location. Each one includes `SKILL.md`, references, and any required assets.

Example request:

```text
Use humanizer-vi to edit this email. Keep the professional tone and preserve
every number, product name, condition, and deadline.
```

## Install the Python CLI

Python 3.11 or newer is required. Install from a source checkout:

```bash
python -m pip install .
```

Build and install a wheel:

```bash
python -m pip install build
python -m build
python -m pip install dist/*.whl
```

Install for development:

```bash
python -m pip install -e ".[dev]"
```

The wheel includes patterns, schemas, skill Markdown, examples, and benchmark resources. When it finds a surrounding repository, the CLI uses that repository by default. Pass `--root PATH` to choose another checkout. Outside a repository, pattern-reading commands use the resources bundled in the wheel.

## Console commands

```bash
viet-writing-lint article.md
viet-writing-lint article.md --format json
viet-writing-lint docs/ --recursive --root .
viet-writing-validate-skills --root .
viet-writing-validate-patterns --root .
viet-writing-validate-examples --root .
viet-writing-benchmark --root . --validate-only
viet-writing-generate-docs --root . --check
```

Source checkouts also retain these legacy wrappers:

```bash
python scripts/lint_vietnamese.py article.md
python scripts/validate_skills.py
python scripts/validate_patterns.py
python scripts/validate_examples.py
python scripts/run_benchmarks.py --validate-only
python scripts/generate_pattern_docs.py --check
```

The linter exits with `1` when it finds material to review and `2` when it cannot run. A finding does not prove that prose is wrong or AI-generated.

## Linter taxonomy

- `ERROR`: A relatively demonstrable error, such as an accidental repeated word or invalid spacing.
- `WARNING`: A structure that may be ambiguous or inconsistent but requires context.
- `PREFERENCE`: A style choice that should only be applied after a style has been selected.
- `HEURISTIC`: A surface signal such as density or sentence rhythm; a reviewer must inspect the full scope.

Patterns also define `scope` and `aggregation`. Repeated sentence openings, for example, use `paragraph/sequence`; sentence rhythm uses `document/variance`; mixed pronouns use `document/consistency`.

## Corpus and benchmark

The catalog has 40 patterns with finding type, scope, aggregation, exceptions, and false-positive risk. Its 100 examples specify an output mode, `context`, `must_preserve`, `must_not_add`, and review provenance. The 30 benchmark cases record an expected output mode, context, specific blockers, and preservation constraints. JSON Schema validates manual-review results, and a case may have several reviewers.

A coding agent audited each input + context → output pair in the corpus. `agent-reviewed` does not mean reviewed by a maintainer, native speaker, or independent reviewer. The repository has no independent baseline yet. The current benchmark helps with process design and data regression; it does not establish effectiveness outside these authored cases.

## Check the repository

```bash
ruff check .
pytest
python scripts/validate_skills.py
python scripts/validate_patterns.py
python scripts/validate_examples.py
python scripts/run_benchmarks.py --validate-only
python scripts/generate_pattern_docs.py --check
python -m build
```

Regenerate the pattern documentation after editing YAML:

```bash
python scripts/generate_pattern_docs.py
```

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), the [Code of Conduct](CODE_OF_CONDUCT.md), the [documentation index](docs/README.md), and the [pattern authoring guide](docs/pattern-authoring-guide.md). New examples need enough input and context for verification, explicit preservation and no-addition constraints, an output mode, and accurate review provenance. New patterns need a taxonomy, scope, aggregation behavior, exceptions, tests, and examples that add no facts.

## Limitations

Regexes and structural validators cannot prove semantic equivalence. They can miss problems or produce false positives. One hundred examples cannot represent every regional, generational, professional, or register difference. See [limitations](docs/limitations.md) and [evaluation methodology](docs/evaluation-methodology.md).

## Support the project

If Vietnamese Writing Skills is useful, you can make an optional donation to support maintenance. Before confirming a transfer, verify that the recipient is **HANG NHUT LONG** at **BIDV**.

<p align="center">
  <a href="assets/donate-vietqr.png">
    <img src="https://raw.githubusercontent.com/longhang2004/vietnamese-humanizer/main/assets/donate-vietqr.png" alt="VietQR donation code for HANG NHUT LONG at BIDV" width="360">
  </a>
</p>

## Contributors and acknowledgments

- **Hàng Nhựt Long** ([@longhang2004](https://github.com/longhang2004)) — Core maintainer & developer.
- **Lê Ngọc Phương Thư** (`lengocphuongthuct2006@gmail.com`) — Suggested and ideated the web application version.

The project draws on the [Agent Skills specification](https://agentskills.io/specification), style-audit ideas from [blader/humanizer](https://github.com/blader/humanizer), and localization work in Chinese and Korean projects. The Vietnamese taxonomy and data in this repository were written independently. Details are in the [research notes](docs/research-notes.md).

Original code and content are released under the [MIT License](LICENSE). See [ROADMAP.md](ROADMAP.md) for planned work.
