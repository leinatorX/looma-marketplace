# 归藏 PPT · 网页 PPT / 配图 / 封面（guizang-ppt-skill）

> **原作者与来源**
>
> 本插件收录自歸藏（GitHub: `op7418`）的开源项目：
> <https://github.com/op7418/guizang-ppt-skill>
>
> 原项目遵循 **AGPL-3.0 License**（Copyright (C) 2026 op7418）。
> 本市场条目完整复制了原作者的 `SKILL.md`、`assets/`、`references/`、`scripts/` 与 `LICENSE`，**未对原作者任何文件做修改**。如需对工作流、模板、参考文档或校验器做修改或新增，请前往原项目提交 Issue / Pull Request。

归藏 PPT 是一个用于生成**单文件 HTML 横向翻页 PPT** 的 Claude Code / Codex Skill。每一份 deck 都是一份可以直接在浏览器打开的 HTML 文件，无需服务器、无需构建工具，并内置完整的演讲者模式、观众屏同步、备注、排练、自动翻页和现场工具。

## 双视觉系统

- **风格 A · 电子杂志 × 电子墨水**：衬线标题 + WebGL 流体背景 + 暖色主题，5 套电子墨水主题（墨水经典、靛蓝瓷、森林墨、牛皮纸、沙丘）。适合人文分享、行业观察、商业发布、需要"杂志感"的演讲。
- **风格 B · 瑞士国际主义**：Inter / Helvetica / Noto Sans SC 全程无衬线 + WebGL 极细网格 + 单一高饱和锚点色（克莱因蓝 IKB、柠檬黄、柠檬绿、安全橙），4 套主题、22 个具名版式（`S01`–`S22`）。适合事实表达、产品分析、技术汇报、数据驱动内容。

## Skill 列表

| 目录                | 职责                                                                       |
| ------------------- | -------------------------------------------------------------------------- |
| `guizang-ppt-skill` | 选风格、需求澄清、拷贝模板、填充内容、生成配图、生成演讲备注、运行校验器   |

加载后 Skill id 形如：`plugin:guizang-ppt-skill:guizang-ppt-skill`。

## 关键能力

- **双视觉系统**：电子杂志风（10 种版式）/ 瑞士风（22 个具名版式），按内容性质选用。
- **横向翻页**：键盘 ← →、滚轮、触屏、ESC 总览、内嵌宫格选页、底部圆点。
- **演讲者模式**：双窗口（当前页 / 下一页 16:9 预览）、结构化备注、计时、排练、自动翻页、激光笔、圈选、黑白屏、冻结、观众屏同步与断线恢复、演前检查。
- **主题色预设**：5 套电子墨水 + 4 套瑞士风锚点色；**不接受自定义 hex**。
- **多平台封面**：从同一份内容生成公众号 21:9、1:1 分享卡、小红书 3:4、视频号横版封面。
- **Codex 配图**：可用 GPT-M 2.0 / GPT-Image 2.0 生成人文纪实照片、信息图、流程图、UI 情景图、截图再设计，并按模板槽位比例插入。
- **校验器**：演讲者模式 / 瑞士风版式 / 演讲者运行时一致性自动校验。
- **低性能静态模式**：按 `B` 关闭 WebGL / canvas 动画，演示不依赖高性能显卡。

## 路径

```text
plugins/guizang-ppt-skill/
├── .codex-plugin/plugin.json
├── assets/icon.png
├── README.md                    # 本文件（Looma 市场视角）
└── skills/
    └── guizang-ppt-skill/       # 原作者仓库镜像
        ├── SKILL.md             # Skill 主文件
        ├── LICENSE              # AGPL-3.0 副本
        ├── README.md            # 原作者中文 README
        ├── README.en.md         # 原作者英文 README
        ├── SPONSORS.md
        ├── CONTRIBUTING.md
        ├── assets/              # 模板、动效、截图背景
        ├── references/          # 10 个组件 / 布局 / 主题 / 演讲 / 校验参考文档
        └── scripts/             # 3 个 Node 校验器
```

## 边界

- 本 Skill **不调用 Looma / Codex 之外的云服务**（无外部 API Key、无远程字体或素材）。
- 不修改用户文件，不在仓库中携带密钥。
- 不包含 `.mcp.json` 或 `hooks/`，因此不会扩大宿主能力边界。
- 模板 `template.html` / `template-swiss.html` 仅在用户明确请求时复制到目标项目，**不会**自动写入用户文件。
- 配套的 Node 校验脚本（`scripts/validate-*.mjs`）由宿主运行时按需调用；不参与宿主启动流程。

## 引用与归属

| 项              | 链接                                                                                |
| --------------- | ----------------------------------------------------------------------------------- |
| 原项目主页      | <https://github.com/op7418/guizang-ppt-skill>                                        |
| 原作者          | 歸藏 (op7418)                                                                       |
| 原项目许可      | AGPL-3.0（Copyright (C) 2026 op7418）                                               |
| 原作者 X 账号   | <https://x.com/op7418>                                                               |
| 360 安全龙虾    | <https://claw.360.cn>                                                                |
| Kimi work       | <https://www.kimi.com/zh-cn/products/kimi-work>                                      |
| Cola Skill      | <https://colaskill.com/guizang-ppt-skill/>                                           |
| 真格 Token Grant | <https://zhenfund.feishu.cn/share/base/form/shrcn1lAANF659o7EpWnxlR1VOh>           |

> 完整赞助与支持信息见原作者仓库 [`SPONSORS.md`](https://github.com/op7418/guizang-ppt-skill/blob/main/SPONSORS.md)。

## 更新策略

本插件是原作者项目的镜像快照。如原作者发布新版本（例如新增版式、新增主题色、修复校验器）：

1. 检查原仓库 `SKILL.md`、`assets/template.html`、`references/`、`scripts/` 是否有实质性变化。
2. 在本市场条目下逐文件覆盖同步，**不修改任何原作者文件**。
3. 在 `plugin.json` 的 `version` 字段按 SemVer 提升：
   - 修订链接、错别字、轻微排版：patch（`1.0.0 → 1.0.1`）。
   - 同步新增版式、主题色或参考文档：minor（`1.0.0 → 1.1.0`）。
   - 重新组织资源结构或破坏既有引用：major（`1.0.0 → 2.0.0`）。
4. 始终保持 `plugin.json` 与本 README 中的作者、仓库与许可字段指向原作者项目。
