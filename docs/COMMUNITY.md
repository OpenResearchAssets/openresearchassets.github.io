# 公开投稿、贡献者署名与社区互动

> 产品原则：面向任何 GitHub 用户开放投稿，但精选结果必须通过质量和版权审核。中文为权威说明，英文简述在文末。

## 已实现：人人可投稿

- 入口：[网站投稿](../contribute.html) / [GitHub Issue Form](https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/new?template=submit-asset.yml)。
- 不需要仓库写权限。通过 GitHub Issue Form 自动获得真实 GitHub 投稿账号和投稿时间；上传者可以在 Issue 编辑框附上自己有权发布的原创可编辑资产。
- 审核者检查作品身份、科学真实性、视觉或科研使用价值、来源与版权。只有经同意后才编辑 `catalog/index.json`，同步 AI 单项索引并在网站展示。
- 新正式收录必须写 `submission.github`（投稿人的实际 GitHub login）和 `submission.added_on`（实际进入目录的日期，YYYY-MM-DD）；建议写 `submission.issue_url` 和确认的 `submission.original_author`。投稿者和原作者不是同一个概念。
- 历史条目没有可核对的收录日或贡献者时明确保留未知，不以目录更新时间或论文年份替代。不要以新增互动机制为由稀释 Gallery 审美门槛。

## 公开 Community 与精选 Curated（已实现）

- **Community 页面：** [community.html](../community.html)，通过浏览器直接读取 GitHub REST API `/repos/OpenResearchAssets/openresearchassets.github.io/issues?state=all&per_page=100&page=N`，只收录真实公开投稿 Issue（标题 `[投稿]` 且具备表单的资产类型与原始来源字段）；排除 PR、垃圾/隐藏标签、`not_planned` 关闭状态。避免为社区再建本地 JSON 数据库。
- **公开即可互动：** 新 Issue 创建后，无需等待精选，Community 页面就可以看到真实的 GitHub 用户、创建日期、👍 Reaction 和评论数。点击点赞/评论进入对应 GitHub Issue 完成登录和操作；网站**没有伪造的本地点赞按钮**，不储存 GitHub Token。页面提供关键词、类型、最新/最多点赞/最多讨论排序。
- **来源与媒体保护：** 展示投稿标题与纯文本简述，不自动转载第三方图片、不渲染投稿 Markdown/HTML。外部原始链接标为未核实；仅允许 HTTPS/HTTP；字符串做 HTML escaping。失效、滥用或版权异议由 GitHub Issue 管理，管理者可添加 `spam`/`hidden`/`do-not-display`/`invalid` 标签或以 `not_planned` 关闭。
- **分页与计数：** 默认最多加载 5 页 GitHub Issues（每页最多 100 条 API 返回记录），页面上的数量及热门排序明确是**已加载的**记录，而不是无限全量排行；GitHub 限流或 API 故障时提示失败并提供 Issues 外链，绝不将故障当作真实零投稿。资源多到需要全量计算时再评估自动生成快照。
- **Curated 仍然独立：** 人工审核后继续只在 `catalog/index.json` 收录，增加真实 `submission.issue_url`、`submission.github` 与 `submission.added_on`。Community 页面据此显示“已入选精选”及详情链接。原始 Issue 不删除，保留署名与社区的互动记录；Issue 点赞与精选 giscus Discussions 是不同的数据源，目前不会自动相加或迁移。
- **空状态：** 截至 2026-10-26，公开仓库 API 返回零条 Issues。因此上线初期应显示欢迎投稿的真实空状态，不能伪造种子案例或数字。新投稿由 GitHub API 数据即时发现，前端刷新可看到更新（受 API 缓存与频率限制）。

## 已启用：资产详情页点赞与评论

详情页已内置 giscus 的按资产 ID 独立映射，支持 GitHub 登录后的真实 Reaction 和 Discussion 评论；现已完成仓库授权配置，**`config/community.json` 中 `enabled=true`**。配置使用真实仓库 ID `R_kgDOVVmmmQ` 和 `Assets` 分类 ID `DIC_kwDOVVmmmc4DJn9q`。访客可在已入库资产的详情页通过 GitHub 账号留下点赞与评论；新讨论首次发生真实互动时由 giscus 自动创建，尚无互动的页面可能显示无讨论状态。

已完成的接入步骤与维护说明：

1. 已在 [仓库 Settings](https://github.com/OpenResearchAssets/openresearchassets.github.io/settings) 启用 **Discussions**。
2. 已创建 Discussions `Assets` 分类（Announcement），并由组织管理员安装 [giscus GitHub App](https://github.com/apps/giscus) 授权本仓库。
3. 已从 [giscus.app/zh-CN](https://giscus.app/zh-CN) 取得确切 Repository ID 和 Category ID，没有使用占位符。
4. 已更新唯一的 `config/community.json` 并启用；**映射必须固定为 `specific` + `ora-asset:<id>`**，绝不能换为 `pathname`，否则同一个 `/asset.html` 路径可能合并不同作品的评论。无需前端 GitHub Token；访客使用自己的 GitHub 身份授权。
5. 验收：在至少两个不同的 `asset.html?id=<id>` 页面检查各自生成独立 Discussion，核实真实反应数字、GitHub 登录发言、双语切换与手机显示。配置已经启用，但**不能把静态检查冒充完成真实账户发言或浏览器端到端测试**。

### 产品限制

- **精选库内**的每份资产都可在详情页获得真实点赞与评论，与点赞数或精选日期无关。**尚未入选的社区投稿**也可以在对应的公开 GitHub Issue 上使用 👍 reaction 和回复；它不需要等待精选审核才能互动。当前网站尚未有独立的未精选投稿展示页，不能把 Issue 反应误称为网页卡片点赞，也不会自动继承进精选资产的 giscus Discussions。
- 读者会被要求 GitHub 账号，互动由 GitHub Discussions 存储和管理；在 GitHub 上可以管理垃圾评论与违规内容。
- 现有前端不提供无需 GitHub 的匿名点赞、跨条目排序或主页总点赞数。Giscus 也不会提供“立即在 Gallery 卡片一键点赞”的无需额外 OAuth 机制。
- 我们优先让评论反馈包含具体的设计建议、纠错、来源补充与实际复用经验，不鼓励无实质价值的社交灌水。若评论维护成本变高，可以关闭 giscus 开关而不影响公开投稿。

**English summary:** Anyone with GitHub can submit through Issue Forms and react/comment on pending submissions through GitHub Issues. Curated asset details now have enabled giscus reactions and comments, mapped independently by stable asset ID in GitHub Discussions. The two reaction stores are currently separate; no invented votes, combined counts, or historical publication dates. Browser end-to-end sign-in validation remains a separate step.
