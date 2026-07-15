# Looma 插件市场

这是 Looma 的公开插件目录与插件包仓库。Looma 设置页从根目录的
[`marketplace.json`](marketplace.json) 获取可用插件。

## 能力边界

- **插件**：由本仓库发布，一个插件可以包含一个或多个 Skill。
- **技能**：插件内 Skill 位于 `skills/<skill-name>/SKILL.md`；用户自己的技能位于
  `~/.looma/skills`，不需要发布到市场。
- **MCP**：不属于插件包。MCP Server 只能由用户在 Looma 设置页新增、编辑、启停和删除。
- 插件不得修改 `~/.looma/mcp/servers.json`，也不得在仓库中提交 API Key、Token 或其他密钥。

## 仓库结构

```text
looma-marketplace/
├── marketplace.json              # Looma 读取的市场索引
├── plugins/                      # 已发布插件，每个目录一个插件
│   └── <plugin-name>/
│       ├── .looma-plugin/
│       │   └── plugin.json       # 插件清单
│       └── skills/
│           └── <skill-name>/
│               └── SKILL.md
├── templates/basic-plugin/       # 最小可复制模板
├── schemas/                      # JSON Schema
├── scripts/validate.py           # 零依赖校验脚本
└── docs/CREATE_PLUGIN.zh-CN.md   # 完整创建与发布指南
```

## 快速开始

复制模板并替换示例字段：

```powershell
Copy-Item -Recurse templates/basic-plugin plugins/my-plugin
python scripts/validate.py --plugin plugins/my-plugin
```

然后把插件条目加入 `marketplace.json`，执行完整校验：

```powershell
python scripts/validate.py --all
```

详细步骤、字段说明、发布规则和 Agent 操作清单见
[`docs/CREATE_PLUGIN.zh-CN.md`](docs/CREATE_PLUGIN.zh-CN.md)。

## 提交要求

- 插件目录名、清单 `name`、市场条目 `id` 必须一致，并使用小写 kebab-case。
- 每个 Skill 必须包含合法的 `SKILL.md`，其 frontmatter 只放 `name` 和 `description`。
- 新版本必须更新插件清单和市场索引中的 `version`。
- 提交前必须通过 `python scripts/validate.py --all`。
- 接受本仓库 [MIT License](LICENSE)；插件自身的许可证由清单 `license` 字段声明。

