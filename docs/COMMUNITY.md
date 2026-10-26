# 公开投稿、贡献者署名与社区互动

> 产品原则：面向任何 GitHub 用户开放投稿，但精选结果必须通过质量和版权审核。中文为权威说明，英文简述在文末。

## 已实现：人人可投稿

- 入口：[网站投稿](../contribute.html) / [GitHub Issue Form](https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/new?template=submit-asset.yml)。
- 不需要仓库写权限。通过 GitHub Issue Form 自动获得真实 GitHub 投稿账号和投稿时间；上传者可以在 Issue 编辑框附上自己有权发布的原创可编辑资产。
- 审核者检查作品身份、科学真实性、视觉或科研使用价值、来源与版权。只有经同意后才编辑 `catalog/index.json`，同步 AI 单项索引并在网站展示。
- 新正式收录必须写 `submission.github`（投稿人的实际 GitHub login）和 `submission.added_on`（实际进入目录的日期，YYYY-MM-DD）；建议写 `submission.issue_url` 和确认的 `submission.original_author`。投稿者和原作者不是同一个概念。
- 历史条目没有可核对的收录日或贡献者时明确保留未知，不以目录更新时间或论文年份替代。不要以新增互动机制为由稀释 Gallery 审美门槛。

## 准备就绪、需要一次仓库管理配置：点赞 / 评论

详情页已内置 giscus 的按资产 ID 独立映射，支持 GitHub 登录后的真实 Reaction 和 Discussion 评论；当前 **`config/community.json` 中 `enabled=false`，因此没有对访客宣称已启用，也不显示空的点赞按钮**。

启用步骤（由拥有组织仓库设置权限的维护者完成）：

1. 打开 [仓库 Settings](https://github.com/OpenResearchAssets/openresearchassets.github.io/settings)，在 General → Features 启用 **Discussions**。
2. 在 Discussions 创建适合精选作品的分类（例如 `Assets`，建议 Announcements 类型以控制新讨论来源）；安装 [giscus GitHub App](https://github.com/apps/giscus)，授权到 **本公开仓库**。
3. 在 [giscus.app/zh-CN](https://giscus.app/zh-CN) 选择该仓库与分类，取得真实 Repository ID（形如 `R_...`）和 Category ID（形如 `DIC_...`）。不要随意猜测。
4. 更新唯一的 `config/community.json`：`repo_id`、`category`、`category_id` 与 `enabled=true`。无需填写前端 GitHub Token；访客使用自己的 GitHub 身份授权。
5. 在至少两个不同的 `asset.html?id=<id>` 页面检查：不同资产映射到不同讨论（按 `ora-asset:<id>` 作为稳定 term）、实际反应数字、发言、双语切换及手机显示。未经真实交互验收不得宣布功能正式上线。

### 产品限制

- 社区反应与评论 **只显示在单项资产详情页**，不在 Gallery 列表堆评论或未验证的互动数字。
- 读者会被要求 GitHub 账号，互动由 GitHub Discussions 存储和管理；在 GitHub 上可以管理垃圾评论与违规内容。
- 现有前端不提供无需 GitHub 的匿名点赞、跨条目排序或主页总点赞数。Giscus 也不会提供“立即在 Gallery 卡片一键点赞”的无需额外 OAuth 机制。
- 我们优先让评论反馈包含具体的设计建议、纠错、来源补充与实际复用经验，不鼓励无实质价值的社交灌水。若评论维护成本变高，可以关闭 giscus 开关而不影响公开投稿。

**English summary:** Anyone with a GitHub account can submit an asset through an Issue Form; maintainers curate and credit the verified submitter separately from the original author. GitHub Discussions-backed per-asset reactions and comments are prepared but disabled until the repository owner enables Discussions, installs giscus, and enters verified IDs. No fabricated likes or historical submission dates.
