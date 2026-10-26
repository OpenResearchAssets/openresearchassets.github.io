## 网站收敛规则（2026-10）

- **内容一级导航只允许 Curated / Community / Findings 三个入口，Contribute 是独立投稿 CTA**。Gallery 与 Skills / Workflows 是 Curated 的两个核心资产类型；可编辑 SVG 属于 Gallery 子板块。Quality、Principles、For AI、版权与更正均退居公共页脚。
- **单一共享导航组件**：`js/navigation.js` 负责渲染主导航、桌面投稿 CTA、移动菜单、次级页脚；各 HTML 只留 `#site-nav[data-page][data-root]`，不重建独立菜单。导航中英切换、相对路径、active 状态必须自动验证。
- **Findings 视觉与交互必须体现两级阅读**：四来源总览每组最多 3 条，强制显示简短来源解释和大字号真实指标；点击分类或“查看完整”应变成自适应宽屏阅读（移动端一列），显示所有当前采集条目及来源解释。搜索包含非预览记录并保留来源排名，中文英文、真实时间、URL 跳转/返回和横向溢出要回归测试；禁止再次把全部 56 条条目堆满首页。\n- **Findings 数据边界**：自动抓取只写 `data/findings.json`（单一 `tools/update_findings.py`，来源与频率解释见 `docs/FINDINGS.md`），不得自动改 `catalog/index.json`、社区 Issues 或已有人类编辑成果。分别明确 HF upvotes、Skills 安装量、GitHub Stars 与 Trending 周榜排序；第三方接口拒绝时透明退化为 GitHub Search 最近新项目，不能冒充官方榜单。标记快照状态与时间，不写假数据，不在浏览器里散发令牌。
- **无损调整**：不重新绘制或删除用户认可的正式资产图。保留精选 `catalog/index.json`、GitHub Issues 社区源、giscus 详情互动及旧案例链接；不要让 GitHub Stars 与本站点赞混淆。
- **页面职责**：首页主要呈现 Gallery + Skills；社区页面先展示真实投稿；发现页面先展示独立来源的趋势卡片；投稿页只保留一个主要上传 CTA 和三项必要说明。辅助工具继续存在但不占首页整块营销区域。不要把原来的长页面换成同样复杂的新一版。
- **测试约束跟随真实产品目标**：旧页面重复链接数量不作为质量指标；验证唯一导航挂载、真实资源数、中文英文、手机/平板/桌面、社区真实数据与安全过滤、导航不会遮挡。

## 选品原则：两个核心资产方向

Open Research Assets 的公开首页只突出 **Research Gallery（高审美科研配图、项目主页和可编辑图）** 与 **Research Skills / Workflows（能够完成具体任务的能力资产）**。论文方法或实验解读仅作为必要的来源、科学事实和设计参考辅助，**不再作为首页、组织主页或增长方向的主产品**；既有页面可以保留旧链接，但不主动作为产品入口推广。

Skills / Workflows **只精选两条正式路径**：

1. **高热度 / Popular**：真实 GitHub 项目、明确用途、公开仓库原始链接和可核对 Star；Star 表示社区关注，不表示实测质量。记录 `curation.track=popular`、`github_repo`、`stars_snapshot` 与 `stars_checked_on`；网页优先实时更新，失败时展示注明日期的快照。禁止为拉数量混入与科研任务无关的仓库或将整个 Skill 目录冒充某个 Skill 已经过测。
2. **实践积累 / Field notes**：团队公开使用过、具有实际产物与来源/审计记录的具体工作流，记录 `curation.track=practice`、`used_in` 与 `evidence[]`。要求能从公开仓库实际产物追溯使用记录。**代码已写好但没有运行记录、只有设想或教学示例，不能标为已实测**；公开产物证明曾应用，不等于独立效益评估。

未达到两类准入条件的原有模板、普通笔记、待验证 Skill 可保留源文件供进一步改进，但不得混进上述精选区。不擅自把用户私有仓库中的未发表论文、结果或过程迁入公开库。

**产品迭代优先级**：先精选作品/工具和证明复用收益，再做新的信息架构或组织治理；对视觉资产增加构图、科学表达、编辑性和真实尺寸可读性审美门槛。


# OpenResearchAssets · AI 维护规则 / Agent instructions

**中文为主、英文为辅。科学真实性、页面实际功能和版权是不可妥协的要求。**

## 产品北极星（所有维护 Agent 必须遵守）

OpenResearchAssets 是**面向人类与 AI 的科研全过程可复用资产库**，不是只收藏漂亮图片的图库。长期希望研究者仅提供当前科研任务、网站 URL 和所需文件/工具权限，Agent 就能自行查找、理解并选择最相关的经验、方法、工具、Skill、工作流或可编辑素材，并推动实际任务，减少重复检索、重复提示、人工返工、时间和 Token 消耗。

维护时必须优先回答：**新增资源解决了哪个科研任务？AI 何时该使用它，如何操作，哪些科学/授权边界不可越过，怎样验证收益？** 从选题、文献、方法、实验、评估、写作到投稿/传播均可收录；起步重点 AI/CV/Robotics 与科研表达，不是永久边界。衡量价值须看真实任务的质量、耗时、人工干预与 Token，而非收藏量。不得把 URL-only Agent 完成科研说成现有功能。

## 独立项目身份与长期愿景

组织与仓库归属 OpenResearchAssets，项目发展以**独立项目价值和开放社区生态**为先，不把项目描述为个人作品集。唯一公开主仓库为 `OpenResearchAssets/openresearchassets.github.io`，当前不拆双仓库。三阶段愿景（有价值的项目 → 活跃社区 → 开放科研基础设施）详见 [产品与社区方向](docs/PRODUCT_STRATEGY.md) 和原生可编辑 [SVG](assets/diagrams/community-trajectory.svg)。这些是未来目标而非已上线功能。维护贡献入口、透明审核和长期可追溯性，不以 Star 代替真实复用。修改官方链接使用组织域名，禁止重新引入旧个人站点路径。

**真实论文案例维护原则**：examples/roborender.html 是基于作者公开论文与官网逐项核对的**原创编辑解读**，非本站实证研究或独立复现。每项任务每方法 10 rollouts、8 项任务；报告均值为 Sim 10%、Sim+DR 20%、RoboRender 71%（逐任务平均 71.25%）。基准数字见 examples/roborender-results.csv，方法与版权说明见 examples/roborender-provenance.md。视频生成器使用真实 DROID/AgiBot 数据训练，不能将下游策略零样本部署误说成系统未使用任何真实机器人数据。任何更改须逐项核对一手来源、保留第三方图像权利、审阅可编辑 SVG 和真实渲染效果。未运行实验绝不称为“复现”。

## 贯通示例维护规范

[`examples/`](examples/README.md) 和 `assets/examples/` 是三个**虚构科研问题驱动的教学案例**，不是新资产索引或实证研究。更新案例必须同时维护中文与英文的完整步骤、双语 SVG、所展示的真实输入/输出边界和可复用检查标准。若加入结果，必须从实际可追溯实验获得，**不能用合成数值模拟真实科研效果**；`examples/evidence-register.csv` 的结果字段默认空白。案例页与 HTML 示例属于已实现的公开静态内容，必须加入中英、手机端和链接测试。仍以 `catalog/index.json` 为唯一结构化科研资产目录，不再建第二份目录。

1. **只宣传已存在并验证过的公开功能**。机器可读目录不等于自动执行 Agent 或语义检索。当前 Quality Critic 网页是人工勾选检查表，不是上传论文自动分析；Skill 是指导协议，不代表已有经过训练与评估的审美模型。未来研究和付费方案不得写作已上线能力。
2. 公开网站**中文默认、英文完整可切换**。新增或改动 HTML、JS 动态文本、ARIA、图片替代文字和报告时，必须维护两个语言，测试首次中文显示以及两端切换。公共文档用中文做权威版本，英文说明作为辅助。
3. 网站风格遵循 **Apple × SuperMimic**：冷白/灰、石墨黑、简洁标题、真实素材和证据；避免暖黄纸感与无意义的卡片。视觉效果必须实际渲染检查。
4. 事实正确性先于审美：严禁伪造数值、改动研究结论或将概念图冒充实验结果；编辑图形必须保留其真实含义。
5. 第三方论文图片、Logo、图标和字体只在许可明确时入库；否则只保留官方来源链接与我们原创的评论。不得在公开代码中泄漏私有稿件、实验资料、凭据或个人隐私。
6. SVG 模板应保持文字及核心图形真正可编辑，附对应预览及来源信息；修改后检查原生编辑性。
7. `catalog/index.json` 是所有科研资产的唯一权威数据源，页面与 AI 入口共同读取。不得继续维护 `data/references.js` 或平行索引。
8. 不把 Agent 自评当作客观用户质量改善；真正的质量结果需要用户/专家评价、科学上下文和最终 PDF。
9. 优先开发**对用户有直接价值的方法与工具**，Benchmark 仅用于检验有效性；研究路线可在私有研发仓库讨论，但不能把它的内部内容自动发布出来。
10. 公开仓库只维护已发布的产品信息。商业化假设、未发布设计或内部研究计划留在私人工作区。任何跨仓库发布都需人工审查授权、事实与隐私。
11. 每次更改运行 `python3 tests/check_project.py`，重要视觉/交互改动运行 `python3 tests/browser_offline_smoke.py`，包含桌面/平板/手机、中英切换、筛选、手工质量报告和导航。报告必须说明哪些测试执行、哪些没有。
12. 文档与代码均保持单一当前版本：直接维护权威文件，避免 `v2`、`final`、`latest` 等平行副本，不以长篇更新日志代替当前状态。

14. **用真实内容取代占位图**：关键案例必须提供可核实的原创设计分析图、图像级版权记录，以及事实约束/复用步骤。原始论文图与主页截图只能在具有合适授权或合法依据时入库；原创分析图放入 `assets/editorials/`，保证真正可编辑，不能只是换色的几何占位块。`catalog/index.json` 是视觉路径与正文元数据唯一手工维护源。

19. **开放投稿与可追溯署名**：所有 GitHub 用户可使用 `.github/ISSUE_TEMPLATE/submit-asset.yml` 投稿；投稿进入人工审核，不能自动公开无授权图像。新入库条目在 `catalog/index.json` 写 `submission.github`（由 Issue / PR 实际作者核验）和 `submission.added_on`（正式收录日）；作品原作者单独记录，不得与投稿人混同。历史无法核实的值保持缺失，不能用 `catalog.generated_on` 冒充逐项投稿日期。不要伪造点赞或虚构互动计数。

20. **开放互动与精选审核分离**：公开投稿 Issue 无需精选即可获得 GitHub Reaction（👍）与回复；精选资产详情已通过 GitHub Discussions 的 giscus 启用真实点赞和评论，使用 `specific` + `ora-asset:<id>` 保证同一路径 `asset.html?id=...` 下不同资产有不同讨论。`config/community.json` 保存经核实的仓库和分类 ID。Issue 与 Discussions 点赞是两个独立来源，不要伪装成统一排名/合并计数；没有授权不得伪造互动或使用 localStorage 假计数，先保持中文默认和英文可切换。

21. **Community / Curated 双层必须真实分离**：Community 通过 `community.html` + `js/community-page.js` 获取 GitHub 公开投稿 Issue（必须是 `[投稿]` + 表单结构），任何人可投稿后立即在页面看到，GitHub 登录直接给予 👍 / 评论；Curated 仍保持 Gallery + Skills 两个正式支柱，只从 `catalog/index.json` 读取人工审核入选条目。两层不是两份平行 JSON 目录；未精选不许套上已审核认证，也不许自动同步第三方图片。按 GitHub `submission.issue_url` 建立精选回链，不虚构相同点赞数。社区 API 失败不得误显示“零投稿”；空社区不放假种子。维护 `tests/community_feed_smoke.js` 验证 XSS escaping、真实计数、非投稿 Issue 与 PR 排除、精选回链、排序、双语与 API 失败，检查桌面/手机真实样式。

**English summary:** Keep the public site Chinese-first with complete English UI support. Show only implemented capabilities. Preserve scientific fidelity, licensing and privacy. Prefer useful methods over benchmark-building. Validate real rendering and interaction before release.

13. **AI 节约上下文**：首选 `catalog/manifest.json`，再沿 `catalog/entries/<id>.json` 取少量详情。唯一手工维护源是 `catalog/index.json`；编辑后运行 `python3 tools/sync_catalog.py` 并用 `--check` 核对派生文件。CI 需要同时验证静态结构与浏览器行为。

15. **真实媒体优先但逐文件确权**：允许复制 CC BY 等已有授权的第三方图片，不需要再发邮件逐项申请，但必须在 `assets/third-party/manifest.json` 登记作者、原始路径、版权依据、原图 Git blob SHA、修改状态，单条 catalog 的 rights 须可查；不要把外部图重新赋予本站 MIT 或原创 SVG 许可。来源不明者默认仅链接，合法例外需针对具体用途单独审查。

16. **版权异议与撤除是产品能力**：网站检索区、资产详情和仓库文档必须保留可见的中英双语撤除入口（Issue 模板 .github/ISSUE_TEMPLATE/asset-removal.yml），收到请求后优先核实并酌情暂停展示，再同步修改 catalog/index.json、媒体、主页详情和自动派生索引。不能把“可撤除”理解成所有第三方截图已经有许可；不要承诺无法保证的固定响应时限。公开 Issue 不收集敏感证件。

17. **视觉偏好与真实性**：用户明确不喜欢 RoboRender 方法结构图，禁止恢复为首页资产；优先参考 Depth Anything 3 官方多视角深度/空间重建概览图，并保留 RoboRender Teaser 案例。参考类卡片默认真实源站图片；若配图不是对应论文 Figure 1 或整页截图，必须明确标注真实媒体的身份。原创分析 SVG 只在详情作为辅助，不可冒充官方截图。外链媒体未自动再授权。

18. **严禁 Figure 1 / 主页截图错配**：RoboRender、RoboDojo、SuperMimic 六个核心案例的实际首图已由原论文/官网核实。论文条目必须指向相应 Figure 1，主页条目必须指向实拍网页首屏；官网其他图片不能冒充 Teaser。新增图片先核对实际像素和文字、来源、许可、Figure 编号，再绑定到目录。来源、作者、图片变更记录写入 figureIdentity 与 third-party manifest；自制解析 SVG 仅作为 analysisVisual 辅助。
