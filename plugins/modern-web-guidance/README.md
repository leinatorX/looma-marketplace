# Modern Web Guidance · 现代 Web 开发指南

> **原作者与来源**
>
> 本插件收录自 Google Chrome 团队联合 Microsoft Edge、Mozilla Firefox、MDN 团队及 Web 社区维护的开源项目：
> <https://github.com/GoogleChrome/modern-web-guidance>（源码仓库：<https://github.com/GoogleChrome/modern-web-guidance-src>）
>
> 上游版本 `1.0.1`，对应提交 `64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65`。
>
> 本市场条目仅做 Codex / Looma 清单格式对齐、Skill frontmatter 单行化适配与离线 `guides/` 兜底说明；2 个 Skill 的正文、204 篇指南及 Chrome 扩展参考资料均完整保留上游内容。

## 能力范围

本插件包含 **2 个 Skill**，覆盖现代 Web 平台开发与 Chrome 浏览器扩展开发：

| 目录 | 加载后 Skill ID | 职责 |
| --- | --- | --- |
| `modern-web-guidance` | `plugin:modern-web-guidance:modern-web-guidance` | 覆盖 262 项现代 Web 特性（CSS 布局、视图过渡、Popover/Dialog、表单与自动填充、INP 性能优化、无障碍、WebAuthn、Sanitizer、端侧内置 AI、WebMCP 等）及 204 个真实开发场景指南 |
| `chrome-extensions` | `plugin:modern-web-guidance:chrome-extensions` | 基于 Manifest V3 构建与发布 Chrome 浏览器扩展，附带 23 份扩展 API 与 Chrome Web Store 审核/上架参考文档 |

## 运行要求与离线兜底

- **CLI 检索模式（推荐）**：`modern-web-guidance` 默认通过 `npx -y modern-web-guidance@latest search/retrieve/legacy-scan` 执行本地语义检索与 BM25 匹配，需要本机安装 **Node.js >= 22.0.0**，且首次执行需联网拉取 npm 包。
- **离线 / 无 Node 22 兜底**：本插件已在 `skills/modern-web-guidance/guides/` 中内置全部 204 篇 Markdown 指南；当环境离线、受限或缺少 Node.js 22+ 时，Agent 可直接搜索并读取本地 `guides/<category>/<id>.md` 文件获取同样完整的规范与代码示例。

## Looma 适配说明

1. **Frontmatter 单行化**：Looma 市场校验脚本 `scripts/validate.py` 要求 `SKILL.md` 的 `description` 为单行字符串，已将上游两份 `SKILL.md` 中的 YAML 多行块（`|` / `>`）收敛为单行，未删减任何触发条件或指令正文。
2. **清单对齐**：在 `.codex-plugin/plugin.json` 中补齐 `brandColor`（`#4285F4`）、统一图标路径 `./assets/icon.png` 与中文展示描述，同时保留上游仓库、主页、支持地址与隐私条款链接。
3. **离线兜底补充**：在 `skills/modern-web-guidance/SKILL.md` 中补充了当 `npx` 不可用时直接读取本地 `guides/` 目录的兜底指引。

## 遥测与隐私说明

上游 `npx modern-web-guidance` CLI 默认会向 Google 上报匿名使用遥测（包括安装计数、调用 Agent 名称、检索的指南 ID 与生成的查询词，**不收集用户原始提示词**）。

如需关闭遥测，可在系统或 Shell 环境中设置：

```powershell
$env:DISABLE_TELEMETRY = "1"
```

或永久写入环境变量 / `.bashrc` / `.zshrc`：`export DISABLE_TELEMETRY=1`。若仅使用本地 `guides/` 目录读取，不触发任何遥测请求。

## 许可证

- 插件软件与配置代码遵循上游 **Apache License 2.0**，完整文本见同目录 [`LICENSE`](LICENSE)。
- `skills/modern-web-guidance/guides/` 下的指南文档遵循 **Creative Commons Attribution 4.0 International (CC-BY 4.0)**。
