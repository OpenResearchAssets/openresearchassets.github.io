# 科研 Skill 的真实任务试运行 / Research Skill Trials

> 2026-10-26 · 本库真实 `catalog/index.json` 数据。它是公开的可重现小规模技术验证，**不是 Skill 质量或模型性能的实验论文**。

## 已执行两项任务

| 试验 | 真实执行对象 | 输入 | 产物 | 客观验收 |
|---|---|---|---|---|
| Notebook 结构化实验 | [OpenAI Jupyter Notebook Skill](https://github.com/openai/skills/blob/main/skills/.curated/jupyter-notebook/SKILL.md) 固定版本的 **官方 `new_notebook.py` 脚手架**，随后运行我们编写的三个分析代码单元格 | 当前公开目录 JSON | 原始 / 已执行 Notebook、统计 JSON | 全新内核执行无异常；全部数值与独立 Python 结果一致 |
| 数据忠实的科研图 | [K-Dense Scientific Visualization Skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-visualization/SKILL.md) 的数据映射/零起点/可访问性流程，由本站用 Matplotlib 实现 | 同一目录 JSON | SVG、PNG、原始 CSV、来源 SHA256 | 图表数字与原始文件一致、SVG 不嵌入整张位图、标明原始来源 |

特别区分：Notebook 官方脚手架脚本**确实被执行**；完整的第三方 SKILL.md **没有被载入自动 Agent Harness**。科研图采用源 Skill 的操作原则，不等于运行它的某个自动化服务。两者均是本站撰写任务程序后的脚本化试运行。

## 可复核的实际结果

| 执行批次 | 目录记录 | Notebook 代码单元格 | Notebook 执行 | Figure 绘制 | 客观检查 | 失败 / 警告 |
|---|---:|---:|---:|---:|---:|---|
| [首次试验（GitHub Actions 40329862757）](https://github.com/OpenResearchAssets/openresearchassets.github.io/actions/runs/40329862757) | 72 | 3/3 | 811.9 ms | 211.0 ms | 7/7 通过 | 无代码异常 |
| [新增实践资产后的复验（GitHub Actions 40330477065）](https://github.com/OpenResearchAssets/openresearchassets.github.io/actions/runs/40330477065) | 73 | 3/3 | 797.7 ms | 185.5 ms | 7/7 通过 | 无代码异常 |

耗时为该次 Ubuntu GitHub runner 的程序**墙钟时间**，只覆盖 Notebook 新内核执行或绘图，不包含 pip 安装和外部源下载。两次输入不同（新增了一个记录），不能把 811.9→797.7 ms 宣称成 Skill 优化提速。具体来源 SHA256、计数和错误栈均在各次 Artifact 的 `trial-results.json`、`source-metrics.json` 中。

七项验证：① Notebook 与独立 Python 输出逐字段一致；② asset kind 计数覆盖全部记录；③ curation track 计数覆盖全部记录；④ 绘图 CSV 与原始数据一致；⑤ SVG 没有嵌入 raster `<image>`；⑥ 源代码图标明数据来源；⑦ **故意修改一行 CSV 计数后，实际验证函数拒绝篡改数据**。第七项在第二轮加强，首次只是数学自检，因此不能把首轮的负向对照描述为完整的篡改测试。

## 第三项：真实论文逐任务结果可视化

本轮还使用已经核对过公开来源的 [RoboRender 作者结果表](../../examples/roborender-results.csv) 执行科研绘图任务。输入为 8 个机器人任务、每个方法/任务 10 rollouts 的**论文作者报告成功率**，脚本把每个任务的 Sim、Sim+DR、RoboRender 三组结果保留为原始百分比。输出 `roborender-author-reported.svg`（可编辑矢量图）、`roborender-author-reported.png`（预览）、`roborender-provenance-check.json`（来源 SHA 和统计）。

[本轮真实运行日志和第三项可下载产物](https://github.com/OpenResearchAssets/openresearchassets.github.io/actions/runs/40331255218)

- 作者报告的八任务等权平均：Sim **10.00%**、Sim+DR **20.00%**、RoboRender **71.25%**。71.25% 是从作者逐项数字计算，论文展示的 71% 是四舍五入结果。
- **无独立机器人复现**；没有原始 rollout 日志，不能声称统计显著、有效置信区间或模型泛化性。本实验仅检查原始数字、等权计算、来源 SHA、矢量结构与图内出处声明。
- 新增的三项检查：① CSV SHA256 与报告一致，② 八项均标为 author-reported、结果平均与源表完全一致，③ SVG 无位图粘贴且公开标注“非独立复现、未虚构误差线”。
- 在同一运行上，前述 7 项 + 本次 3 项共 **10/10 客观检查通过**。Notebook 新内核执行 **714.8 ms**；资产分布图 **132.4 ms**；机器人结果图 **177.2 ms**，仅为这一 CI 环境的程序耗时。

## 可执行文件和复现

- [实际运行脚本](../../tools/run_skill_trials.py)（包含 Notebook 执行、绘图、来源验证与负向测试）
- [独立 GitHub Actions 运行器](../../.github/workflows/skill-trials.yml)（固定上游模板脚本版本、直接输出 ZIP Artifacts）
- [首次试验的 60 天产物](https://github.com/OpenResearchAssets/openresearchassets.github.io/actions/runs/40329862757)：Notebook 源文件与执行版、SVG/PNG/CSV、结果 JSON
- [第二次复验的 60 天产物](https://github.com/OpenResearchAssets/openresearchassets.github.io/actions/runs/40330477065)：新的 Notebook、科研图与验证结果

GitHub Actions 使用上游 OpenAI 技能的固定 Git 提交 `49f948faa9258a0c61caceaf225e179651397431` 下载 `new_notebook.py` 和 `experiment-template.ipynb`；模板辅助代码可核查，并且本次没有执行第三方复杂插件或接触私人数据。

本地复现（Python 3.11+，需要实际的上游 helper 与模板）：

```bash
python -m pip install matplotlib nbclient nbformat ipykernel pillow
python tools/run_skill_trials.py --helper /path/to/upstream-notebook/scripts/new_notebook.py
```

## 证据与未测量维度

| 维度 | 当前状态 | 是否允许声称效果提升？ |
|---|---|---|
| 输出能否复现、是否保留真实来源 | 已按预置断言复核 | 只能声称这两次给定输入通过检查 |
| 任务墙钟时间 | 记录了真实 CI 耗时 | 不能声称比无 Skill 更快 |
| 运行失败类型 | 两轮无代码异常，保留完整 CI 和 JSON 错误记录字段 | 不能声称任意任务都成功 |
| 模型 Token / API 费用 | `null`：此脚本没有可计量的 LLM API 调用 | 不能推算成本优势 |
| 相同模型、任务、预算的有/无 Skill 对照 | **没有运行** | 不能宣称 Skill 带来因果收益 |
| 机器人、论文审稿等真实领域任务 | **没有运行** | 不能推断泛化效果 |

## 下一步真正的研究式 A/B 要求

若后续要比较 Skill 对 Agent 的收益，应冻结：① 同一基座模型与解码设置，② 同一真实科研任务集和人工保留验收集，③ 工具与可见上下文权限，④ 最大墙钟时间 / 模型预算。任务和运行随机顺序配对，记录输出质量、人工修改次数、Token/美元和成功率，报告均值、方差和失败个例；优先挑选文献筛查、数据分析与图表审阅，避免把脚手架生成速度当成模型推理效率。

**English:** These are reproducible *source-guided* engineering trials. The upstream notebook scaffold actually ran and the chart was generated using documented visualization principles. We did not conduct native agent skill invocation or a controlled no-skill comparison. Program wall time is measured; model tokens and causal improvement are **not** measured.
