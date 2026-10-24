# OpenResearchAssets 资产模型与收录要求

> 权威数据源：[catalog/index.json](../catalog/index.json)。人类网页与 AI 入口都直接读取它；不维护另一份平行参考目录。

## 核心目标

一个条目不仅要回答“这是什么”，还要回答：

- **何时使用？** 当前研究任务适合什么资源。
- **可以学到什么？** 可迁移的设计或操作经验，而不是泛泛赞美。
- **需要避免什么？** 科学真实性、适用范围、版权及实现限制。
- **从哪里来？** 官方链接、原文、原作者或可编辑源；不要冒充原创。
- **可以直接做什么？** 有可编辑源就指明路径；没有则明确为参考。

## 结构

目录使用 UTF-8 JSON，当前版本 \`schema_version: 1.0.0\`。每条 \`entries[]\` 包括：

| 字段 | 内容 | 规则 |
|---|---|---|
| \`id\` | 稳定的小写连字符 ID | 不能因标题改变而更换 |
| \`title\` | 明确资源名与具体组成部分 | 一篇论文的 Teaser 和主页可以分为关联的两项 |
| \`kind\` | 资产类型 | 使用 \`facets.kinds\` 中已定义的类型 |
| \`stages[]\` | 科研阶段 | 使用 \`facets.stages\` 的标签 |
| \`domains[]\` | 适用领域 | 使用 \`facets.domains\` 的标签 |
| \`tasks[]\` | 细粒度使用任务 | 可逐步扩展；使用稳定英文 slug |
| \`description\` | 具体价值概述 | \`{zh,en}\` 双语 |
| \`keywords\` | 中英关键词及别名 | \`{zh:[...], en:[...]}\` |
| \`applicability\` | \`use_when\`、\`learn\`、\`avoid\` | 每个都是双语字符串数组；填写可执行要点 |
| \`links.source\` | 原始来源 URL | 必填，使用可验证的 HTTPS |
| \`links.paper\` | 论文链接 | 有原论文时填写 |
| \`links.editable\` | 原创可编辑源/合法授权文件 | 没有时不要伪造 |
| \`rights\` | \`reuse\`、\`preview\`、\`third_party_media\` | 外部来源默认 \`reference-only\` |
| \`parent\` | 相关条目 ID | 可选，用于 Teaser ↔ 项目主页跳转 |
| \`previewStyle\` | 原创结构图的样式关键词 | 网站用自身图形示意，不把它叫官方截图 |

中文是说明的权威版本；英文为检索与国际读者服务，不得缺失。

## 收录与版权边界

- 第三方论文图、主页截图、Logo、字体及视频**不因为可访问而成为可再分发素材**。公开仓库目前只保留链接与原创示意，待逐项查证后才能增加正式缩略图。
- 经授权展示真实图时，额外记录图像级来源、许可、展示用途和版本，并做好撤稿与下架路径。
- 不能把结构示意说成原论文图。原创模板中的数值均为概念占位，不代表任何真实结果。
- 新增资源需要准确的事实、清楚的用途和当前可访问来源。绝不以没有验证的 AI 能力为卖点。

## 页面与机器消费

- 面向人的入口：[首页检索](../index.html#references)、[独立详情](../asset.html?id=supermimic-site)。
- 面向 AI 的入口：[for-agents/](../for-agents/) 和 [llms.txt](../llms.txt)，机器读取 [catalog/index.json](../catalog/index.json)。
- Agent 尽量只读取最相关的几个条目，不必抓取全站。使用前核实源文件权限及真实论文条件。
- 当前是静态 JSON 加浏览器端筛选，不是语义向量检索或在线 Agent 执行器。全文关键词包含中文、英文和用例字段。

## 修改验收

\`\`\`bash
python3 -m http.server 8000
python3 tests/check_project.py
python3 tests/browser_offline_smoke.py   # Playwright 与 Chromium 可用时
\`\`\`

修改资产记录只更新 \`catalog/index.json\`，并让所有页面从此文件读取。不要重新创建 \`data/references.js\` 或同名目录的不同版本。

## 已实现的轻量 AI 读取流程

唯一**手工维护**的事实源是 `catalog/index.json`。运行 `python3 tools/sync_catalog.py` 自动生成 `catalog/manifest.json`（检索摘要）和 `catalog/entries/<id>.json`（单项全部内容）。Agent 应先读取轻量索引，再按照条目中的 `entry` 路径读取少量相关文件，以减少不必要的上下文。禁止直接修改生成文件；执行 `python3 tools/sync_catalog.py --check` 验证一致性。网站检索当前仍使用完整目录与静态前端筛选，并不是已部署的语义数据库。
