from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

try:
    from scripts._shared import ROOT
except ModuleNotFoundError:  # Chạy trực tiếp: python scripts/validate_skills.py
    from _shared import ROOT

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")
ALLOWED_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
REQUIRED_HEADINGS = {
    "quy trình": "thiếu mục Quy trình",
    "bảo toàn": "thiếu mục Bảo toàn",
    "anti-goals": "thiếu mục Anti-goals",
}


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("thiếu frontmatter mở đầu bằng ---")
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration as exc:
        raise ValueError("frontmatter chưa được đóng bằng ---") from exc
    try:
        metadata = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        raise ValueError(f"frontmatter YAML không hợp lệ: {exc}") from exc
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter phải là một YAML mapping")
    return metadata, "\n".join(lines[end + 1 :])


def _validate_metadata(metadata: dict[str, Any], directory_name: str) -> list[str]:
    errors: list[str] = []
    unknown = sorted(set(metadata) - ALLOWED_FIELDS)
    if unknown:
        errors.append(f"frontmatter có field ngoài specification: {', '.join(unknown)}")
    name = metadata.get("name")
    description = metadata.get("description")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name) or len(name) > 64:
        errors.append("name phải dài 1-64 ký tự, chỉ gồm chữ thường, số và dấu gạch nối")
    elif name != directory_name:
        errors.append(f"name {name!r} không trùng tên thư mục {directory_name!r}")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append("description phải là chuỗi không rỗng và không quá 1024 ký tự")
    metadata_value = metadata.get("metadata")
    if metadata_value is not None and (
        not isinstance(metadata_value, dict)
        or not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in metadata_value.items()
        )
    ):
        errors.append("metadata chỉ được chứa các cặp string:string")
    return errors


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"{skill_dir}: thiếu SKILL.md"]
    if not (skill_dir / "README.md").is_file():
        errors.append(f"{skill_dir}: thiếu README.md")
    text = skill_file.read_text(encoding="utf-8")
    if len(text.splitlines()) > 500:
        errors.append(f"{skill_file}: vượt giới hạn progressive disclosure 500 dòng")
    try:
        metadata, body = parse_frontmatter(text)
    except ValueError as exc:
        return [f"{skill_file}: {exc}"]
    errors.extend(f"{skill_file}: {item}" for item in _validate_metadata(metadata, skill_dir.name))
    headings = {
        match.group(1).strip().lower()
        for match in re.finditer(r"^#{2,6}\s+(.+?)\s*$", body, flags=re.MULTILINE)
    }
    for expected, message in REQUIRED_HEADINGS.items():
        if not any(expected in heading for heading in headings):
            errors.append(f"{skill_file}: {message}")
    for target in LINK_RE.findall(body):
        clean_target = target.split("#", 1)[0].strip().strip("<>")
        if not clean_target or re.match(r"^(?:https?://|mailto:)", clean_target):
            continue
        if Path(clean_target).is_absolute() or ".." in Path(clean_target).parts:
            errors.append(f"{skill_file}: reference phải tương đối trong skill: {target}")
            continue
        if len(Path(clean_target).parts) > 2:
            errors.append(f"{skill_file}: reference sâu quá một cấp: {target}")
        if not (skill_dir / clean_target).exists():
            errors.append(f"{skill_file}: link hỏng: {target}")
    return errors


def validate_all(skills_dir: Path) -> list[str]:
    if not skills_dir.is_dir():
        return [f"{skills_dir}: thư mục skills không tồn tại"]
    directories = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    if not directories:
        return [f"{skills_dir}: chưa có skill nào"]
    return [error for directory in directories for error in validate_skill(directory)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Kiểm tra cấu trúc Agent Skills")
    parser.add_argument("path", nargs="?", type=Path, default=ROOT / "skills")
    args = parser.parse_args(argv)
    errors = validate_all(args.path.resolve())
    if errors:
        print("Skill validation thất bại:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Skill validation đạt: {len(list(args.path.iterdir()))} thư mục skill.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
