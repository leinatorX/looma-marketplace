#!/usr/bin/env python3
"""校验 Codex 官方格式的插件与 Marketplace（.agents/plugins/marketplace.json）。

只校验官方字段与 Looma 发布质量，不要求 Looma 私有 manifest 或私有 files 白名单。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"
NAME_PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
HEX_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")
INSTALLATION_VALUES = {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}
AUTHENTICATION_VALUES = {"ON_INSTALL", "ON_USE"}
SOURCE_KINDS = {"local", "git-subdir", "url", "npm"}
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


def safe_relative_path(value: str, source: Path, base: Path) -> PurePosixPath:
    """校验 ./ 开头的相对路径，且 canonicalize 后仍位于 base 之内。"""
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{source} 的路径必须是非空字符串")
    if not value.startswith("./") or "\\" in value:
        raise ValidationError(f"{source} 的路径必须以 ./ 开头且不能包含反斜杠：{value}")
    raw = PurePosixPath(value)
    if ".." in raw.parts:
        raise ValidationError(f"{source} 的路径不能包含 ..：{value}")
    target = (base / value).resolve()
    resolved_base = base.resolve()
    if target != resolved_base and resolved_base not in target.parents:
        raise ValidationError(f"{source} 的路径越过根目录：{value}")
    return raw


def url_without_credentials(value: str, source: Path) -> None:
    parsed = urlparse(value)
    if parsed.username is not None or parsed.password is not None:
        raise ValidationError(f"{source} 的 URL 不允许内嵌凭据：{value}")


def validate_manifest_paths(manifest: dict[str, Any], manifest_path: Path, plugin_dir: Path) -> None:
    """校验 manifest 中所有路径字段（./ 开头、在插件根内、目标存在）。"""
    for key in ("skills", "mcpServers", "apps", "hooks"):
        value = manifest.get(key)
        if value is None:
            continue
        values = value if isinstance(value, list) else [value]
        for item in values:
            if not isinstance(item, str):
                raise ValidationError(f"{manifest_path} 的 {key} 必须是字符串或字符串数组")
            safe_relative_path(item, manifest_path, plugin_dir)
            if not (plugin_dir / item).exists():
                raise ValidationError(f"{manifest_path} 引用的文件不存在：{item}")

    interface = manifest.get("interface")
    if isinstance(interface, dict):
        for key in ("composerIcon", "logo", "logoDark"):
            item = interface.get(key)
            if item is None:
                continue
            if not isinstance(item, str):
                raise ValidationError(f"{manifest_path} 的 interface.{key} 必须是字符串")
            safe_relative_path(item, manifest_path, plugin_dir)
            if not (plugin_dir / item).is_file():
                raise ValidationError(f"{manifest_path} 引用的图片不存在：{item}")
        screenshots = interface.get("screenshots")
        if screenshots is not None:
            if not isinstance(screenshots, list):
                raise ValidationError(f"{manifest_path} 的 interface.screenshots 必须是数组")
            for item in screenshots:
                if not isinstance(item, str):
                    raise ValidationError(f"{manifest_path} 的 interface.screenshots 元素必须是字符串")
                safe_relative_path(item, manifest_path, plugin_dir)
                if not (plugin_dir / item).is_file():
                    raise ValidationError(f"{manifest_path} 引用的截图不存在：{item}")


def validate_plugin(plugin_dir: Path, *, allow_template: bool = False) -> dict[str, Any]:
    plugin_dir = plugin_dir.resolve()
    manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
    manifest = load_json(manifest_path)

    name = require_text(manifest, "name", manifest_path)
    version = require_text(manifest, "version", manifest_path)
    description = require_text(manifest, "description", manifest_path)

    if not NAME_PATTERN.fullmatch(name):
        raise ValidationError(f"插件 name 必须是小写 kebab-case，且不超过 64 字符：{name}")
    if plugin_dir.name != name and not allow_template:
        raise ValidationError(f"插件目录名必须与清单 name 一致：{plugin_dir.name} != {name}")
    if not SEMVER_PATTERN.fullmatch(version):
        raise ValidationError(f"插件 version 不是合法 SemVer：{version}")
    if len(description) < 10:
        raise ValidationError(f"插件 description 至少需要 10 个字符：{manifest_path}")

    validate_manifest_paths(manifest, manifest_path, plugin_dir)

    interface = manifest.get("interface")
    if interface is not None:
        if not isinstance(interface, dict):
            raise ValidationError(f"interface 必须是对象：{manifest_path}")
        if "brandColor" in interface and not HEX_COLOR_PATTERN.fullmatch(interface["brandColor"]):
            raise ValidationError(f"interface.brandColor 必须是六位十六进制颜色：{manifest_path}")
        if "capabilities" in interface and not isinstance(interface["capabilities"], list):
            raise ValidationError(f"interface.capabilities 必须是字符串数组：{manifest_path}")

    if not allow_template:
        serialized = json.dumps(manifest, ensure_ascii=False)
        matched = [value for value in PLACEHOLDERS if value in serialized]
        if matched:
            raise ValidationError(f"插件仍包含模板占位符 {matched}：{manifest_path}")

    skills_value = manifest.get("skills")
    skills_dir = plugin_dir / "skills"
    if skills_value is not None or skills_dir.is_dir():
        if not skills_dir.is_dir():
            raise ValidationError(f"manifest 声明 skills 但目录不存在：{plugin_dir}")
        skill_files = sorted(skills_dir.glob("*/SKILL.md"))
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

    print(f"插件校验通过：{name} {version}")
    return manifest


def validate_marketplace_entry(
    entry: dict[str, Any], index: int, marketplace_path: Path, marketplace_root: Path
) -> str:
    source = marketplace_path
    name = require_text(entry, "name", source)
    if not NAME_PATTERN.fullmatch(name):
        raise ValidationError(f"plugins[{index}] name 必须是小写 kebab-case：{name}")

    entry_source = entry.get("source")
    if not isinstance(entry_source, dict):
        raise ValidationError(f"plugins[{index}] 缺少 source 对象：{name}")
    kind = entry_source.get("source")
    if kind not in SOURCE_KINDS:
        raise ValidationError(f"plugins[{index}] source.source 无效：{kind}")
    if kind == "local":
        local_path = require_text(entry_source, "path", source)
        relative = safe_relative_path(local_path, source, marketplace_root)
        plugin_dir = (marketplace_root / str(relative)).resolve()
        if not plugin_dir.is_dir():
            raise ValidationError(f"plugins[{index}] 的插件目录不存在：{local_path}")
        manifest = validate_plugin(plugin_dir)
        if manifest["name"] != name:
            raise ValidationError(
                f"plugins[{index}] 名称与插件清单 name 不一致：{name} != {manifest['name']}"
            )
    elif kind == "git-subdir":
        url = require_text(entry_source, "url", source)
        url_without_credentials(url, source)
        safe_relative_path(require_text(entry_source, "path", source), source, marketplace_root)
    elif kind == "url":
        url = require_text(entry_source, "url", source)
        url_without_credentials(url, source)
    elif kind == "npm":
        require_text(entry_source, "package", source)
        registry = entry_source.get("registry")
        if registry is not None:
            if not isinstance(registry, str) or not registry.startswith("https://"):
                raise ValidationError(f"plugins[{index}] npm registry 必须是 HTTPS URL：{name}")
            parsed = urlparse(registry)
            if parsed.username is not None or parsed.password is not None or parsed.query or parsed.fragment:
                raise ValidationError(f"plugins[{index}] npm registry 不允许凭据、查询或片段：{name}")

    policy = entry.get("policy")
    if not isinstance(policy, dict):
        raise ValidationError(f"plugins[{index}] 缺少 policy 对象：{name}")
    if policy.get("installation") not in INSTALLATION_VALUES:
        raise ValidationError(f"plugins[{index}] policy.installation 无效：{name}")
    if policy.get("authentication") not in AUTHENTICATION_VALUES:
        raise ValidationError(f"plugins[{index}] policy.authentication 无效：{name}")

    require_text(entry, "category", source)
    return name


def validate_marketplace(path: Path) -> None:
    marketplace = load_json(path)
    require_text(marketplace, "name", path)

    interface = marketplace.get("interface")
    if interface is not None and not isinstance(interface, dict):
        raise ValidationError(f"interface 必须是对象：{path}")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        raise ValidationError(f"plugins 必须是数组：{path}")

    # source.path 相对 marketplace 根目录解析（官方规则：不是相对 .agents/plugins/ 目录）
    marketplace_root = path.resolve().parent.parent.parent

    seen: set[str] = set()
    for index, entry in enumerate(plugins):
        if not isinstance(entry, dict):
            raise ValidationError(f"plugins[{index}] 必须是对象：{path}")
        name = validate_marketplace_entry(entry, index, path, marketplace_root)
        if name in seen:
            raise ValidationError(f"市场插件条目重复：{name}")
        seen.add(name)

    print(f"市场校验通过：{path}（{len(plugins)} 个插件）")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验 Codex 官方格式插件与 Marketplace")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--plugin", type=Path, help="要校验的插件目录")
    group.add_argument("--marketplace", type=Path, help="要校验的 Marketplace JSON")
    group.add_argument("--all", action="store_true", help="校验模板与仓库 Marketplace")
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
            validate_marketplace(MARKETPLACE_PATH)
            print("全部校验通过")
    except (OSError, ValidationError) as exc:
        print(f"校验失败：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
