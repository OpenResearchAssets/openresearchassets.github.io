# P1 · 贯通式科研资产复用案例 / Worked research cases

这是一套用于**演示科研经验如何迁移**的原创公开案例，贯穿科学问题 → 方法图 → 反事实实验 → 项目主页。研究情境为**假设性的机器人视觉操作任务**：“有条件地获取第二视角，是否能在观察成本与响应延迟可控的条件下改善任务表现？”它不是已发表论文、真实系统或真实实验，所有结果均待验证。

This is an **invented teaching scenario**, not an empirical study or a deployed robot system. It illustrates the transformation of a falsifiable question into an editable method figure, a controlled evaluation protocol and a responsible project-site storyboard. **No quantitative outcomes are claimed.**

## 真实公开研究案例（作者结果可追溯）

**[RoboRender：方法 → 8 项真机实验 → 主页叙事](roborender.html)**

以作者 [官方论文与项目主页](https://robo-render.github.io/) 为主要来源，提供 [报告结果 CSV](roborender-results.csv)、[来源审计](roborender-provenance.md)、[原创可编辑方法 SVG](../assets/examples/roborender-method.svg) 与 [原创证据 SVG](../assets/examples/roborender-evidence.svg)。原论文 Figure 1 的评论缩略图保留其作者版权。作者报告均值 Sim 10%、Sim+DR 20%、RoboRender 71%；**我们未独立复现**。

**English:** [Source-grounded real-paper case](roborender.html) with author-reported outcomes, editable editorial SVGs, a transcribed CSV and explicit limits. This is separate from the hypothetical teaching scenarios below.

## 原创贯通式教学练习（虚构情境）

## 三条完整路径

| 案例 | 中文步骤 | Full English guide | 真正可编辑交付 |
|---|---|---|---|
| 01 方法图 / Method figure | [中文](method-figure.zh.md) | [English](method-figure.en.md) | [中文 SVG](../assets/examples/method-figure.zh.svg) · [English SVG](../assets/examples/method-figure.en.svg) |
| 02 实验设计 / Experimental design | [中文](experiment-design.zh.md) | [English](experiment-design.en.md) | [中文 SVG](../assets/examples/experiment-design.zh.svg) · [English SVG](../assets/examples/experiment-design.en.svg) · [可填写实验表](evidence-register.csv) |
| 03 项目主页 / Project site | [中文](project-homepage.zh.md) | [English](project-homepage.en.md) | [中文 SVG](../assets/examples/project-homepage.zh.svg) · [English SVG](../assets/examples/project-homepage.en.svg) |

**可运行项目主页示例：** [HTML 源文件](sample-project.html)（直接访问本项目的 GitHub Pages 即可浏览；概念情境、无真实结果）。

**网站版入口：** [examples.html](../examples.html) · [线上案例页](https://openresearchassets.github.io/examples.html)

## 使用边界与复用

- 内容全部由本项目原创撰写/绘制；SVG 的文本和形状保持原生可编辑，不内嵌位图，不含真实论文图、项目截图或数据。
- 方法分支、比较组和实验指标只演示一种合理的设计思路；适用性需要针对具体任务确认，不能将其当作已验证方法。
- 实验表仅登记计划，**结果栏留空**；任何统计结论、性能提升或执行成功都必须由可追溯的真实实验补齐。
- 真实使用时先替换研究问题、输入数据及约束，再更新 SVG 标签，运行真实实验、关联原始数据、检查最终输出 PDF/网页。
- 这不是新的平行资产目录：研究资产的**唯一权威索引仍是** [catalog/index.json](../catalog/index.json)。这里是围绕已有工作流的一组深入教学用例，而非新的产品功能。

## 与现有资产的关系

[方法图模板](../assets/templates/method-flow.svg) → [实验规划工作流](../workflows/experiment-planning.md) → [论点/证据图](../assets/templates/claim-evidence-map.svg) → [研究成果发布](../workflows/research-release.md)。

验收依据见 [tests/check_project.py](../tests/check_project.py) 和 [浏览器测试](../tests/browser_offline_smoke.py)；这些测试验证链接、矢量可编辑性、双语和渲染，不代表做过真实研究者效用对照实验。
