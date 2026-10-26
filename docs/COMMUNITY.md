# 公开投稿、贡献者署名与社区互动

> 产品原则：面向任何 GitHub 用户开放投稿，但精选结果必须通过质量和版权审核。中文为权威说明，英文简述在文末。

## 已实现：人人可投稿

- 入口：[网站投稿](../contribute.html) / [GitHub Issue Form](https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/new?template=submit-asset.yml)。
- 不需要仓库写权限。通过 GitHub Issue Form 自动获得真实 GitHub 投稿账号和投稿时间；上传者可以在 Issue 编辑框附上自己有权发布的原创可编辑资产。
- 审核者检查作品身份、科学真实性、视觉或科研使用价值、来源与版权。只有经同意后才编辑 `catalog/index.json`，同步 AI 单项索引并在网站展示。
- 新正式收录必须写 `submission.github`（投稿人的实际 GitHub login）和 `submission.added_on`（实际进入目录的日期，YYYY-MM-DD）；建议写 `submission.issue_url` 和确认的 `submission.original_author`。投稿者和原作者不是同一个概念。
- 历史条目没有可核对的收录日或贡献者时明确保留未知，不以目录更新时间或论文年份替代。不要以新增互动机制为由稀释 Gallery 审美门槛。

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
