# Looma 插件市场

这是 Looma 的公开插件目录与插件包仓库，采用 **Codex 官方插件格式**。
Codex（`codex plugin marketplace add leinatorX/looma-marketplace`）与 Looma
都可以直接添加本仓库作为插件来源，无需格式转换。

## 能力边界

- **插件**：由本仓库发布，一个插件可以包含一个或多个 Skill，也可以包含
  `.mcp.json`（bundled MCP）与 `hooks/`（生命周期钩子）。
- **技能**：插件内 Skill 位于 `skills/<skill-name>/SKILL.md`；用户自己的技能位于
  `~/.looma/skills`，不需要发布到市场。
- 插件不得在仓库中提交 API Key、Token 或其他密钥。

## 仓库结构

```text
looma-marketplace/
├── .agents/plugins/
│   └── marketplace.json          # Codex 官方 Marketplace 清单
├── plugins/                      # 已发布插件，每个目录一个插件
│   └── <plugin-name>/
│       ├── .codex-plugin/
│       │   └── plugin.json       # 插件清单（官方格式）
│       └── skills/
│           └── <skill-name>/
│               └── SKILL.md
├── templates/basic-plugin/       # 最小可复制模板
├── scripts/validate.py           # 零依赖校验脚本（官方格式）
└── docs/CREATE_PLUGIN.zh-CN.md   # 完整创建与发布指南
```

## 快速开始

复制模板并替换示例字段：

```powershell
Copy-Item -Recurse templates/basic-plugin plugins/my-plugin
python scripts/validate.py --plugin plugins/my-plugin
```

然后把插件条目加入 `.agents/plugins/marketplace.json`，执行完整校验：

```powershell
python scripts/validate.py --all
python -m unittest discover -s tests -p "test_*.py"
```

详细步骤、字段说明、发布规则见
[`docs/CREATE_PLUGIN.zh-CN.md`](docs/CREATE_PLUGIN.zh-CN.md)。

## 提交要求

- 插件目录名与清单 `name` 必须一致，并使用小写 kebab-case。
- 每个 Skill 必须包含合法的 `SKILL.md`，其 frontmatter 只放 `name` 和 `description`。
- Marketplace 条目必须包含 `source`、`policy.installation`、`policy.authentication` 与 `category`。
- 路径必须以 `./` 开头并保持在插件/Marketplace 根目录内；URL 不允许内嵌凭据。
- 提交前必须通过 `python scripts/validate.py --all` 与单元测试。
- 接受本仓库 [MIT License](LICENSE)；插件自身的许可证由清单 `license` 字段声明。
