import tomllib
from pathlib import Path

import yaml

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

    assert pyproject["build-system"]["requires"] == ["hatchling>=1.27"]
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
    workflow_text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(
        encoding="utf-8"
    )
    workflow = yaml.safe_load(workflow_text)
    jobs = workflow["jobs"]

    assert jobs["lint-test"]["strategy"]["matrix"]["python-version"] == [
        "3.11",
        "3.12",
        "3.13",
        "3.14",
    ]
    assert jobs["package"]["steps"][1]["with"]["python-version"] == "3.14"
    assert "twine check dist/*" in workflow_text
    commands = (
        "viet-writing-lint",
        "viet-writing-validate-skills",
        "viet-writing-validate-patterns",
        "viet-writing-validate-examples",
        "viet-writing-benchmark",
        "viet-writing-generate-docs",
    )
    for command in commands:
        assert f".tmp-wheel-venv/bin/{command} --help" in workflow_text


def test_release_workflow_is_tag_gated_and_uses_trusted_publishing() -> None:
    path = ROOT / ".github" / "workflows" / "release.yml"
    assert path.is_file()
    workflow_text = path.read_text(encoding="utf-8")
    workflow = yaml.safe_load(workflow_text)
    jobs = workflow["jobs"]

    assert '      - "v*"' in workflow_text

    build = jobs["build"]
    build_commands = [step.get("run") for step in build["steps"] if "run" in step]
    assert build_commands.count("python -m build") == 1
    tag_check = next(
        step for step in build["steps"] if step.get("name") == "Verify tag matches package version"
    )
    assert "GITHUB_REF_NAME" in tag_check["run"]
    assert "f'v{version}'" in tag_check["run"]
    upload = next(
        step for step in build["steps"] if step.get("uses") == "actions/upload-artifact@v6"
    )
    assert upload["with"] == {
        "name": "python-distributions",
        "path": "dist/",
        "if-no-files-found": "error",
    }

    publish = jobs["publish-pypi"]
    assert publish["needs"] == "build"
    assert publish["environment"] == "pypi"
    assert publish["permissions"] == {"id-token": "write"}
    assert publish["steps"][0] == {
        "uses": "actions/download-artifact@v7",
        "with": {"name": "python-distributions", "path": "dist/"},
    }
    assert publish["steps"][1]["uses"] == "pypa/gh-action-pypi-publish@release/v1"

    release = jobs["github-release"]
    assert release["needs"] == "publish-pypi"
    assert release["permissions"] == {"contents": "write"}
    assert release["steps"][0] == publish["steps"][0]
    assert "gh release create" in release["steps"][1]["run"]


def test_release_hardening_files_and_status_are_present() -> None:
    security_path = ROOT / "SECURITY.md"
    dependabot_path = ROOT / ".github" / "dependabot.yml"
    assert security_path.is_file()
    assert dependabot_path.is_file()

    security = security_path.read_text(encoding="utf-8")
    dependabot = dependabot_path.read_text(encoding="utf-8")
    roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert "/security/advisories/new" in security
    assert "sensitive" in security.lower()
    assert 'package-ecosystem: "pip"' in dependabot
    assert 'package-ecosystem: "github-actions"' in dependabot
    assert dependabot.count('interval: "weekly"') == 2
    assert "## 0.2.x / Post-0.2" in roadmap
    assert "## 0.2\n" not in roadmap
    unreleased, released = changelog.split("## [0.2.0]", 1)
    assert "Trusted Publishing" not in unreleased
    assert "Trusted Publishing" in released
    assert "Python 3.11–3.14" in released
