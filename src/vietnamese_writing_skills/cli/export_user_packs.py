"""Build deterministic, instruction-only downloads for nontechnical users."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import stat
import tomllib
import zipfile
from pathlib import Path
from typing import Any

import yaml

SKILL_IDS = (
    "humanizer-vi",
    "translationese-cleaner-vi",
    "grammar-checker-vi",
    "style-guide-vi",
)
LINK = re.compile(r"\[([^]]+)\]\(([^)]+)\)")
SITE = "https://vietnamese-humanizer-g1o9.vercel.app"
REPO = "https://github.com/longhang2004/vietnamese-humanizer"


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def text_bytes(path: Path) -> bytes:
    return path.read_text(encoding="utf-8").encode("utf-8")


def zip_bytes(files: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    # Stored ZIPs are byte-stable across Python/zlib versions used by CI and releases.
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, content)
    return stream.getvalue()


def anchor(path: str) -> str:
    return "resource-" + path.replace("/", "-").replace(".", "-").lower()


def build_packs(root: Path) -> dict[str, bytes]:
    root = root.resolve()
    catalog = json.loads((root / "distribution/catalog.json").read_text(encoding="utf-8"))
    if tuple(item["id"] for item in catalog["skills"]) != SKILL_IDS:
        raise ValueError("Catalog must list exactly the four supported skills in order")
    install_url = catalog["chatgpt_install_url"]
    if install_url is not None and not install_url.startswith("https://chatgpt.com/"):
        raise ValueError("ChatGPT install URL must be an official HTTPS listing")
    version = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"][
        "version"
    ]
    license_text = text_bytes(root / "LICENSE")
    source_files: dict[str, bytes] = {}
    native: dict[str, dict[str, bytes]] = {}
    for item in catalog["skills"]:
        skill_id = item["id"]
        if not 1 <= len(item["description"]) <= 200:
            raise ValueError(f"Description must be 1–200 characters: {skill_id}")
        directory = root / "skills" / skill_id
        if directory.is_symlink() or not directory.resolve().is_relative_to(root / "skills"):
            raise ValueError(f"Skill directory must stay inside skills/: {skill_id}")
        paths = [directory / "SKILL.md"]
        for name in ("references", "assets"):
            folder = directory / name
            if folder.exists():
                paths.extend(sorted(folder.rglob("*.md")))
                paths.extend(sorted(folder.rglob("*.txt")))
        native[skill_id] = {}
        for path in paths:
            if any(part.startswith(".") for part in path.relative_to(directory).parts):
                continue
            if path.is_symlink() or not path.resolve().is_relative_to(directory.resolve()):
                raise ValueError(f"Skill resources must be regular local files: {path}")
            data = text_bytes(path)
            relative = path.relative_to(directory).as_posix()
            source_files[f"skills/{skill_id}/{relative}"] = data
            if relative == "SKILL.md":
                _, frontmatter, body = data.decode("utf-8").split("---", 2)
                metadata = yaml.safe_load(frontmatter)
                if metadata["name"] != skill_id:
                    raise ValueError(f"Skill name and folder disagree: {skill_id}")
                # Short activation descriptions satisfy the narrowest target limit.
                metadata["description"] = item["description"]
                data = (
                    "---\n"
                    + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False)
                    + "---"
                    + body
                ).encode("utf-8")
                item["skill_version"] = str(metadata.get("metadata", {}).get("version", ""))
            native[skill_id][relative] = data
        native[skill_id]["LICENSE.txt"] = license_text

    def rewrite_links(text: str, source: str) -> str:
        def replace(match: re.Match[str]) -> str:
            label, target = match.groups()
            clean = target.split("#", 1)[0].strip("<>")
            if not clean or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", clean):
                return match.group(0)
            resolved = (root / source).parent.joinpath(clean).resolve()
            if not resolved.is_relative_to(root):
                raise ValueError(f"Reference escapes source tree: {source}: {target}")
            name = resolved.relative_to(root).as_posix()
            if name not in source_files:
                raise ValueError(f"Reference omitted from user packs: {source}: {target}")
            return f"[{label}](#{anchor(name)})"

        return LINK.sub(replace, text)

    prompt = (
        catalog["quick_start"]
        + "\n\n"
        + catalog["skills"][0]["request"]
        + "\n\nVăn bản cần biên tập:\n[Dán văn bản của bạn vào đây]\n"
    )
    handbook = [
        "# Hướng dẫn biên tập tiếng Việt\n",
        "Tài liệu của Vietnamese Writing Skills. Chọn phần phù hợp với yêu cầu của người dùng; "
        "các ví dụ chỉ minh họa cách biên tập, không phải dữ kiện để thêm vào văn bản.\n",
        "## Dùng nhanh\n\n" + prompt,
        "## Mục lục tài liệu\n",
    ]
    for name in source_files:
        handbook.append(f"- [{name}](#{anchor(name)})")
    for name, content in source_files.items():
        text = content.decode("utf-8")
        if name.endswith("/SKILL.md"):
            text = text.split("---", 2)[2].lstrip()
        handbook.append(f'\n<a id="{anchor(name)}"></a>\n\n' + rewrite_links(text, name))

    outputs: dict[str, bytes] = {
        "BAT-DAU.txt": (
            "VIETNAMESE WRITING SKILLS — BẮT ĐẦU SỬ DỤNG\n\n"
            f"Hướng dẫn cài đặt được đối chiếu ngày {catalog['docs_checked_on']}.\n"
            f"Trang hướng dẫn: {SITE}/start\n\n"
            "CLAUDE\nChọn một ZIP trong thư mục claude/. Mở Customize → Skills → "
            "thêm skill → Upload a skill, chọn ZIP và bật skill. Nếu được yêu cầu, "
            "bật Code execution and file creation trong Settings → Capabilities.\n\n"
            "GEMINI\nChọn một ZIP trong thư mục gemini/. Trên web Gemini, mở "
            "Customize → Skills → Create → Upload, chọn ZIP, xem lại và chọn Create. "
            "Nếu tài khoản chưa có Skills, dùng yêu cầu mẫu trong yeu-cau-bien-tap.txt.\n\n"
            "CHATGPT VÀ CHATBOT KHÁC\nMở yeu-cau-bien-tap.txt, sao chép vào cuộc "
            "trò chuyện và thay phần trong ngoặc bằng văn bản của bạn. Có thể đính kèm "
            "huong-dan-tieng-viet.md khi chatbot hỗ trợ đọc tài liệu. Yêu cầu mẫu là "
            "bản rút gọn; gói skill gồm các tài liệu tham khảo chi tiết.\n\n"
            "Bốn nhu cầu: humanizer-vi — viết tự nhiên hơn; translationese-cleaner-vi — "
            "sửa câu dịch chưa tự nhiên; grammar-checker-vi — soát lỗi tiếng Việt; "
            "style-guide-vi — "
            "giữ cách viết nhất quán.\n\n"
            "Gói trong chatgpt/ dành cho người phát hành nộp xét duyệt plugin; "
            "việc tải gói không cài plugin vào tài khoản ChatGPT.\n\n"
            "Trước khi sử dụng kết quả, đọc lại số, tên, điều kiện và cam kết. "
            "Các nền tảng và model có thể thực hiện hướng dẫn khác nhau.\n"
        ).encode(),
        "yeu-cau-bien-tap.txt": prompt.encode("utf-8"),
        "huong-dan-tieng-viet.md": ("\n\n".join(handbook).rstrip("\n") + "\n").encode("utf-8"),
    }
    plugin_files: dict[str, bytes] = {
        "LICENSE.txt": license_text,
        "assets/icon.svg": text_bytes(root / "distribution/icon.svg"),
    }
    for skill_id, files in native.items():
        outputs[f"claude/{skill_id}.zip"] = zip_bytes(
            {f"{skill_id}/{name}": content for name, content in files.items()}
        )
        outputs[f"gemini/{skill_id}.zip"] = zip_bytes(files)
        plugin_files.update({f"skills/{skill_id}/{name}": data for name, data in files.items()})
    plugin_files["plugin.json"] = json_bytes(
        {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": "vietnamese-writing-skills",
            "version": version,
            "description": "Biên tập tiếng Việt rõ, tự nhiên, nhất quán và giữ dữ kiện.",
            "author": {"name": "Vietnamese Writing Skills contributors", "url": REPO},
            "homepage": SITE + "/start",
            "repository": REPO,
            "license": "MIT",
            "keywords": ["vietnamese", "writing", "editing"],
            "extensions": {
                "com.openai": {
                    "interface": {
                        "displayName": "Viết tiếng Việt tự nhiên",
                        "shortDescription": "Sửa câu, giữ giọng và dữ kiện",
                        "longDescription": (
                            "Biên tập văn phong, sửa câu dịch, soát ngữ pháp và giữ cách viết "
                            "nhất quán. Giữ dữ kiện, thuật ngữ, xưng hô và mức chắc chắn; "
                            "hỏi người viết khi thiếu thông tin. Kết quả cần được người dùng "
                            "đọc lại trước khi sử dụng."
                        ),
                        "logo": "./assets/icon.svg",
                        "composerIcon": "./assets/icon.svg",
                    }
                }
            },
        }
    )
    outputs["chatgpt/vietnamese-writing-skills.zip"] = zip_bytes(plugin_files)
    sources = {
        **source_files,
        "distribution/catalog.json": text_bytes(root / "distribution/catalog.json"),
        "distribution/icon.svg": text_bytes(root / "distribution/icon.svg"),
        "LICENSE": license_text,
        "pyproject.toml": text_bytes(root / "pyproject.toml"),
    }
    manifest = {
        "format_version": 1,
        "project_version": version,
        "docs_checked_on": catalog["docs_checked_on"],
        "chatgpt_install_url": install_url,
        "quick_start": catalog["quick_start"],
        "skills": catalog["skills"],
        "sources": {
            name: hashlib.sha256(data).hexdigest() for name, data in sorted(sources.items())
        },
        "artifacts": {
            name: {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            for name, data in sorted(outputs.items())
        },
    }
    outputs["manifest.json"] = json_bytes(manifest)
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, help="Default: web/frontend/public/downloads")
    parser.add_argument("--check", action="store_true", help="Fail if checked-in packs are stale")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    output = (args.output or root / "web/frontend/public/downloads").resolve()
    try:
        artifacts = build_packs(root)
        if args.check:
            mismatches = [
                name
                for name, data in artifacts.items()
                if not (output / name).is_file() or (output / name).read_bytes() != data
            ]
            if output.exists():
                mismatches.extend(
                    path.relative_to(output).as_posix()
                    for path in output.rglob("*")
                    if path.is_file() and path.relative_to(output).as_posix() not in artifacts
                )
            if mismatches:
                print("Gói tải chưa đồng bộ: " + ", ".join(sorted(mismatches)))
                return 1
        else:
            for name, data in artifacts.items():
                destination = output / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
    except (OSError, ValueError, KeyError) as exc:
        print(f"Không tạo được gói tải: {exc}")
        return 1
    print(f"Gói tải đồng bộ: {len(artifacts)} tệp.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
