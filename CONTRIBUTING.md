## 优先级重申（2026-10-25）

**Gallery + Skills/Workflows 是两个正式产品支柱。** 外部精选以可核实的热度、任务相关性为准；亲自实践的流程必须带可公开的成果或日志证据。旧的论文解读不再作为首页入口或项目主叙事，但保持已有 URL 兼容。任何“未被验证”的 Skill 不得被标为“实践资产”；Star 计数日期必须显示清楚。禁止公开未发表项目的内部实验或私有代码。

# 贡献指南 · OpenResearchAssets / Contributing

**质量优先、科学真实、来源可追溯；中文权威，英文辅助。**

OpenResearchAssets 收录的不只是论文视觉素材，还包括科研流程、工具、可编辑文件和真正可用的经验。所有贡献需要回答：**何时使用、能学到什么、要避免什么、原始出处在哪里**。

## 欢迎的内容

- **视觉参考：** 论文 Teaser、方法图、结果图、优秀项目主页。说明具体设计决策；第三方作品默认只链接，未获许可不要上传图像或截图。
- **可编辑原创素材：** SVG、PPTX、HTML、代码与真实预览。确认版权与每个元素可原生编辑；概念模板标明非真实实验。
- **科研方法与工作流：** 文献调查、实验管理、排错、评估、写作、投稿、展示等可执行经验。明确输入、操作步骤、输出、适用范围与验证方式。
- **工具与 Skill：** 提供版本与实际使用前提。目录收录不代表我们已完成独立评估。
- **质量案例：** 经过授权的诊断和修订，包含科学约束、原始成果和最终版面复核。

## 第一次参与 / First contribution

目前接受五类贡献：论文视觉参考、项目主页案例、原创可编辑文件、科研方法与工作流、科研工具与 Skill。**首次贡献只需提交可信来源与具体使用场景，不必提前制作完整素材。** 欢迎从简单的、可核实的改进开始：通过 [Asset request](https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/new?template=asset-request.md) 推荐有明确来源与用途的研究资产；通过 [纠错模板](https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/new?template=catalog-correction.md) 报告失效链接、事实错误和说明不清；或提交一个范围清楚的 PR。较大改动建议先通过 Issue 讨论，无须一开始就提交完整素材。

建议 Issue 至少说明：解决哪个具体研究任务、源头在哪里、何时使用、能复用什么、有哪些已知限制。不是所有资产都必须以 SVG/PPTX 形式交付；方法和工作流更重视可操作步骤及验证依据。较大的 schema 改动先讨论，不直接新增平行目录。

所有社区贡献遵循相同的公开质量与授权标准。随着稳定贡献者增多，项目会按实际需要完善 Maintainer 权限与审核机制，不提前承诺自动接纳投稿。

**English:** Start with a well-sourced suggestion or focused correction; discuss substantial changes in an issue before opening a PR. Contributions are reviewed for accuracy, reuse value, and rights.

## 人人可投稿 · 开放审核

任何 GitHub 用户都可以从 [网站投稿入口](https://openresearchassets.github.io/contribute.html) 或 [资产投稿表单](https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/new?template=submit-asset.yml) 提交高审美视觉案例、研究主页、原创可编辑资产、真正有用的 Skills / Workflows。不需要 Fork、仓库写入权限或编程技能。GitHub Issue Form 自动识别提交账号；如拥有原创文件的版权，可附上 SVG/PPTX 等源文件或公开存储链接；第三方图片默认只提供原始链接。

GitHub Issue 仅表示收到投稿，**不自动发布到精选资产库**。维护者审核原创者署名、科学真实性、设计价值、许可边界与具体复用收益后，才把条目写入 `catalog/index.json`。新增正式收录条目必须记录 `submission.github` 与 `submission.added_on`，建议记录 `submission.issue_url`，按需记 `submission.original_author`。已有条目无明确的历史记录时不要补造日期或归属于某位作者。

目前公开反馈使用 GitHub Issue / PR；**站点尚未接入真正的单项点赞计数与站内评论系统**。不能把 GitHub 项目 Star 或浏览器本地计数冒充单项资产点赞。未来优先考虑 GitHub Discussions + giscus 做登录反应，详见产品迭代规则。

## 提交资产

1. **只编辑 [catalog/index.json](catalog/index.json)**：这是唯一资产登记数据源。字段参见 [docs/ASSET_SCHEMA.md](docs/ASSET_SCHEMA.md)。不要创建第二份参考目录。
2. 确保每个条目拥有稳定 \`id\`、\`stages\`、\`domains\`、\`tasks\`、\`kind\`、双语 \`description\` 和 \`keywords\`。
3. 在双语 \`applicability.use_when / learn / avoid\` 中记录能用于真实任务的经验，禁止“画得好看”等无法操作的评语。
4. 核验 \`links.source\`，如果有论文或合法可编辑源则添加相应链接。第三方截图和论文图**不能因为公开可访问就复制到仓库**。
5. 明确 \`rights\`：本人创作、第三方引用、明确许可、来源不清必须区分。原始数据、可修改矢量图和最终概念示意也要分别标注。
6. 禁止提交未公开论文、隐私、商业资料、API key 或无权再分发的素材。

## 验收

\`\`\`bash
python3 -m http.server 8000
python3 tests/check_project.py
python3 tests/browser_offline_smoke.py  # Playwright + Chromium 可用时
\`\`\`

维护者按科学真实、授权、出处、适用场景、编辑性、实际科研价值和网页双语可用性审核，不因为数量或漂亮程度自动接受。图片类改动需在真实浏览器中审查。

[提交 Issue](https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/new/choose) · [提交 PR](https://github.com/OpenResearchAssets/openresearchassets.github.io/pulls)

**English:** Contribute a traceable, task-specific research asset with bilingual metadata and actionable \`use_when / learn / avoid\` notes. Add records to the single JSON catalog. Do not repost third-party figures or screenshots without the necessary rights, and do not treat a listed skill as independently validated.

## 结构化资产维护

只编辑 `catalog/index.json`；每个条目需有明确任务、阶段、双语用例、具体可迁移经验、禁忌和可核对来源。执行 `python3 tools/sync_catalog.py` 重新生成 `catalog/manifest.json` 与 `catalog/entries/*.json`。不要手动改派生文件。提交前运行 `python3 tests/check_project.py` 及可能的浏览器测试；不得将第三方截图未经确权作为原创上传。

## 可供 AI 实际学习的优质案例

高优先级研究案例应提供真实来源支持的 `caseStudy` 四项内容（核心价值、视觉/信息结构、迁移步骤、验收限制），配套经独立设计的可编辑 `assets/editorials/<id>.svg`。SVG 用来分析可迁移的信息结构，必须标注为原创分析，不可冒充原始论文图或网站截图。若有公开的官方原图链接，可使用 `links.officialFigure`；未经图像级确权不下载第三方图到仓库。

## 权利人提出异议 / Removal requests

如权利人认为某个研究资产不适合在本站展示，可使用 [素材撤除 / 更正 Issue 模板](https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/new?template=asset-removal.yml)。需要提供站内链接、对应原始作品和问题说明。**不要在公开 Issue 里提交身份证明材料或其他私人信息。** 维护者检查后及时停止有争议的展示，并同步处理媒体文件、目录、详情与派生 AI 索引。详见 [资产政策](docs/ASSET_POLICY.md)。署名、非商业用途和“可申请撤除”并非授权替代品。
