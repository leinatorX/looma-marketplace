# Blender 智能体技能包

> **原作者与来源**
>
> 本插件收录自 EL4CTEO 的开源项目：
> <https://github.com/EL4CTEO/blender-skills>
>
> 上游版本 `1.1.0`，对应提交 `71d031dab8bc6729504d11a78cbe91945401045f`。
> 原项目遵循 **MIT License**（Copyright (c) 2026 EL4CTEO）。
>
> 本市场条目仅做 Codex 插件格式适配、Skill frontmatter 精简和 Looma MCP 工具映射；
> 22 个 Skill 的正文、脚本、参考资料与模板均来自上游。

## 能力范围

这是一个面向 Blender 5.2 LTS+ 的完整 3D 工作流技能包，包含 22 个 Skill：

```text
blender-core
blender-scene-setup
blender-hardsurface-modeling
blender-sculpting
blender-retopology-uv
blender-pbr-materials
blender-texture-baking
blender-geometry-nodes
blender-character-rigging
blender-facial-shapekeys
blender-animation
blender-game-optimization
blender-export-pipelines
blender-rendering
blender-lighting-lookdev
blender-simulation
blender-time-of-day
blender-weather-fx
blender-addon-development
blender-pipeline-automation
blender-asset-qa
blender-workflow-recipes
```

覆盖建模、雕刻、重拓扑、UV、PBR 材质、贴图烘焙、几何节点、角色绑定、表情形变、
动画、LOD 与性能优化、Unity/Unreal/Godot/Roblox/Web 导出、渲染、灯光、
昼夜与天气、物理仿真、插件开发和资产质检。

## 运行要求

- **Blender 5.2 LTS 或更高版本**。低于 5.2 时部分 API 不存在，脚本会失败。
- 可选：Blender MCP。Looma 已提供 `execute_blender_code`，短交互任务可直接使用。
- Headless 模式需要系统 Python 3.9+ 和 Blender 可执行文件；可用 `BLENDER_EXE` 指定路径。

## Looma 适配说明

- Skill frontmatter 已精简为 `name` 和 `description`，符合 Looma 的市场校验规则。
- 上游提到的 `look` 工具在当前 Blender MCP 中不存在。请使用
  `render_viewport_to_path`、`get_screenshot_of_area_as_image`，或运行
  `blender-asset-qa/scripts/review_shots.py` 生成多角度检查图。
- 上游提到的 `search_assets`、`import_asset` 若不可用，请改用用户提供的本地 HDRI，
  通过 `ShaderNodeTexEnvironment` 接入；不要假设这些工具一定存在。
- 长渲染、批量烘焙、批量转换等任务建议使用 headless
  `blender-core/scripts/run_in_blender.py`，避免实时 MCP 的 300 秒超时。
- 不要运行上游的 `install/install.ps1` 或 `install/install.sh`。市场插件已经提供
  全部 Skill，重复安装会在 `~/.agents/skills` 产生同名技能。
- `--save`、批量转换、渲染和烘焙会写入文件。执行前确认目标路径，不要覆盖用户原文件。

## 使用方式

实时模式：

```python
import sys, importlib
sys.path.insert(0, r"<插件目录>/skills/blender-asset-qa/scripts")
import qa_check
importlib.reload(qa_check)
print(qa_check.run(objects=["Chair"], profile="game"))
```

Headless 模式：

```powershell
python skills/blender-core/scripts/run_in_blender.py --which
python skills/blender-core/scripts/run_in_blender.py --blend input.blend skills/blender-asset-qa/scripts/qa_check.py -- --objects Chair --profile game
```

## 许可证

本插件遵循上游 **MIT License**，完整许可证见同目录 `LICENSE`。
