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

## 经过分析的案例与可编辑封面

已完成案例可填写 `visual: {src, kind, alt:{zh,en}, label:{zh,en}}`。`src` 必须指向 `assets/editorials/<id>.svg` 的本站**原创分析图**；它是对应项目的图文组织学习工具，不是原论文 Figure 或官网截图。`rights.preview=authored-analysis-svg` 记录其性质，媒体版权与来源仍在 `rights` 与 `links` 中注明。另有官方原图链接时可使用 `links.officialFigure`，链接本身不等于本仓库获得了再分发许可。

六个核心案例还包含 `caseStudy`：`insight`（为何值得学习）、`composition`（信息/视觉拆解）、`reuseSteps`（如何迁移到自己的研究）、`verification`（事实、评估与授权检查），以上均提供中英文内容。这使 Agent 不只是看到图，还能回答“怎么用，怎么验证”。独立条目 JSON 与 manifest 仍从 `catalog/index.json` 自动生成。

## 统一视觉封面与精读密度

所有卡片采用 5:3 可响应的封面区域：重点论文/网站条目显示 6 个本站独立 SVG 分析图；可编辑模板显示原生 SVG 内容；外部资源、Workflow、Skill 根据自身关键词和实践经验生成有内容的结构封面，不能把它冒充原作者图片。重点案例页面避免重复渲染 `caseStudy` 与 `applicability.learn/avoid` 的同义内容；数据文件完整保留，供 AI 单项读取。

## 第三方真实图片记录（已启用）

许可允许时可以收录官方真实图片。此类条目的 `visual.kind=licensed-paper-figure`，`visual.src` 指向 `assets/third-party/<project>/<file>.png`，`rights.preview=third-party-cc-by-4.0`；必填 `rights.license_url`、`rights.licensing_evidence`、`rights.attribution`、`rights.original_file`、`rights.original_blob_sha` 和 `rights.modifications`。第三方文件独立见 `assets/third-party/manifest.json`，不继承本站 MIT/原创 SVG 的统一版权声明。

真实图与本站原创结构分析图为**两种独立资产**，不能将方法结构图误写成论文 Teaser。无需许可的情况仅限拥有适用合法例外或其他授权，必须描述具体依据，而不是把所有互联网图片一概认定为“合理使用”。

## 真实来源图优先

参考型条目支持 `visual.kind=external-reference-image` 和官方 HTTPS `src`；这是对原站媒体的直接链接，不代表本站获得再授权。优先展示原始素材，但仍需在双语 `visual.alt` 中说明它是论文主图、官网配图、作者 portfolio 封面还是截图，不能混称。源图载入失败时显示可见提示，详情保留作者/主页链接。

## Figure 1 / 主页首屏：强制核实原图身份

核心视觉条目的主封面不再允许用其他“同项目官方配图”冒充：`visual.kind=verified-paper-figure` 必须是真正 Figure 1（或在 title 中准确给出论文 Figure 编号）；`visual.kind=verified-site-screenshot` 必须是真实浏览器截取的源站首屏。`figureIdentity` 的 source/type/name/date/credit/modifications 均为必填元数据，第三方低分辨率引用截图不等于自动拥有可再分发许可。对原图有疑义可按权利人撤除机制响应。六案例当前均有内容专属的原图 JPG，同时保留 `analysisVisual` 为原创结构解析辅助。

## 精选 Skill / Workflow 双轨资格

- `curation.track="popular"`：仓库级 GitHub Star 快照（`stars_snapshot` 整数、`stars_checked_on` YYYY-MM-DD、`github_repo` 精确 owner/name），以及能力类型 `type`（skill / tool / workflow）；每次人工编辑检查一手仓库。网站可尝试实时刷新 Star，失败显示快照及日期。Star 不代表实际效果。
- `curation.track="practice"`：实际在本项目或获准公开项目中使用，至少一个可访问的 `evidence[]` 路径，包含产物或验证记录。`verification` 应区分“公开项目实践”与“第三方独立实验验证”，不能混淆。
- 尚未实践的原创 Skill 或普通流程不应被显示成“我们用过”。目录允许保留未精选条目，主站只展示双轨审核过的精选项。
- 所有数据仍从 `catalog/index.json` 生成，不得另建 Star 热度或 Workflow 的第二份事实源。

## Gallery 严选：具体图像而非整篇论文（2026-10-25）

新入选 Gallery 作品必须核实 **作者项目页实际使用的图像**及作者原仓库的精确文件路径，并记录 `figureIdentity.type=project-website-figure` 和原始文件名；此类官网图不自动等于论文 Figure 1，也不等于本站拥有原图许可。优先外链原图，不复制第三方资源到本仓库。写明为什么**构图、层次、配色、真实视觉实例与信息密度**值得借鉴，以及从中能迁移的表达模式和不能复用的具体科学内容。普通拥挤 Method 图不因论文著名而自动入库。示例质量门槛见 README 的本轮新增精选清单。

## Teaser、Results、Ablation、Project Site 类型边界

2026-10-25 起，视觉参考可以在 `curation.visual_category` 填 `teaser`、`results`、`ablation` 或 `project-site`。类别必须由官网用途及真实原始素材支撑：

- Teaser：以最短路径表达研究问题或核心展示；不能把所有结果拼图都标成 Teaser。
- Results：相同输入和评价口径下的结果对照，特别适合对齐表格、局部放大和区域编辑。
- Ablation：必须是作者明确的删减组件、控制变量实验，不能把基线对比或失败示例自动称为消融。
- Project Site：评价站点导航、交互和证据路径；如果预览只是官网某张图或滑杆端点，`figureIdentity.type=project-website-media`，**不得标为实际首屏截图**。
- 第三方媒体默认只存准确的外链，保留作者原图版权，不重新分发为本站原生 SVG。
