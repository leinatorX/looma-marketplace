# 归藏 Product Video · 产品宣传片

> **原作者与来源**
>
> 本插件收录自原作者歸藏（GitHub: `op7418`）的开源项目：
> <https://github.com/op7418/guizang-product-video-skill>
>
> 上游快照：`18842e0`（2026-10-09）。本市场条目为**完整镜像**，正文、脚本、参考文档与素材均未改动；唯一修改是移除原作者 `SKILL.md` frontmatter 中的 `license` 字段（Looma / Codex 插件格式只接受 `name` 与 `description`）。如需修改 Skill 本身，请前往原项目提交 Issue / Pull Request。

用真实业务组件讲清楚一个软件产品或一次更新，让画面、文案和声音一起推进。视觉手法从产品自身推导，不套模板。

## 适用场景

- 软件版本更新宣传片、release notes video、changelog promo。
- 产品演示片、功能讲解片，配合真实界面与交互录制。
- 需要配乐、音效与工程可复现的完整视频交付。

## Skill

加载后 Skill id 形如：`plugin:guizang-product-video-skill:guizang-product-video-skill`。

## 路径

```text
plugins/guizang-product-video-skill/
├── .codex-plugin/plugin.json
├── README.md                      # 本文件
├── assets/icon.png                # 市场图标（96x96）
└── skills/guizang-product-video-skill/
    ├── SKILL.md                   # 主流程与硬约束
    ├── README.md                  # 原作者上游文档
    ├── LICENSE                    # GNU AGPL-3.0
    ├── COMMERCIAL_LICENSING.md
    ├── references/                # 12 篇参考文档
    ├── scripts/                   # 初始化、环境检查、混音、交付检查
    ├── tests/
    ├── assets/
    │   ├── starter/               # 起步工程（HyperFrames / 浏览器引擎）
    │   ├── fx-lab/                # 可改写的动效样例
    │   ├── fallback/              # CodePilot 默认样式（BSL-1.1）
    │   └── audio/                 # 原创配乐示例与 11 个内置 WAV 音效
    └── extras/news-video/         # 新闻视频叠加层扩展
```

## 边界

- 需要本机具备 Python 3、FFmpeg 与 Node.js；浏览器引擎另需 Playwright 等依赖，缺失项由 `scripts/check_environment.py` 报告。
- 会在**独立的视频工程目录**中工作，不修改被宣传产品的代码与依赖。
- 不含 `.mcp.json` 或 `hooks/`，不携带 API Key、Token 或用户私有数据。

## 许可（重要：本插件为混合许可）

本插件**不是单一许可**，分发或再分发时必须同时核对以下条款：

- **主许可**：工作流、文档、脚本、起步工程与原创音频资产适用 [GNU AGPL-3.0](skills/guizang-product-video-skill/LICENSE)。
- **单独授权**：`skills/guizang-product-video-skill/assets/fallback/` 中的 CodePilot 改编组件与样式适用 [Business Source License 1.1](skills/guizang-product-video-skill/assets/fallback/LICENSE.CodePilot)，其 Additional Use Grant 禁止商业用途，Change Date 为 2029-03-16。
- **不得**将本插件整体宣称为 MIT 或"可无限制商用"。

本市场为非商业分发，属BSL Additional Use Grant 明确排除的非营利使用。闭源集成、白标、平台内置等超出开源分发的用法，请按上游 [COMMERCIAL_LICENSING.md](skills/guizang-product-video-skill/COMMERCIAL_LICENSING.md) 与作者协商。

## 更新策略

本插件是上游的镜像快照。同步时按以下顺序处理：

1. 比对上游 `SKILL.md`、`references/`、`scripts/`、`assets/` 是否有实质性变化。
2. 同步文件，保留全部许可文件（`LICENSE`、`COMMERCIAL_LICENSING.md`、`assets/fallback/LICENSE.CodePilot`、`assets/*/SOURCE.md`）。
3. 重新套用 frontmatter 适配（移除 `license` 字段，保留 `name` 与 `description`）。
4. `version` 按 SemVer 提升：修订错别字与链接为 patch，同步新增参考文档或脚本为 minor，重新组织主流程为 major。
5. `plugin.json` 中的作者、仓库、许可与 homepage 字段始终指向原作者。

## 已知差异

- 上游根目录的 `agents/openai.yaml` 是 Claude Code 的界面定义，Codex 侧改用 `.codex-plugin/plugin.json` 的 `interface` 字段，故未收录。
- `assets/icon.png` 是本市场自建的图标（非上游资产），沿用作者品牌色 `#002FA7` 与歸藏系列插件的视觉语言：白色 16:9 画面、播放三角、黄色播放进度，与 `guizang-ppt-skill` 图标同源。上游未提供可复用的插件图标，故未直接复用 `assets/readme/` 或 CodePilot 品牌素材。
