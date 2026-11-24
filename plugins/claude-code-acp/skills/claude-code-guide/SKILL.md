---
name: claude-code-guide
description: 指引用户安装配置与使用 Claude Code ACP 智能体内核、切换模型与思考深度、以及在 Looma 工作区和画布中协同工作。
---

# Claude Code ACP 智能体执行内核

本插件通过官方 ACP 适配器 `@agentclientprotocol/claude-agent-acp` 将 Anthropic Claude Code 接入 Looma 桌面端。

## 核心特性

- **原生模型与思考档位**：握手后自动同步当前账号可用的 Claude 模型（如 Opus / Sonnet / Haiku）及思考深度档位（low / medium / high / max），并可在「设置 → 运行时」中自定义前台显示哪些模型。
- **权限模式与安全审批**：自动对接 Claude Code 的 `default` / `acceptEdits` / `bypassPermissions` / `plan` 模式，所有需授权的工具调用均映射为 Looma 审批卡。
- **跨内核无缝续聊**：支持在同一会话内于 Codex、Antigravity ACP 与 Claude Code ACP 之间自由切换并自动承接上下文。
- **画布与记忆协同**：自动注入 Looma 本地 MCP 画布与记忆服务，直接在多步任务中操作画布和持久化知识。

## 快速使用

1. 安装官方适配器：`npm install -g @agentclientprotocol/claude-agent-acp`（需 Node.js >= 22）。
2. 确保本机 Claude 账号已登录（在设置页点击「终端登录」或运行 `claude auth login`），或已配置 `ANTHROPIC_API_KEY`。
3. 在 Looma 模型选择器中切换至 `Claude Code (ACP)` 分组下的任意模型即可开始对话。
