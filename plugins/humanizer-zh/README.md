# Humanizer-zh · 中文去 AI 味

> **原作者与来源**
>
> 本插件收录自原作者歸藏（GitHub: `op7418`）的开源项目：
> <https://github.com/op7418/Humanizer-zh>
>
> 原项目遵循 **MIT License**（Copyright (c) 2026 歸藏）。
> 本市场条目**仅对 frontmatter 进行了格式适配**，正文、24 类模式清单、示例与说明均完整保留原作者内容。如需对模式本身做修改或新增，请前往原项目提交 Issue / Pull Request。

Humanizer-zh 是一个用于去除文本中 AI 生成痕迹的中文 Skill，帮助你将 AI 生成的内容改写得更自然、更像人类书写。本仓库条目将其封装为 Looma 插件，遵循 **Codex 官方插件格式**，与 `image-generator`、`emergency-studio` 等其他插件采用一致的目录与清单结构。

## 适用场景

- 编辑和审阅 AI 生成的内容。
- 提升公众号、博客、专栏、newsletter、邮件的人性化程度。
- 学习识别 AI 写作的常见模式。
- 处理"中译中"修订，重点清理翻译腔、机械对照句、空泛大词、口号式收束。

## Skill

| 目录            | 职责                                       |
| --------------- | ------------------------------------------ |
| `humanizer-zh` | 识别并改写 24 类 AI 写作痕迹，注入人味与节奏 |

加载后 Skill id 形如：`plugin:humanizer-zh:humanizer-zh`。

## 24 类 AI 写作痕迹速览

- **内容模式（6）**：夸大的象征意义、过度强调媒体报道、以 -ing 结尾的肤浅分析、宣传性语言、模糊归因、"挑战与未来展望"提纲。
- **语言和语法模式（6）**：AI 高频词、系动词回避、否定式排比、三段式法则、同义词循环、虚假范围。
- **风格模式（6）**：破折号过度使用、粗体过度使用、内联标题列表、标题大写、表情符号、弯引号。
- **交流与填充（6）**：协作交流痕迹、知识截止免责声明、谄媚语气、填充短语、过度限定、通用积极结论。

完整定义、警告词、示例和改写策略见 `skills/humanizer-zh/SKILL.md`。

## 路径

```text
plugins/humanizer-zh/
├── .codex-plugin/plugin.json
├── assets/icon.png
├── LICENSE                  # 原作者 MIT 许可副本
├── README.md                # 本文件
└── skills/
    └── humanizer-zh/
        └── SKILL.md
```

## 边界

- 本 Skill **不调用任何外部网络或 API**，所有改写由宿主模型完成。
- 不修改用户文件，不在仓库中携带 API Key、Token 或用户私有数据。
- 不包含 `.mcp.json` 或 `hooks/`，因此不会扩大宿主能力边界。

## 引用与归属

| 项           | 链接                                                                            |
| ------------ | ------------------------------------------------------------------------------- |
| 原项目主页   | <https://github.com/op7418/Humanizer-zh>                                        |
| 原作者       | 歸藏 (op7418)                                                                   |
| 原项目许可   | MIT（Copyright (c) 2026 歸藏）                                                  |
| 原始英文版   | <https://github.com/blader/humanizer/tree/main>                                 |
| 实用工具参考 | <https://github.com/hardikpandya/stop-slop>                                     |
| 资料基础     | <https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing>                   |

## 更新策略

本插件的内容是原作者项目的镜像快照。如原作者发布新版本（例如新增模式、修改示例），市场维护者将按以下顺序处理：

1. 检查原仓库的 `SKILL.md` 是否有实质性变化。
2. 同步正文到 `skills/humanizer-zh/SKILL.md`，保留所有原作者标注。
3. 在 `plugin.json` 的 `version` 字段按 SemVer 提升：
   - 修订错别字、链接、示例排版：patch（`1.0.0 → 1.0.1`）。
   - 同步新增模式或调整分类：minor（`1.0.0 → 1.1.0`）。
   - 重新组织正文结构或破坏既有引用：major（`1.0.0 → 2.0.0`）。
4. 始终保持 README 与 `plugin.json` 中的作者、仓库与许可字段指向原作者项目。
