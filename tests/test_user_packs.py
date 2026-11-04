import hashlib
import io
import json
import posixpath
import re
import zipfile
from pathlib import Path

import pytest
import yaml

from vietnamese_writing_skills.cli.export_user_packs import SKILL_IDS, build_packs, main

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "web/frontend/public/downloads"


@pytest.fixture(scope="module")
def packs() -> dict[str, bytes]:
    return build_packs(ROOT)


def test_downloads_match_current_skills_and_checksums(packs) -> None:
    manifest = json.loads(packs["manifest.json"])
    for name, content in packs.items():
        assert (DOWNLOADS / name).read_bytes() == content, name
        if name != "manifest.json":
            assert manifest["artifacts"][name] == {
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
    assert {
        path.relative_to(DOWNLOADS).as_posix() for path in DOWNLOADS.rglob("*") if path.is_file()
    } == set(packs)


@pytest.mark.parametrize("platform", ["claude", "gemini"])
def test_native_archives_have_correct_layout_complete_references_and_no_execution(platform, packs):
    for skill_id in SKILL_IDS:
        prefix = f"{skill_id}/" if platform == "claude" else ""
        with zipfile.ZipFile(io.BytesIO(packs[f"{platform}/{skill_id}.zip"])) as archive:
            names = set(archive.namelist())
            assert prefix + "SKILL.md" in names
            assert prefix + "LICENSE.txt" in names
            for name in names:
                assert not name.startswith("/") and ".." not in name.split("/")
                assert name.endswith((".md", ".txt"))
                text = archive.read(name).decode("utf-8")
                for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
                    clean = target.split("#", 1)[0]
                    if clean and not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", clean):
                        assert (
                            posixpath.normpath(posixpath.join(posixpath.dirname(name), clean))
                            in names
                        )
            skill = archive.read(prefix + "SKILL.md").decode("utf-8")
            _, frontmatter, body = skill.split("---", 2)
            metadata = yaml.safe_load(frontmatter)
            assert metadata["name"] == skill_id
            assert len(metadata["description"]) <= 200
            original_body = (ROOT / "skills" / skill_id / "SKILL.md").read_text().split("---", 2)[2]
            assert body == original_body


def test_chatgpt_package_contains_the_four_skills_and_local_icon(packs) -> None:
    with zipfile.ZipFile(io.BytesIO(packs["chatgpt/vietnamese-writing-skills.zip"])) as archive:
        plugin = json.loads(archive.read("plugin.json"))
        assert plugin["name"] == "vietnamese-writing-skills"
        assert plugin["license"] == "MIT"
        interface = plugin["extensions"]["com.openai"]["interface"]
        assert len(interface["displayName"]) <= 30
        assert len(interface["shortDescription"]) <= 30
        assert interface["logo"].removeprefix("./") in archive.namelist()
        for skill_id in SKILL_IDS:
            assert f"skills/{skill_id}/SKILL.md" in archive.namelist()
        assert "mcp.json" not in archive.namelist()


def test_portable_guide_links_are_self_contained(packs) -> None:
    guide = packs["huong-dan-tieng-viet.md"].decode("utf-8")
    anchors = set(re.findall(r'<a id="([^"]+)"></a>', guide))
    for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", guide):
        if target.startswith("#"):
            assert target[1:] in anchors
        else:
            assert re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target)


def test_check_mode_rejects_a_corrupt_or_extra_download(tmp_path, packs, capsys) -> None:
    for name, data in packs.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (tmp_path / "claude/humanizer-vi.zip").write_bytes(b"corrupt")
    (tmp_path / "old.zip").write_bytes(b"obsolete")
    assert main(["--root", str(ROOT), "--output", str(tmp_path), "--check"]) == 1
    message = capsys.readouterr().out
    assert "claude/humanizer-vi.zip" in message
    assert "old.zip" in message
