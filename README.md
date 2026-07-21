**English** | [Tiếng Việt](README.vi.md)

# Vietnamese Writing Skills

[![CI](https://github.com/longhang2004/vietnamese-humanizer/actions/workflows/ci.yml/badge.svg)](https://github.com/longhang2004/vietnamese-humanizer/actions/workflows/ci.yml)
[![Python 3.11–3.14](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A Vietnamese editing toolkit that helps make writing clear, natural, consistent, and appropriate for its context without losing facts.

The repository keeps the name `vietnamese-humanizer` because that is its project URL. The product is called **Vietnamese Writing Skills** because it includes four skills, not only a humanizer. The Python distribution is named `vietnamese-writing-skills`, while the import package is `vietnamese_writing_skills`.

The project does not classify authorship, produce an “AI probability score,” or provide detector-evasion advice. The linter only identifies surface signals for human review.

## Four skills

| Skill | Use it when | Do not use it when |
| --- | --- | --- |
| `humanizer-vi` | Writing sounds templated, clichéd, rhythmically flat, or inconsistent in voice | Inferring authorship, evading detectors, or performing purely mechanical proofreading |
| `translationese-cleaner-vi` | Vietnamese follows English word order, metaphors, or nominalization too closely | Replacing established terminology or weakening legal language |
| `grammar-checker-vi` | Checking spelling, punctuation, structure, and ambiguity | Imposing a style or modifying code, URLs, and identifiers |
| `style-guide-vi` | Keeping pronouns, terminology, numbers, and formatting consistent | Overriding a project-specific style guide or changing facts |

## Fact-preserving example

Before:

> Trong bài viết này, chúng ta sẽ cùng tìm hiểu cách Redis lưu dữ liệu thường dùng trong bộ nhớ để giảm số lần truy cập nguồn dữ liệu chậm hơn.

After:

> Redis lưu dữ liệu thường dùng trong bộ nhớ, nhờ đó hệ thống ít phải truy cập nguồn dữ liệu chậm hơn.

The edit only removes the announcement phrase. The Redis mechanism was present in the input; it must not be inferred from a generic sentence such as “Redis improves performance.” In the corpus, information outside the input must be stated explicitly in the `context` field.

## Four output modes

- `clean_rewrite`: A fact-preserving rewrite that can directly replace the input.
- `review_comment`: Feedback for the author when evidence or sources are missing; it is not replacement text.
- `needs_author_decision`: Multiple interpretations are possible, so the author must decide before editing.
- `no_change`: The input is already suitable; do not edit merely to make it different.

An agent is not required to rewrite every input. Refusing to guess is correct when the subject, scope, date, or level of obligation is ambiguous.

## Install Agent Skills from the repository

```bash
git clone https://github.com/longhang2004/vietnamese-humanizer.git
cd vietnamese-humanizer
```

Point an Agent Skills-compatible client to the desired directory under `skills/`, or copy that directory into the client's skill location. Each skill contains a `SKILL.md`, references, and any required assets.

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

The wheel contains patterns, schemas, skill Markdown, examples, and benchmark resources. By default, the CLI uses the repository surrounding the current directory when one is found; pass `--root PATH` to select another checkout. Outside a repository, pattern-reading commands use resources bundled in the wheel.

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

Legacy wrappers remain available in a source checkout:

```bash
python scripts/lint_vietnamese.py article.md
python scripts/validate_skills.py
python scripts/validate_patterns.py
python scripts/validate_examples.py
python scripts/run_benchmarks.py --validate-only
python scripts/generate_pattern_docs.py --check
```

The linter exits with code `1` when it finds items that need review and `2` when the command cannot run. A finding does not prove that writing is incorrect or AI-generated.

## Linter taxonomy

- `ERROR`: A relatively demonstrable error, such as an accidental repeated word or invalid spacing.
- `WARNING`: A structure that may be ambiguous or inconsistent but requires context.
- `PREFERENCE`: A style choice that should only be applied after a style has been selected.
- `HEURISTIC`: A surface signal such as density or sentence rhythm; a reviewer must inspect the full scope.

Each pattern also defines `scope` and `aggregation`. For example, repeated sentence openings use `paragraph/sequence`, sentence rhythm uses `document/variance`, and mixed pronouns use `document/consistency`.

## Corpus and benchmark

- 40 patterns include finding type, scope, aggregation, exceptions, and false-positive risk.
- 100 examples include output mode, `context`, `must_preserve`, `must_not_add`, and review provenance.
- 30 benchmark cases include an expected output mode, context, specific blockers, and preservation constraints.
- Manual review results are checked by JSON Schema and can contain multiple reviewers per case.

The corpus has been audited by a coding agent against each input + context → output pair. `agent-reviewed` does not mean maintainer-reviewed, native-speaker-reviewed, or independently reviewed. The repository has no independent baseline yet; the current benchmark supports process design and data regression, not claims of effectiveness outside the authored cases.

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

Read [CONTRIBUTING.md](CONTRIBUTING.md), the [documentation index](docs/README.md), and the [pattern authoring guide](docs/pattern-authoring-guide.md). New examples must contain enough input/context to be verified, state what must be preserved and must not be added, choose an output mode, and record accurate review provenance. New patterns need a taxonomy, scope, aggregation behavior, exceptions, tests, and examples that do not introduce facts.

## Limitations

Regexes and structural validators cannot prove semantic equivalence; they can miss problems or report false positives. One hundred examples do not fully represent regional, generational, professional, and register variation. See [limitations](docs/limitations.md) and [evaluation methodology](docs/evaluation-methodology.md).

## Support the project

If Vietnamese Writing Skills is useful to you, you can support its continued maintenance with an optional donation. Please verify that the recipient name is **HANG NHUT LONG** at **BIDV** before confirming the transfer.

<p align="center">
  <a href="assets/donate-vietqr.png">
    <img src="https://raw.githubusercontent.com/longhang2004/vietnamese-humanizer/main/assets/donate-vietqr.png" alt="VietQR donation code for HANG NHUT LONG at BIDV" width="360">
  </a>
</p>

## Attribution and license

The project references the [Agent Skills specification](https://agentskills.io/specification), the style-audit ideas in [blader/humanizer](https://github.com/blader/humanizer), and localization experience from Chinese and Korean projects. The Vietnamese taxonomy and data in this repository were written independently. See the [research notes](docs/research-notes.md) for details.

Original code and content are released under the [MIT License](LICENSE). See [ROADMAP.md](ROADMAP.md) for planned work.
