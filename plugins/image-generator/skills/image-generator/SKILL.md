---
name: image-generator
description: Looma 图片生成技能 ImageGenerator。当用户要求生成、绘制、出图、改图、重绘、图生图、局部编辑、下载或保存图片，或提到 ImageGenerator、图片生成、AI出图、生图、海报、封面、公众号配图、小红书封面、视频号封面、抖音封面、知识图谱、信息图、gpt-image-2、DALL·E 风格 /v1/images/generations 请求时使用。生成成功后必须把图片主动发送到当前会话，而不是只报告本地路径。
---

# ImageGenerator

## 目标

使用 `gpt-image-2` 兼容异步接口为 **Looma** 生成图片，并把结果 **主动发送到当前会话**，让用户在对话界面直接看到图片。

本技能的交付目标是会话可见，而不是仅落盘：

| 对比项 | 仅落盘交付 | Looma `ImageGenerator` |
| --- | --- | --- |
| 主交付物 | 写入目录并回报路径 | 把图片发回当前会话 |
| 默认落盘目录 | 项目/技能 `outputs` | `~/.looma/temp/image-generator`（仅缓存） |
| 成功标准 | 文件已保存 | 用户已在会话中看到图片 |

详细接口约束见 `references/api.md`。需要优化提示词、选择平台比例、生成中文海报或封面时，读取 `references/prompting.md`。

## 硬性要求：会话回传

生成成功后，**禁止**只回复“已保存到某某路径”。

必须立即处理 `image_paths`（或 `absolute_image_paths`）中的每张图片，并按宿主能力把图片发送到当前会话：

1. **优先**：若 Looma 提供附件/媒体发送能力，用本地绝对路径把图片作为会话附件发送。
2. **其次**：若可读取图片到上下文，读取图片文件，使宿主渲染预览。
3. **再次**：在回复中使用 Markdown 图片语法引用绝对路径，例如：

```markdown
![生成结果](C:/Users/you/.looma/temp/image-generator/image-xxx-1.png)
```

4. 仅当以上方式都不可用时，才退化为提供可点击的绝对路径，并明确说明“未能自动插入会话预览”。

补充说明：

- 本地文件是缓存，不是最终交付；**会话可见**才是交付完成。
- 可同时简要说明 `task_id`、尺寸、模型、质量；不要回显 API Key。
- 有多张图时，逐张发送/展示，不要只展示第一张。

## 快速流程

1. 确认运行环境存在：
   - `T8_BASE_URL`：图片服务 Base URL，不要包含末尾 `/v1/images/generations`。
   - `T8_API_KEY`：Bearer API Key。
   - `T8_REQUEST_TIMEOUT`：可选，请求超时秒数；默认 `600`。
2. 从用户需求提取场景、平台、主题、文字、主体、风格、尺寸、质量和参考图。需要把简短需求改写成完整视觉设计任务书时，按 `references/prompting.md` 组织提示词。
   - 如无特殊要求，提交给接口的 `prompt` 一律使用简体中文。
   - 只有用户明确要求英文提示词、目标图片必须包含英文文案、或专有英文术语不可翻译时，才在提示词中保留英文。
3. 校验尺寸：最大边不超过 `3840px`，宽高都是 `16` 的倍数，长短边比例不超过 `3:1`，总像素数在 `655360` 到 `8294400` 之间。
4. 调用 `scripts/generate_image.py`。
5. 根据返回的 `image_paths` **把图片发送到当前会话**。不要只报路径。

## 调用脚本

> Looma Skill 脚本通常最长约 60 秒。高质量出图经常更久，因此 **默认推荐异步提交 + 分次查询**。

### 推荐：先提交，再查询（适配 60 秒限制）

只提交任务、立即返回 `task_id`：

```bash
python scripts/generate_image.py \
  --prompt "一张写实风格的未来城市夜景" \
  --size 1024x1024 \
  --quality auto \
  --no-wait
```

查询已有异步任务（可重复调用，直到成功或失败）：

```bash
python scripts/generate_image.py \
  --task-id "3dad96708a77485e97ac7ef652796d7b"
```

### 短等待（仅在预计很快完成时使用）

```bash
python scripts/generate_image.py \
  --prompt "一张写实风格的未来城市夜景" \
  --size 1024x1024 \
  --quality auto \
  --timeout 50
```

若返回仍在处理中或超时，保留 `task_id`，继续用 `--task-id` 查询，**不要**重复提交同一需求。

### 带参考图

```bash
python scripts/generate_image.py \
  --prompt "保留主体，改成高级科技海报风格" \
  --image "/path/to/ref.png" \
  --size 1536x1024 \
  --quality high \
  --no-wait
```

用户在会话中上传的参考图，优先使用 Looma 附件的本地绝对路径；脚本会自动把本地文件转成 data URL。

### 自定义缓存目录（可选）

默认写入 `~/.looma/temp/image-generator`。用户明确要求保存到某目录时再指定：

```bash
python scripts/generate_image.py \
  --prompt "..." \
  --output-dir "D:/exports/posters" \
  --no-wait
```

即使指定了 `output-dir`，成功后仍必须把图片发送到会话。

## 参数选择

- 默认先走 `/v1/images/generations?async=true`；T8 失败时只允许同通道模型兜底。
- `model` 默认 `gpt-image-2`。
- `t8-fallback-model` 默认 `gpt-image-2-all`（仅 1K 档）。`--t8-fallback-size auto` 会按原始比例映射到 1K。
- 默认异步模式：提交后用 `GET /v1/images/tasks/{task_id}` 查询。
- `--no-wait` 只提交并返回 `task_id`，适合 Looma 脚本超时边界。
- `--task-id` 查询已有任务，不重新提交。
- `--sync` 使用旧同步接口，仅作兼容兜底。
- 服务端 `FAILURE` 时默认输出失败 JSON 并以 0 退出，避免宿主误判为需要重提；只有明确需要失败语义时才加 `--fail-on-task-failure`。
- `quality` 默认 `auto`；要更快用 `low`，要成品用 `high`。
- `response_format` 默认 `b64_json`；异步结果可能只返回 `url`，脚本会兼容下载。
- `size` 默认 `1024x1024`。公众号/海报等场景按 `references/prompting.md` 换算到接口合法尺寸。
- `image` 支持 URL、本地路径或 `data:image/...;base64,...`，可重复传入。

## 提示词语言

- 默认用简体中文编写最终 `prompt`。
- 技术名词、品牌名、API 名、模型名和画面中必须出现的英文原文可以保留英文。
- 如果用户明确要求英文提示词或英文画面文案，按用户要求执行。

## Looma 使用边界

- 不要把 API Key 写入 `SKILL.md`、命令参数、聊天回复或日志说明。
- 如果环境变量缺失，先提示用户配置 `T8_BASE_URL` 与 `T8_API_KEY`，不要猜测。
- 本技能不配置、不修改 MCP；不要写入 `~/.looma/mcp/servers.json`。
- 如果任务状态为 `FAILURE`，向用户报告 `task_id` 和失败原因，不要自动重新提交；只有用户明确要求重试时才重新生图。
- 如果接口返回 `{}` 或非标准结构，保留响应 JSON 并说明没有可下载图片字段。
- 如果用户要求生成违法、侵权、隐私泄露或高风险内容，拒绝该部分请求，并给出安全替代提示词。
- 图片生成失败时，先检查尺寸合法性、认证头、Base URL 拼接和服务端原始错误。
- 成功后必须完成 **会话回传**；只落盘不算完成。
