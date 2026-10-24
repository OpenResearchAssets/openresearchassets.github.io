# OpenResearchAssets · 面向人类与 AI 的可复用科研资产库

**中文（默认）** · [English](README.en.md) · [在线网站](https://suchenl.github.io/OpenResearchAssets/) · [给 AI 使用](https://suchenl.github.io/OpenResearchAssets/for-agents/)

> **科研资产不只是收藏，而是可以被发现、理解与复用的经验。**  
> 科学真实性先于外观；高质量的资产需要说明其用途、来源和使用边界。

OpenResearchAssets 面向科研生命周期，整理值得学习的论文视觉案例、优秀项目主页、可编辑原创素材、研究工具与可用的工作流。**中文为主、英文为辅**；允许人类按任务搜索，也提供无需付费 API 的结构化 AI 读取入口。

## 项目目标与用途

**长期目标：让科研经验真正成为 AI 可使用的生产力。** 我们希望未来的研究者在选题、调研、方法设计、实验、评估、写作、投稿、项目主页和成果传播等任务中，只需给有网页读取能力的 AI **一个 OpenResearchAssets 网址**，AI 就能根据当前任务主动检索并理解相关资产，选择可复用的方法、实践经验、工具、Skill、可编辑素材及工作流程，在获得必要项目文件和工具权限后将其应用于实际工作，而不必反复让人类编写详细提示词或从零检索同类资料。

这不是一个单纯收藏优秀论文图、项目主页的 Gallery，也不是只有外部链接的 Awesome List。**每项资产要回答：什么时候用、为什么有价值、怎么使用或迁移、有哪些风险与约束、出处和授权是什么、最终如何验收。** 好看的 Teaser、复现经验、实验排错方法、论文叙事技巧和 Agent 工作流，只有能够帮助下一次实际科研任务，才构成我们的核心价值。

**希望减少的成本**是重复搜索、重复解释、工具试错、人工返工以及无关内容带来的时间与 Token 开销。我们将用真实任务比较资产检索正确性、最终工作质量、人工干预次数、完成耗时和 Token 成本，而不是只用收录数量或页面访问量衡量成败。

**近期建设**从 AI / CV / Robotics 领域和科研视觉表达起步，优先保证资产质量、可追溯性与可复用性，再稳步扩展科研全流程；**长期愿景不等于已上线能力**：目前提供静态检索、结构化 AI 入口和部分工具/工作流，尚不能仅凭一个网址替 AI 获得项目文件权限或自动完成整个科研流程。

## 现在已经能用

| 内容 | 实际交付 | 边界 |
|---|---|---|
| [任务搜索与多维筛选](https://suchenl.github.io/OpenResearchAssets/#references) | 双语关键词、科研阶段、领域、资产类型过滤；独立详情页 | 当前是浏览器本地筛选，不是语义向量检索 |
| [结构化资产目录](catalog/index.json) · [轻量 AI 索引](catalog/manifest.json) | **22 项**记录，含 6 个 RoboRender / RoboDojo / SuperMimic 的深入视觉分析案例 | 已收录两张带 CC BY 溯源的 RoboRender 官网视觉图，其他真实预览通过官方外链展示且不由本站再授权 |
| [AI 使用指南](for-agents/) · [llms.txt](llms.txt) | 无需认证的 JSON、Markdown 导航和来源链接 | AI 的具体执行能力取决于 Agent 文件与工具权限 |
| [原创可编辑 SVG](assets/templates/) | 5 份概念模板：Teaser、流程、结果、主页故事板、论点—证据映射 | 只展示结构和占位，不代表真实实验 |
| [人工质量自查](quality.html) | 五类审核对象、问题手工勾选和 Markdown 报告 | **不自动读取或诊断图片** |
| [质量审核 Skill](skills/quality-critic/SKILL.md) | 可供有文件读取能力的 AI 参考的审核流程 | 未经过独立专家效果验证 |

## 使用

**人类：** 在[资产目录](https://suchenl.github.io/OpenResearchAssets/#references)输入任务关键词，筛选科研阶段、领域、类型。打开独立详情查看何时适用、可学什么、注意事项和原始链接。

**AI：** 把[网站地址](https://suchenl.github.io/OpenResearchAssets/)交给有浏览/文件工具的 Agent；使用 [for-agents/README.md](for-agents/README.md) 和 [catalog/manifest.json](catalog/manifest.json) 先定位任务，再按单项 `entry` 路径获取完整资产说明。AI 不能仅凭网页就获得本地文件执行权。

本地浏览请开启静态服务器（JSON 使用 \`fetch\`，直接打开 \`file://\` 的首页可能无法加载目录）：

\`\`\`bash
python3 -m http.server 8000
python3 tools/sync_catalog.py --check
python3 tests/check_project.py
# 可选：安装 Playwright 与 Chromium 后运行
python3 tests/browser_offline_smoke.py
\`\`\`

## 版权异议与素材撤除

第三方作品归原权利人。我们为科研检索、引用导航及具体设计分析整理公开来源，网站代码、原创 SVG 与第三方图片不共享同一许可证。**如您是权利人且对某项收录或展示有异议，请[提交素材撤除或更正申请](https://github.com/Suchenl/OpenResearchAssets/issues/new?template=asset-removal.yml)**，注明站内资产 URL 与原始来源。我们会及时核实并处理。公开 Issue 中请勿提交私人证件或敏感资料；必要时可使用 [GitHub 版权投诉入口](https://github.com/contact/dmca)。

详细步骤和边界见 [资产来源与许可规范](docs/ASSET_POLICY.md)。署名、非盈利与可撤除机制不能替代必要的使用许可。

## 资产与维护原则

1. **单一数据源：** \`catalog/index.json\` 是人类网站与 Agent 共享的唯一资产目录；[资产模型](docs/ASSET_SCHEMA.md) 明确字段。
2. **真实与可溯源：** 外部资产标注原始来源；分析不能冒充论文结论，且不重发无明确权限的第三方原图。
3. **允许不同类型资源：** 独立的设计案例、可编辑文件、工具和科研经验应按使用任务组织，而不是被统一塞进视觉图库。
4. **小而精、可实际使用：** 条目讲清 \`use_when → learn → avoid\`，保持当前数据可靠性，不靠条目数量竞争。
5. **只宣传实现功能：** 公开站未提供自动 AI 质量模型、远程科研 Agent 执行器或商业服务。
6. **中英同步与真实页面验收：** 中文权威，英文完整；新增功能需要检查移动端/桌面端和真实入口。
7. **两仓库隔离：** 本仓库只放获准公开内容；私有研究、商业假设和未发表实验仅在独立私有工作区处理，不从这里自动读取或链接。

第三方内容与改造的进一步约束见 [资产政策](docs/ASSET_POLICY.md)；贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)，AI 维护流程见 [AGENTS.md](AGENTS.md)。

## 文件导航

| 位置 | 内容 |
|---|---|
| \`catalog/index.json\` | 所有资产唯一数据源：中英说明、标签、复用建议及原始链接 |
| \`index.html\` / \`asset.html\` | 任务检索与独立资产详情 |
| \`js/catalog.js\` / \`css/catalog.css\` | 资产 UI、原创建模缩略图与筛选逻辑 |
| \`for-agents/\` / \`llms.txt\` | 面向 AI 的公开自助使用入口 |
| \`assets/templates/\`、\`assets/previews/\` | 本站原创可编辑 SVG 与预览 |
| \`skills/quality-critic/\` | 可供 Agent 参考的质量审核协议 |
| \`docs/\`、\`tests/\` | 资产政策、质量标准、工程验收 |

**License**：程序和 Skill 为 MIT；原创 SVG/预览为 CC BY 4.0；第三方引用内容的版权不随链接归本仓库。详见 [LICENSE](LICENSE) 和 [资产政策](docs/ASSET_POLICY.md)。

## 真实第三方视觉资产

**官方真实图优先展示**：首页首个视觉案例更新为 Depth Anything 3 的真实官网概览图，并保留 RoboRender 的真实项目配图；已移除你不喜欢的 RoboRender 模型结构图资产。自动化验收会检查首页首卡真实 PNG 的实际加载和目录展示文案。

本站已收录 RoboRender 官网训练数据和生成质量图片，并为 Depth Anything 3 等参考型资产优先使用官方原站真实图片链接；明确区分真实官网媒体与原论文 Figure 的身份。原始 PNG 保存在 `assets/third-party/roborender/`，作者、原始仓库 blob SHA、论文 CC BY 4.0 许可依据和改动说明记录在 [第三方资产台账](assets/third-party/manifest.json)。其他项目的可见媒体不自动视为获准转载。
