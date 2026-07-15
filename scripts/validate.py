#!/usr/bin/env python3
"""校验 Looma 插件清单、Skill 结构和市场索引。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
NAME_PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
HEX_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")
PLACEHOLDERS = ("Your Name", "your-account", "my-plugin", "my-skill")


class ValidationError(Exception):
    """表示一个或多个可修复的结构错误。"""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"文件不存在：{path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"JSON 无效：{path}:{exc.lineno}:{exc.colno} {exc.msg}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"根节点必须是对象：{path}")
    return value


def require_text(value: dict[str, Any], key: str, source: Path) -> str:
    item = value.get(key)
    if not isinstance(item, str) or not item.strip():
        raise ValidationError(f"{source} 的 {key} 必须是非空字符串")
    return item.strip()


def parse_skill_frontmatter(path: Path) -> dict[str, str]:
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValidationError(f"Skill 缺少 frontmatter：{path}")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValidationError(f"Skill frontmatter 未闭合：{path}") from exc

    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValidationError(f"Skill frontmatter 行格式无效：{path} -> {line}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        if key not in {"name", "description"}:
            raise ValidationError(f"Skill frontmatter 只允许 name 和 description：{path}")
        metadata[key] = raw_value.strip().strip('"\'')

    if set(metadata) != {"name", "description"}:
        raise ValidationError(f"Skill frontmatter 必须同时包含 name 和 description：{path}")
    if not metadata["description"]:
        raise ValidationError(f"Skill description 不能为空：{path}")
    if not any(line.strip() for line in lines[end + 1 :]):
        raise ValidationError(f"Skill 正文不能为空：{path}")
    return metadata


def validate_plugin(plugin_dir: Path, *, allow_template: bool = False) -> dict[str, Any]:
    plugin_dir = plugin_dir.resolve()
    manifest_path = plugin_dir / ".looma-plugin" / "plugin.json"
    manifest = load_json(manifest_path)

    if manifest.get("schemaVersion") != 1:
        raise ValidationError(f"schemaVersion 当前必须为 1：{manifest_path}")

    name = require_text(manifest, "name", manifest_path)
    version = require_text(manifest, "version", manifest_path)
    description = require_text(manifest, "description", manifest_path)
    repository = require_text(manifest, "repository", manifest_path)
    license_name = require_text(manifest, "license", manifest_path)

    if not NAME_PATTERN.fullmatch(name):
        raise ValidationError(f"插件 name 必须是小写 kebab-case，且不超过 64 字符：{name}")
    if plugin_dir.name != name and not allow_template:
        raise ValidationError(f"插件目录名必须与清单 name 一致：{plugin_dir.name} != {name}")
    if not SEMVER_PATTERN.fullmatch(version):
        raise ValidationError(f"插件 version 不是合法 SemVer：{version}")
    if len(description) < 10:
        raise ValidationError(f"插件 description 至少需要 10 个字符：{manifest_path}")
    if not repository.startswith(("https://", "http://")):
        raise ValidationError(f"repository 必须是 HTTP(S) URL：{manifest_path}")
    if not license_name:
        raise ValidationError(f"license 不能为空：{manifest_path}")

    author = manifest.get("author")
    if not isinstance(author, dict) or not isinstance(author.get("name"), str) or not author["name"].strip():
        raise ValidationError(f"author.name 必须是非空字符串：{manifest_path}")

    if manifest.get("skills") != "./skills/":
        raise ValidationError(f"skills 当前必须为 ./skills/：{manifest_path}")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        raise ValidationError(f"interface 必须是对象：{manifest_path}")
    for key in ("displayName", "shortDescription", "category", "brandColor"):
        require_text(interface, key, manifest_path)
    if not HEX_COLOR_PATTERN.fullmatch(interface["brandColor"]):
        raise ValidationError(f"interface.brandColor 必须是六位十六进制颜色：{manifest_path}")

    if not allow_template:
        serialized = json.dumps(manifest, ensure_ascii=False)
        matched = [value for value in PLACEHOLDERS if value in serialized]
        if matched:
            raise ValidationError(f"插件仍包含模板占位符 {matched}：{manifest_path}")

    skills_dir = plugin_dir / "skills"
    skill_files = sorted(skills_dir.glob("*/SKILL.md")) if skills_dir.is_dir() else []
    if not skill_files:
        raise ValidationError(f"插件至少需要一个 skills/<name>/SKILL.md：{plugin_dir}")

    skill_names: set[str] = set()
    for skill_file in skill_files:
        metadata = parse_skill_frontmatter(skill_file)
        skill_name = metadata["name"]
        if not NAME_PATTERN.fullmatch(skill_name):
            raise ValidationError(f"Skill name 必须是小写 kebab-case：{skill_file}")
        if skill_file.parent.name != skill_name:
            raise ValidationError(
                f"Skill 目录名必须与 frontmatter name 一致：{skill_file.parent.name} != {skill_name}"
            )
        if skill_name in skill_names:
            raise ValidationError(f"插件内 Skill name 重复：{skill_name}")
        skill_names.add(skill_name)

    print(f"插件校验通过：{name} {version}（{len(skill_names)} 个 Skill）")
    return manifest


def validate_marketplace(path: Path) -> None:
    catalog = load_json(path)
    if catalog.get("version") != 1:
        raise ValidationError(f"市场 version 当前必须为 1：{path}")
    updated_at = require_text(catalog, "updatedAt", path)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", updated_at):
        raise ValidationError(f"updatedAt 必须是 YYYY-MM-DD：{path}")

    plugins = catalog.get("plugins")
    if not isinstance(plugins, list):
        raise ValidationError(f"plugins 必须是数组：{path}")

    seen: set[str] = set()
    for index, entry in enumerate(plugins):
        if not isinstance(entry, dict):
            raise ValidationError(f"plugins[{index}] 必须是对象：{path}")
        plugin_id = require_text(entry, "id", path)
        if plugin_id in seen:
            raise ValidationError(f"市场插件 ID 重复：{plugin_id}")
        seen.add(plugin_id)
        if not NAME_PATTERN.fullmatch(plugin_id):
            raise ValidationError(f"市场插件 ID 必须是小写 kebab-case：{plugin_id}")

        for key in ("name", "description", "version", "author", "category", "homepage", "manifest"):
            require_text(entry, key, path)
        if not SEMVER_PATTERN.fullmatch(entry["version"]):
            raise ValidationError(f"市场插件 version 不是合法 SemVer：{plugin_id}")

        expected_manifest = f"plugins/{plugin_id}/.looma-plugin/plugin.json"
        if entry["manifest"] != expected_manifest:
            raise ValidationError(f"市场 manifest 必须为 {expected_manifest}：{plugin_id}")
        manifest_path = ROOT / expected_manifest
        manifest = validate_plugin(manifest_path.parents[1])
        if manifest["name"] != plugin_id:
            raise ValidationError(f"市场 ID 与插件清单 name 不一致：{plugin_id}")
        if manifest["version"] != entry["version"]:
            raise ValidationError(f"市场与插件清单 version 不一致：{plugin_id}")

        source = entry.get("source")
        if not isinstance(source, dict) or source.get("type") != "github":
            raise ValidationError(f"source.type 当前必须为 github：{plugin_id}")
        if source.get("path") != f"plugins/{plugin_id}":
            raise ValidationError(f"source.path 与插件 ID 不一致：{plugin_id}")
        for key in ("repository", "ref"):
            require_text(source, key, path)

        policy = entry.get("policy")
        if not isinstance(policy, dict):
            raise ValidationError(f"policy 必须是对象：{plugin_id}")
        if policy.get("installation") not in {"AVAILABLE", "BLOCKED"}:
            raise ValidationError(f"policy.installation 无效：{plugin_id}")
        if policy.get("authentication") not in {"NONE", "ON_USE", "REQUIRED"}:
            raise ValidationError(f"policy.authentication 无效：{plugin_id}")

    print(f"市场校验通过：{len(plugins)} 个插件")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验 Looma 插件与市场索引")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--plugin", type=Path, help="要校验的插件目录")
    group.add_argument("--marketplace", type=Path, help="要校验的市场 JSON")
    group.add_argument("--all", action="store_true", help="校验模板、市场和所有已发布插件")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.plugin:
            validate_plugin(args.plugin)
        elif args.marketplace:
            validate_marketplace(args.marketplace)
        else:
            validate_plugin(ROOT / "templates" / "basic-plugin", allow_template=True)
            validate_marketplace(ROOT / "marketplace.json")
            print("全部校验通过")
    except (OSError, ValidationError) as exc:
        print(f"校验失败：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

