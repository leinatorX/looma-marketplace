---
name: antigravity-guide
description: 指引用户了解与使用 Antigravity ACP 智能体内核、切换推理深度、以及与 Looma 画布和工具协同的技巧。
---

# Antigravity ACP 智能体执行内核

本插件为 Looma 引入了原生的 Antigravity ACP（Agent Client Protocol）执行内核与模型能力。

## 核心特性

- **多步规划流式呈现**：实时渲染 Antigravity 的任务规划卡片（Plan），包括待办事项、执行中与已完成状态。
- **动态思考折叠**：支持配置思维链推理深度（low / medium / high），在 Looma 聊天界面中平滑折叠并展示逐步推理。
- **画布原生协同**：在执行多步任务时，外部 ACP 内核可无缝调用 Looma 的本地 MCP 画布工具与记忆管理服务。
- **安全审批卡片**：所有的敏感命令与工作区写入均自动映射为 Looma 前端审批卡，由用户安全授权。

## 快速使用

1. 确保系统已安装 `agy` 命令行工具（版本 >= 1.5.1）。
2. 在终端运行 `agy login` 完成账号授权。
3. 在 Looma 会话顶部的模型选择器中，切换至 `Antigravity (ACP)` 分组下的模型即可开始交互。
