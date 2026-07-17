# AI 视频工作室（ai-video-studio）

将 AI 短视频导演工作流拆为 **6 个专职 Skill**，便于在 Looma 中按需加载。

## Skills

| 目录 | 职责 | 典型触发 |
| --- | --- | --- |
| `video-director` | 总导演编排，全流程串联 | 完整 AI 短视频方案 |
| `video-script-writer` | 剧本与创意定位 | 写剧本、钩子、旁白字幕 |
| `video-sequence-planner` | 集→序列→镜头、合法时长 | 分镜、序列表、剪辑表 |
| `video-asset-art` | 定妆/场景/道具/首尾帧图提示词 | 角色一致性、参考图规划 |
| `video-prompt-engineer` | 序列级三段式 + 多模型适配 | Grok / Veo / Seedance 等提示词 |
| `video-qc-publisher` | 质检与平台发布包装 | 检查生成结果、发布文案 |

## 默认模型

- 视频：`Grok Imagine Video`（用户指定优先）
- 图像：`GPT Image 2`（用户指定优先）

## 边界

- 本插件输出**方案与提示词**，默认不直接调用视频生成 API。
- 真正出图可衔接 `image-generator` 等执行类插件。

## 路径

```text
plugins/ai-video-studio/
```

市场启用后 Skill id 形如：`plugin:ai-video-studio:video-director`。
