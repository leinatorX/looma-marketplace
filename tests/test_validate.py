"""Marketplace 与插件清单校验的正向与负向测试（Codex 官方格式）。"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate import ValidationError, validate_marketplace, validate_plugin  # noqa: E402


class BaseMarketplaceCase(unittest.TestCase):
    """在临时目录中搭建最小市场结构，逐项注入错误后断言校验失败。"""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="looma-mp-test-"))
        self.plugin = self.root / "plugins" / "probe"
        (self.plugin / ".codex-plugin").mkdir(parents=True)
        (self.plugin / "skills" / "probe-skill").mkdir(parents=True)
        (self.plugin / ".codex-plugin" / "plugin.json").write_text(
            json.dumps(
                {
                    "name": "probe",
                    "version": "1.0.0",
                    "description": "用于市场校验测试的最小插件。",
                    "skills": "./skills/",
                }
            ),
            encoding="utf-8",
        )
        (self.plugin / "skills" / "probe-skill" / "SKILL.md").write_text(
            "---\nname: probe-skill\ndescription: 校验测试 Skill。\n---\n\n正文。\n",
            encoding="utf-8",
        )
        self.marketplace_dir = self.root / ".agents" / "plugins"
        self.marketplace_dir.mkdir(parents=True)
        self.marketplace = self.marketplace_dir / "marketplace.json"

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def write_marketplace(self, value):
        self.marketplace.write_text(json.dumps(value), encoding="utf-8")

    def valid_marketplace(self):
        return {
            "name": "probe-marketplace",
            "plugins": [
                {
                    "name": "probe",
                    "source": {"source": "local", "path": "./plugins/probe"},
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                    "category": "Developer Tools",
                }
            ],
        }


class MarketplacePositive(BaseMarketplaceCase):
    def test_valid_marketplace_passes(self):
        self.write_marketplace(self.valid_marketplace())
        validate_marketplace(self.marketplace)

    def test_local_source_plain_string_path_still_rejected(self):
        # 官方文档允许 local source 为纯字符串路径；本仓库校验要求 ./ 前缀对象形态。
        value = self.valid_marketplace()
        value["plugins"][0]["source"] = "./plugins/probe"
        self.write_marketplace(value)
        with self.assertRaises(ValidationError):
            validate_marketplace(self.marketplace)

    def test_empty_plugins_array_passes(self):
        value = self.valid_marketplace()
        value["plugins"] = []
        self.write_marketplace(value)
        validate_marketplace(self.marketplace)


class MarketplaceNegative(BaseMarketplaceCase):
    def check_fails(self, mutate):
        value = self.valid_marketplace()
        mutate(value)
        self.write_marketplace(value)
        with self.assertRaises(ValidationError):
            validate_marketplace(self.marketplace)

    def test_missing_marketplace_name(self):
        def mutate(v):
            del v["name"]

        self.check_fails(mutate)

    def test_missing_policy_installation(self):
        def mutate(v):
            del v["plugins"][0]["policy"]["installation"]

        self.check_fails(mutate)

    def test_missing_policy_authentication(self):
        def mutate(v):
            del v["plugins"][0]["policy"]["authentication"]

        self.check_fails(mutate)

    def test_missing_category(self):
        def mutate(v):
            del v["plugins"][0]["category"]

        self.check_fails(mutate)

    def test_source_path_not_dot_prefixed(self):
        def mutate(v):
            v["plugins"][0]["source"]["path"] = "plugins/probe"

        self.check_fails(mutate)

    def test_source_path_escapes_marketplace_root(self):
        def mutate(v):
            v["plugins"][0]["source"]["path"] = "./../../outside"

        self.check_fails(mutate)

    def test_source_path_backslash_rejected(self):
        def mutate(v):
            v["plugins"][0]["source"]["path"] = ".\\plugins\\probe"

        self.check_fails(mutate)

    def test_plugin_missing_codex_manifest(self):
        shutil.rmtree(self.plugin / ".codex-plugin")
        value = self.valid_marketplace()
        self.write_marketplace(value)
        with self.assertRaises(ValidationError):
            validate_marketplace(self.marketplace)

    def test_manifest_name_mismatch(self):
        value = self.valid_marketplace()
        value["plugins"][0]["name"] = "other-plugin"
        self.write_marketplace(value)
        with self.assertRaises(ValidationError):
            validate_marketplace(self.marketplace)

    def test_manifest_references_missing_skills(self):
        manifest = self.plugin / ".codex-plugin" / "plugin.json"
        manifest.write_text(
            json.dumps(
                {
                    "name": "probe",
                    "version": "1.0.0",
                    "description": "引用不存在 skills 的插件。",
                    "skills": "./missing-skills/",
                }
            ),
            encoding="utf-8",
        )
        value = self.valid_marketplace()
        self.write_marketplace(value)
        with self.assertRaises(ValidationError):
            validate_marketplace(self.marketplace)

    def test_manifest_references_missing_mcp_file(self):
        manifest = self.plugin / ".codex-plugin" / "plugin.json"
        manifest.write_text(
            json.dumps(
                {
                    "name": "probe",
                    "version": "1.0.0",
                    "description": "引用不存在 MCP 配置的插件。",
                    "skills": "./skills/",
                    "mcpServers": "./.mcp.json",
                }
            ),
            encoding="utf-8",
        )
        value = self.valid_marketplace()
        self.write_marketplace(value)
        with self.assertRaises(ValidationError):
            validate_marketplace(self.marketplace)

    def test_manifest_references_missing_hooks(self):
        manifest = self.plugin / ".codex-plugin" / "plugin.json"
        manifest.write_text(
            json.dumps(
                {
                    "name": "probe",
                    "version": "1.0.0",
                    "description": "引用不存在 hooks 的插件。",
                    "skills": "./skills/",
                    "hooks": "./hooks/hooks.json",
                }
            ),
            encoding="utf-8",
        )
        value = self.valid_marketplace()
        self.write_marketplace(value)
        with self.assertRaises(ValidationError):
            validate_marketplace(self.marketplace)

    def test_manifest_references_missing_icon(self):
        manifest = self.plugin / ".codex-plugin" / "plugin.json"
        manifest.write_text(
            json.dumps(
                {
                    "name": "probe",
                    "version": "1.0.0",
                    "description": "引用不存在图标的插件。",
                    "skills": "./skills/",
                    "interface": {"composerIcon": "./assets/icon.png"},
                }
            ),
            encoding="utf-8",
        )
        value = self.valid_marketplace()
        self.write_marketplace(value)
        with self.assertRaises(ValidationError):
            validate_marketplace(self.marketplace)

    def test_url_with_embedded_credentials(self):
        def mutate(v):
            v["plugins"][0]["source"] = {
                "source": "url",
                "url": "https://user:secret@example.com/repo.git",
            }

        self.check_fails(mutate)

    def test_duplicate_plugin_entries(self):
        def mutate(v):
            v["plugins"].append(v["plugins"][0])

        self.check_fails(mutate)

    def test_invalid_installation_policy(self):
        def mutate(v):
            v["plugins"][0]["policy"]["installation"] = "BLOCKED"

        self.check_fails(mutate)

    def test_invalid_authentication_policy(self):
        def mutate(v):
            v["plugins"][0]["policy"]["authentication"] = "NONE"

        self.check_fails(mutate)

    def test_invalid_plugin_name(self):
        def mutate(v):
            v["plugins"][0]["name"] = "Bad Name"

        self.check_fails(mutate)

    def test_git_subdir_url_with_credentials(self):
        def mutate(v):
            v["plugins"][0]["source"] = {
                "source": "git-subdir",
                "url": "https://user:secret@example.com/repo.git",
                "path": "./plugins/probe",
            }

        self.check_fails(mutate)

    def test_git_subdir_path_escapes_root(self):
        def mutate(v):
            v["plugins"][0]["source"] = {
                "source": "git-subdir",
                "url": "https://example.com/repo.git",
                "path": "./../../outside",
            }

        self.check_fails(mutate)

    def test_npm_registry_with_credentials(self):
        def mutate(v):
            v["plugins"][0]["source"] = {
                "source": "npm",
                "package": "@example/plugin",
                "registry": "https://user:secret@registry.example.com",
            }

        self.check_fails(mutate)

    def test_npm_registry_with_query(self):
        def mutate(v):
            v["plugins"][0]["source"] = {
                "source": "npm",
                "package": "@example/plugin",
                "registry": "https://registry.example.com?token=x",
            }

        self.check_fails(mutate)


class PluginNegative(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="looma-plugin-test-"))
        self.plugin = self.root / "probe"
        (self.plugin / ".codex-plugin").mkdir(parents=True)
        (self.plugin / "skills" / "probe-skill").mkdir(parents=True)
        (self.plugin / "skills" / "probe-skill" / "SKILL.md").write_text(
            "---\nname: probe-skill\ndescription: 校验测试 Skill。\n---\n\n正文。\n",
            encoding="utf-8",
        )
        self.manifest_path = self.plugin / ".codex-plugin" / "plugin.json"

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def write_manifest(self, value):
        self.manifest_path.write_text(json.dumps(value), encoding="utf-8")

    def valid_manifest(self):
        return {
            "name": "probe",
            "version": "1.0.0",
            "description": "用于插件校验测试的最小插件。",
            "skills": "./skills/",
        }

    def test_valid_plugin_passes(self):
        self.write_manifest(self.valid_manifest())
        validate_plugin(self.plugin)

    def test_missing_manifest(self):
        self.write_manifest(self.valid_manifest())
        self.manifest_path.unlink()
        with self.assertRaises(ValidationError):
            validate_plugin(self.plugin)

    def test_manifest_skills_path_escapes_root(self):
        value = self.valid_manifest()
        value["skills"] = "./../../outside/"
        self.write_manifest(value)
        with self.assertRaises(ValidationError):
            validate_plugin(self.plugin)

    def test_manifest_skills_path_absolute(self):
        value = self.valid_manifest()
        value["skills"] = "/absolute/path/"
        self.write_manifest(value)
        with self.assertRaises(ValidationError):
            validate_plugin(self.plugin)

    def test_invalid_brand_color(self):
        value = self.valid_manifest()
        value["interface"] = {"brandColor": "red"}
        self.write_manifest(value)
        with self.assertRaises(ValidationError):
            validate_plugin(self.plugin)

    def test_invalid_semver(self):
        value = self.valid_manifest()
        value["version"] = "v1"
        self.write_manifest(value)
        with self.assertRaises(ValidationError):
            validate_plugin(self.plugin)

    def test_short_description(self):
        value = self.valid_manifest()
        value["description"] = "短"
        self.write_manifest(value)
        with self.assertRaises(ValidationError):
            validate_plugin(self.plugin)

    def test_skill_dir_name_mismatch(self):
        (self.plugin / "skills" / "probe-skill" / "SKILL.md").write_text(
            "---\nname: other-name\ndescription: 名称不一致的 Skill。\n---\n\n正文。\n",
            encoding="utf-8",
        )
        self.write_manifest(self.valid_manifest())
        with self.assertRaises(ValidationError):
            validate_plugin(self.plugin)

    def test_duplicate_skill_names(self):
        (self.plugin / "skills" / "probe-other").mkdir()
        (self.plugin / "skills" / "probe-other" / "SKILL.md").write_text(
            "---\nname: probe-skill\ndescription: 与第一个 Skill 同名。\n---\n\n正文。\n",
            encoding="utf-8",
        )
        self.write_manifest(self.valid_manifest())
        with self.assertRaises(ValidationError):
            validate_plugin(self.plugin)


if __name__ == "__main__":
    unittest.main()
