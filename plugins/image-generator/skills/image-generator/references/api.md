# gpt-image-2 Generations 接口速查

面向 Looma `image-generator`（展示名 ImageGenerator）。来源：`https://gpt-best.apifox.cn/api-447261009`。

## 默认异步 Endpoint

```http
POST /v1/images/generations?async=true
Authorization: Bearer {{YOUR_API_KEY}}
Content-Type: application/json
```

异步提交返回：

```json
{
  "task_id": "3dad96708a77485e97ac7ef652796d7b"
}
```

查询任务：

```http
GET /v1/images/tasks/{task_id}
Authorization: Bearer {{YOUR_API_KEY}}
```

状态值：

- `IN_PROGRESS`：处理中
- `FAILURE`：失败
- `SUCCESS`：成功

成功后结果通常位于：

```json
{
  "data": {
    "status": "SUCCESS",
    "progress": "100%",
    "data": {
      "data": [
        {
          "url": "https://...",
          "b64_json": "",
          "revised_prompt": "..."
        }
      ]
    }
  }
}
```

异步查询结果可能只返回 `url`，即使提交时指定了 `response_format=b64_json`，调用方仍需兼容 URL 下载。

## 同步 Endpoint

```http
POST /v1/images/generations
Authorization: Bearer {{YOUR_API_KEY}}
Content-Type: application/json
```

实际请求地址为：

```text
{{BASE_URL}}/v1/images/generations?async=true
```

## 请求体

```json
{
  "model": "gpt-image-2",
  "prompt": "string",
  "size": "1024x1024",
  "quality": "auto",
  "response_format": "b64_json",
  "image": ["string"]
}
```

字段说明：

- `model`：模型名，默认用 `gpt-image-2`。
- `prompt`：生成提示词。
- `size`：图片尺寸，也可用 `auto`。
- `quality`：`low`、`medium`、`high`、`auto`。
- `response_format`：可选 `url` 或 `b64_json`，默认按 `b64_json` 处理，便于脚本落本地文件后回传到会话。
- `image`：参考图数组。远程 URL 可原样传入；本地路径必须先转成 `data:image/...;base64,...`，否则远端 API 读不到本机文件。脚本会自动完成本地图片转换。

## T8 模型兜底

默认主模型：

```text
gpt-image-2
```

T8 同通道兜底模型：

```text
gpt-image-2-all
```

`gpt-image-2-all` 是 ChatGPT 逆向得到的 `gpt-image-2`，当前只支持 1K 图片。脚本在 `gpt-image-2` 任务失败或提交/查询报错时，会先使用兜底模型重新提交一次 T8 任务。

默认尺寸策略为 `--t8-fallback-size auto`，会按原始 `size` 比例映射到 1K 档：

| 原始比例 | 兜底尺寸 |
|---|---:|
| 1:1 | 1024x1024 |
| 16:9 | 1024x576 |
| 9:16 | 576x1024 |
| 4:3 | 1024x768 |
| 3:4 | 768x1024 |
| 3:2 | 1024x688 |
| 2:3 | 688x1024 |

如需禁用该同通道兜底：

```bash
--t8-fallback-model none
```

## 尺寸约束

- 最大边长小于或等于 `3840px`。
- 宽和高都必须是 `16px` 的倍数。
- 长边与短边比例不得超过 `3:1`。
- 总像素数至少 `655360`，最多 `8294400`。

常用尺寸：

- `1024x1024`
- `1536x1024`
- `1024x1536`
- `2048x2048`
- `2048x1152`
- `3840x2160`
- `2160x3840`
- `auto`

## 异步 cURL 示例

```bash
curl --location "{{BASE_URL}}/v1/images/generations?async=true" \
  --header "Authorization: Bearer {{YOUR_API_KEY}}" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gpt-image-2",
    "prompt": "一张写实风格的未来城市夜景",
    "size": "1024x1024",
    "quality": "auto",
    "response_format": "b64_json",
    "image": ["data:image/png;base64,..."]
  }'
```

查询结果：

```bash
curl --location "{{BASE_URL}}/v1/images/tasks/3dad96708a77485e97ac7ef652796d7b" \
  --header "Authorization: Bearer {{YOUR_API_KEY}}" \
  --header "Content-Type: application/json"
```

## 响应兼容性

文档页面的返回示例只给出 `{}`，因此调用方需要兼容以下情况：

- `data[].b64_json`
- `data[].url`
- 其它平台自定义字段
- 空对象或错误对象

如果无法识别图片字段，保留完整响应供排查。

## Looma 超时与轮询

Looma Skill 脚本默认最长运行约 60 秒。高质量生成可能超过该限制。

推荐策略：

1. 先用 `--no-wait` 提交，快速拿到 `task_id`；
2. 再用 `--task-id` 分次查询，直到 `SUCCESS` 或 `FAILURE`；
3. 成功后根据 `image_paths` 把图片发回当前会话。

也可单次使用 `--timeout 50` 做短等待；若未完成，继续用 `--task-id` 查询，不要重新提交。

## 失败与重试策略

服务端任务返回 `FAILURE` 时，脚本默认把失败作为已处理结果输出，退出码仍为 `0`，避免宿主把命令失败误判为需要重新提交。

只有在显式传入 `--fail-on-task-failure` 时，任务状态为 `FAILURE` 才会使用非 `0` 退出码。

遇到 `FAILURE` 后，应先报告 `task_id` 和失败原因，不要自动重试；只有用户明确要求重试时才重新提交生图请求。
