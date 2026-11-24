# Claude Code ACP 插件

官方 Claude Code ACP 智能体执行内核插件，通过 `@agentclientprotocol/claude-agent-acp` 将 Anthropic Claude Code 接入 Looma。

## 功能介绍

- 自动发现本机已安装的 `claude-agent-acp` 命令行适配器
- 离线核验本机 Claude 登录态（支持 Claude 订阅账号、`ANTHROPIC_API_KEY` 及自定义网关）
- 在 Looma 模型选择器中提供 `Claude Code (ACP)` 分组，并在启动/会话握手后同步账号实际可用模型与思考档位
- 支持 Plan 模式、工具调用安全审批、多步思考折叠与 Looma 本地画布/记忆 MCP 联动

## 前置准备

```bash
npm install -g @agentclientprotocol/claude-agent-acp
```

若尚未登录 Claude 账号，可在设置页「运行时 → ACP 智能体运行时」点击「终端登录」，或在终端执行 `claude-agent-acp --cli auth login --claudeai`。

## 协议与授权

MIT License.
