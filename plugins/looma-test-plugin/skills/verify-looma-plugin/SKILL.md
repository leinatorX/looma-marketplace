---
name: verify-looma-plugin
description: 验证 Looma 市场插件是否已成功加载并能被 Agent 触发。当用户提到“测试插件”“验证插件”“检查 Looma 插件”或要求确认插件链路时使用。
---

# 验证 Looma 插件

普通验证时直接返回以下结果，不访问网络，也不修改任何文件：

```text
Looma 测试插件已成功触发
plugin: looma-test-plugin
skill: verify-looma-plugin
status: success
```

如果用户要求验证 Skill 脚本运行时、执行链路或审批流程，调用 `scripts/verify.py`。该脚本无网络访问和文件写入，只向标准输出返回 JSON；Looma 仍须按当前审批模式决定是否执行。

如果用户要求继续执行其他操作，先完成上述验证，再按用户请求正常处理。
