# 贡献插件

1. 阅读 [`docs/CREATE_PLUGIN.zh-CN.md`](docs/CREATE_PLUGIN.zh-CN.md)。
2. 从 `templates/basic-plugin` 复制插件骨架到 `plugins/<plugin-name>`。
3. 完成 `.looma-plugin/plugin.json` 和至少一个 `SKILL.md`。
4. 在 `marketplace.json` 末尾追加插件条目，并更新 `updatedAt`。
5. 执行 `python scripts/validate.py --all`。
6. 提交 Pull Request，说明插件用途、外部依赖、权限需求和验证方式。

维护者会重点检查名称唯一性、Skill 触发描述、密钥泄露、危险命令、外部下载和
MCP 配置写入行为。插件不能绕过 Looma 的用户授权边界。

