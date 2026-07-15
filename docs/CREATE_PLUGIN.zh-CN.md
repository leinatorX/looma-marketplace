# Looma 插件创建与发布指南

本文面向两类创建者：手工开发插件的用户，以及需要自动生成插件的 Agent。文中的
“必须”是市场校验与审核要求，“建议”是有助于插件稳定触发和长期维护的实践。

## 1. 先理解三个独立概念

Looma 将插件、MCP 和个人技能明确分开：

| 类型 | 来源 | 存放位置 | 管理方式 |
| --- | --- | --- | --- |
| 插件 | Looma GitHub 插件市场 | 市场下载与缓存目录 | 在“插件”选项卡启停 |
| MCP | 用户本地配置 | `~/.looma/mcp/servers.json` | 用户新增、编辑、检测、启停、删除 |
| 个人技能 | 用户自己维护 | `~/.looma/skills/<skill-name>` | 在“技能”选项卡启停 |

一个市场插件是一个可版本化的 Skill 集合。插件当前不承载 MCP Server，也不能写入
用户 MCP 配置。需要 MCP 的插件，应在文档中说明依赖，由用户自行在 Looma 界面配置；
不要随插件自动创建、修改或启用 MCP。

## 2. 环境准备

需要：

- Git；
- Python 3.9 或更高版本，仅用于运行仓库自带校验脚本；
- 一个 fork，或对本仓库具有提交权限；
- 能够编写 Markdown 和 JSON 的编辑器。

克隆仓库：

```powershell
git clone https://github.com/leinatorX/looma-marketplace.git
Set-Location looma-marketplace
```

## 3. 插件目录约定

插件必须放在 `plugins/<plugin-name>`，最小结构如下：

```text
plugins/my-plugin/
├── .looma-plugin/
│   └── plugin.json
└── skills/
    └── my-skill/
        └── SKILL.md
```

可选结构：

```text
plugins/my-plugin/
└── skills/my-skill/
    ├── SKILL.md
    ├── scripts/       # 可执行辅助脚本
    ├── references/    # 按需读取的参考资料
    └── assets/        # 模板、图标或输出资源
```

命名规则：

- 插件目录名和 Skill 目录名只能使用小写字母、数字和短横线；
- 必须以字母或数字开头和结尾；
- 长度不超过 64 个字符；
- 插件目录名、`plugin.json.name`、市场条目 `id` 三者必须相同；
- Skill 目录名与 `SKILL.md` frontmatter 中的 `name` 必须相同。

## 4. 从模板创建

复制最小模板：

```powershell
Copy-Item -Recurse templates/basic-plugin plugins/my-plugin
```

至少需要修改：

1. `plugins/my-plugin/.looma-plugin/plugin.json`；
2. Skill 目录名；
3. `SKILL.md` 的 `name`、`description` 和正文；
4. 根目录 `marketplace.json` 中的插件条目。

不要原样提交 `example-plugin`、`hello-looma`、`Your Name` 或示例 URL。

## 5. 编写插件清单

`.looma-plugin/plugin.json` 示例：

```json
{
  "$schema": "../../../schemas/plugin.schema.json",
  "schemaVersion": 1,
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "帮助用户完成某类明确任务的插件。",
  "author": {
    "name": "Your Name",
    "url": "https://github.com/your-account"
  },
  "homepage": "https://github.com/leinatorX/looma-marketplace/tree/main/plugins/my-plugin",
  "repository": "https://github.com/leinatorX/looma-marketplace",
  "license": "MIT",
  "keywords": ["productivity", "example"],
  "skills": "./skills/",
  "interface": {
    "displayName": "My Plugin",
    "shortDescription": "一句话说明插件能解决什么问题。",
    "category": "效率",
    "brandColor": "#3B82F6"
  }
}
```

字段说明：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `$schema` | 建议 | 编辑器校验地址；发布目录中的相对路径通常是 `../../../schemas/plugin.schema.json` |
| `schemaVersion` | 是 | 清单格式版本，当前固定为 `1` |
| `name` | 是 | 插件稳定标识，小写 kebab-case，发布后不要更改 |
| `version` | 是 | SemVer，例如 `1.0.0`、`1.2.0-beta.1` |
| `description` | 是 | 插件用途，建议 20–200 个字符 |
| `author` | 是 | 作者名称，可附主页 URL |
| `homepage` | 否 | 插件介绍、文档或仓库内目录地址 |
| `repository` | 是 | 源代码仓库 URL |
| `license` | 是 | SPDX 许可证标识，例如 `MIT`、`Apache-2.0` |
| `keywords` | 否 | 用于搜索，最多 10 个，单项不超过 32 个字符 |
| `skills` | 是 | Skill 根目录，当前固定为 `./skills/` |
| `interface` | 是 | 市场展示信息 |

`interface.category` 应选择稳定、易理解的中文分类，例如“开发”“效率”“写作”“设计”或
“数据”。`brandColor` 必须是六位十六进制颜色，仅用于展示，不应承载状态含义。

## 6. 编写 Skill

每个 Skill 必须有 `SKILL.md`。frontmatter 只允许 `name` 和 `description`：

```markdown
---
name: my-skill
description: 当用户需要完成某类明确任务、提到相关关键词或提供对应输入时使用。
---

# My Skill

先检查输入是否完整，再执行任务，并明确报告验证结果。
```

### 6.1 `description` 决定是否触发

描述应同时写清：

- Skill 能做什么；
- 用户在什么情况下需要它；
- 常见触发词、输入文件或目标结果；
- 必须使用该 Skill 的边界条件。

避免“这是一个有用的技能”之类无法区分场景的描述，也不要在描述中承诺 Skill 实际
做不到的事情。

### 6.2 正文写执行流程

- 使用祈使句和可验证步骤；
- 先写关键约束，再写正常流程；
- 如果流程依赖脚本，明确命令、输入、输出和失败处理；
- 较长资料放到 `references/`，并在 `SKILL.md` 中说明何时读取；
- 模板和静态资源放到 `assets/`；
- 不要在 Skill 目录额外放一份 README，使用 `SKILL.md` 作为入口；
- 不要嵌入 API Key、Cookie、Token、个人路径或真实业务数据。

### 6.3 脚本与安全

如果提供 `scripts/`：

- 默认使用确定性、非交互命令；
- 明确依赖版本和安装方式；
- 写操作限制在用户明确指定的目录；
- 删除、覆盖、发布、发送消息等高影响操作必须要求用户确认；
- 外部网络请求必须说明目标域名和用途；
- 不得修改 `~/.looma/mcp/servers.json` 或绕过 Looma 审批流程。

## 7. 添加市场条目

在根目录 `marketplace.json` 的 `plugins` 数组末尾追加：

```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "description": "帮助用户完成某类明确任务的插件。",
  "version": "1.0.0",
  "author": "Your Name",
  "category": "效率",
  "homepage": "https://github.com/leinatorX/looma-marketplace/tree/main/plugins/my-plugin",
  "manifest": "plugins/my-plugin/.looma-plugin/plugin.json",
  "files": [
    ".looma-plugin/plugin.json",
    "skills/my-skill/SKILL.md"
  ],
  "source": {
    "type": "github",
    "repository": "leinatorX/looma-marketplace",
    "ref": "main",
    "path": "plugins/my-plugin"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_USE"
  }
}
```

同时把顶层 `updatedAt` 改为当天的 `YYYY-MM-DD`。条目规则：

- `id`、`version` 必须与插件清单一致；
- `description`、`author`、`category` 是 Looma 列表当前直接展示的字段；
- `manifest` 必须指向仓库内真实文件；
- `files` 必须列出插件目录内的全部文件，路径相对于 `plugins/<plugin-id>`；客户端只下载清单中声明的文件；
- `source.repository` 使用 `owner/repository`；
- `source.ref` 当前使用 `main`，以后可改为固定 tag 以提供不可变版本；
- `policy.installation` 当前固定为 `AVAILABLE`；
- `policy.authentication` 表示外部服务何时需要用户认证，不允许在清单中保存密钥。

## 8. 本地校验

只校验一个插件：

```powershell
python scripts/validate.py --plugin plugins/my-plugin
```

校验市场索引和所有已发布插件：

```powershell
python scripts/validate.py --all
```

成功时输出 `校验通过`。脚本会检查：

- JSON 能否解析；
- 清单必填字段、命名和 SemVer；
- 插件目录、清单名称和市场 ID 是否一致；
- Skill frontmatter 和目录名称是否一致；
- 市场 ID 是否重复；
- `manifest` 是否存在；
- `files` 是否与插件目录中的真实文件完全一致；
- 市场版本是否与插件版本一致；
- 常见示例占位符是否仍然存在。

JSON Schema 也可用于编辑器实时提示：

- `schemas/plugin.schema.json`
- `schemas/marketplace.schema.json`

## 9. 本地试用

当前 Looma 会直接扫描 `~/.looma/skills` 中的个人 Skill。开发阶段可以把某个 Skill 复制
到个人目录，重启或刷新 Looma 后检查名称、描述和启停状态：

```powershell
Copy-Item -Recurse plugins/my-plugin/skills/my-skill "$HOME/.looma/skills/my-skill"
```

测试结束后由用户自行删除该测试副本。这个步骤只验证 Skill 内容，不代表市场安装流程
已经完成。市场插件的完整下载、完整性校验和安装运行时仍由 Looma 客户端版本决定。

建议至少测试：

1. 明确命中描述的请求能够触发；
2. 不相关请求不会误触发；
3. 缺少输入时能给出清楚提示；
4. 脚本失败时不会伪装成功；
5. 所有写操作都在授权范围内；
6. 输出中不泄露环境变量和密钥。

## 10. 发布 Pull Request

提交范围应只包含本插件、市场条目和必要的公共规范修订。建议提交信息：

```text
feat(插件): 发布 my-plugin 1.0.0
```

Pull Request 说明至少包含：

- 插件解决的问题和目标用户；
- 包含哪些 Skill；
- 是否使用外部网络、命令或第三方依赖；
- 是否需要用户自行配置 MCP；
- 本地验证命令和结果；
- 示例输入与预期输出；
- 安全边界和已知限制。

审核通过并合并到 `main` 后，Looma 用户刷新插件市场即可读取新条目。客户端是否能安装
并运行该插件，取决于当时 Looma 已实现的插件运行时能力；请勿在说明中超前承诺。

## 11. 更新、弃用和兼容性

- 修复错别字或非行为文档：提升 patch，例如 `1.0.0 → 1.0.1`；
- 新增兼容能力或 Skill：提升 minor，例如 `1.0.0 → 1.1.0`；
- 破坏既有调用方式：提升 major，例如 `1.0.0 → 2.0.0`；
- 同时更新 `plugin.json.version`、市场条目 `version` 和 `updatedAt`；
- 不要复用旧版本号发布不同内容；
- 弃用插件时先在说明中给迁移方案，不要直接删除导致现有用户失去来源。

## 12. Agent 创建插件的标准操作清单

Agent 应按以下顺序执行，不能跳过验证：

1. 阅读本文件、两个 JSON Schema 和 `templates/basic-plugin`；
2. 向用户确认插件目标、名称、作者、许可证和包含的 Skill；
3. 确认需求是否真的需要插件；单个私人 Skill 应优先放 `~/.looma/skills`；
4. 确认不会把 MCP 配置、API Key 或用户私有数据打包进插件；
5. 创建 `plugins/<plugin-name>`，名称使用小写 kebab-case；
6. 填写真实的 `plugin.json`，清除所有模板占位符；
7. 为每个 Skill 创建合法 `SKILL.md`，让触发描述具体可判定；
8. 仅在必要时添加 `scripts/`、`references/`、`assets/`；
9. 执行 `python scripts/validate.py --plugin plugins/<plugin-name>`；
10. 用命中和不命中场景测试每个 Skill；
11. 在 `marketplace.json` 末尾追加条目并更新 `updatedAt`；
12. 执行 `python scripts/validate.py --all`；
13. 检查 `git diff`，确保没有密钥、缓存、个人路径或无关文件；
14. 向用户报告改动、验证结果、外部依赖、风险和未验证项；
15. 只有获得用户授权后，才提交、推送或创建 Pull Request。

Agent 不得：

- 自行扩大插件权限或引入未确认的基础设施；
- 修改 Looma 公共协议来迁就单个插件；
- 在插件中提供自动写入 MCP 配置的后门；
- 把“市场已展示”描述成“运行时已安装并执行”；
- 在没有实际执行校验时声称校验通过。

## 13. 常见问题

### 一个插件可以包含多个 Skill 吗？

可以。每个 Skill 使用独立目录和 `SKILL.md`，职责应清晰，不要把互不相关的能力强行打包。

### 插件可以启动 MCP Server 吗？

不可以。插件可以在文档中说明可选的 MCP 依赖，但 MCP 配置与启停完全由用户管理。

### API Key 应放在哪里？

不要放进插件或市场仓库。需要密钥时，在 Skill 中指导用户通过对应服务的安全配置方式
提供。MCP 使用的环境变量由用户在 Looma MCP 设置中配置，并只保存在用户本地。

### 私人 Skill 必须发布为插件吗？

不需要。直接放到 `~/.looma/skills/<skill-name>` 即可。只有希望版本化分发给其他用户的
Skill 集合才适合发布为市场插件。

### 为什么市场条目和插件清单有重复字段？

市场索引用于快速展示，不需要下载完整插件；插件清单用于安装后验证和运行时发现。
校验脚本保证关键字段一致。
