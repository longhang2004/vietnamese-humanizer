import tomllib
from pathlib import Path

import vietnamese_writing_skills
from vietnamese_writing_skills.cli import (
    benchmarks,
    generate_docs,
    lint,
    validate_examples,
    validate_patterns,
    validate_skills,
)
from vietnamese_writing_skills.core.paths import data_location
from vietnamese_writing_skills.core.patterns import pattern_index

ROOT = Path(__file__).resolve().parents[1]


def test_package_import_and_version() -> None:
    assert vietnamese_writing_skills.__version__ == "0.2.0"


def test_console_entry_modules_expose_main() -> None:
    modules = (
        lint,
        validate_skills,
        validate_patterns,
        validate_examples,
        benchmarks,
        generate_docs,
    )
    assert all(callable(module.main) for module in modules)


def test_repository_resources_are_loaded() -> None:
    location = data_location("patterns", ROOT)
    assert len(pattern_index(location)) == 40


def test_pyproject_packages_official_import_and_resources() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'packages = ["src/vietnamese_writing_skills"]' in pyproject
    assert '"patterns" = "vietnamese_writing_skills/data/patterns"' in pyproject


def test_release_metadata_matches_package_version() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]

    assert project["version"] == vietnamese_writing_skills.__version__
    assert project["readme"] == "README.md"
    assert project["license"] == "MIT"
    assert project["license-files"] == ["LICENSE"]
    assert "Programming Language :: Python :: 3.14" in project["classifiers"]
    assert "Natural Language :: Vietnamese" in project["classifiers"]
    assert project["urls"] == {
        "Homepage": "https://github.com/longhang2004/vietnamese-humanizer",
        "Repository": "https://github.com/longhang2004/vietnamese-humanizer",
        "Issues": "https://github.com/longhang2004/vietnamese-humanizer/issues",
        "Changelog": "https://github.com/longhang2004/vietnamese-humanizer/blob/main/CHANGELOG.md",
        "Documentation": "https://github.com/longhang2004/vietnamese-humanizer/tree/main/docs",
    }


def test_scripts_are_thin_non_package_wrappers() -> None:
    assert not (ROOT / "scripts" / "__init__.py").exists()
    for path in (ROOT / "scripts").glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "from " + "scripts" not in text
        assert len(text.splitlines()) <= 5


def test_ci_checks_artifacts_and_all_console_commands() -> None:
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "twine check dist/*" in workflow
    commands = (
        "viet-writing-lint",
        "viet-writing-validate-skills",
        "viet-writing-validate-patterns",
        "viet-writing-validate-examples",
        "viet-writing-benchmark",
        "viet-writing-generate-docs",
    )
    for command in commands:
        assert f".tmp-wheel-venv/bin/{command} --help" in workflow


def test_release_workflow_is_tag_gated_and_uses_trusted_publishing() -> None:
    path = ROOT / ".github" / "workflows" / "release.yml"
    assert path.is_file()
    workflow = path.read_text(encoding="utf-8")

    assert '      - "v*"' in workflow
    assert "Verify tag matches package version" in workflow
    assert "actions/upload-artifact@v6" in workflow
    assert "actions/download-artifact@v7" in workflow
    assert "environment: pypi" in workflow
    assert "id-token: write" in workflow
    assert "pypa/gh-action-pypi-publish@release/v1" in workflow
    assert "needs: publish-pypi" in workflow
    assert "gh release create" in workflow
