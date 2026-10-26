# Findings · 自动趋势发现

> 产品定位：**Curated（精选）是编辑判断，Community（社区）是用户贡献，Findings（发现）是公开数据源的自动捕捉。** 投稿 / Contribute 是独立操作按钮，不是第四类内容库。

- 页面：[findings.html](../findings.html)
- 快照：[data/findings.json](../data/findings.json)
- 唯一采集程序：[tools/update_findings.py](../tools/update_findings.py)
- 定时 GitHub Actions：[Refresh Findings](../.github/workflows/findings.yml)：每天 4 次（UTC 00:17、06:17、12:17、18:17），也可以在 Actions 手动运行。GitHub Actions 的 schedule 执行可能有延迟，不承诺分钟级实时。
- **重要：** Findings 不是本站精选，不表达论文质量、技能安全性、可复现性或工具使用效果。数据永远链接原站；不会将趋势直接写进 `catalog/index.json` 或自动晋级 Curated。

## 页面信息架构与阅读体验

- **默认总览（四个来源）**：采用两列宽屏/单列窄屏的卡片布局；每个来源仅展示 **前三条**，同时给出名称、为什么要关注、指标定义、真实采集时间、总数和“查看完整榜单”操作。不再把最多 56 条条目一次性铺开。
- **单类聚焦**：点击类别 Tab 或“查看完整”，切换为全宽独立榜单，左侧完整阅读、右侧来源与指标解释（移动端自动下移）；展示最多 14 条已采集记录，保留原始来源顺序及排名。支持“返回发现总览”，URL `?feed=papers|github|skills|workflows` 可复制打开。
- **搜索**：只搜索当前快照中已采集的记录，但**不受前三条预览限制**；清空搜索恢复卡片预览。搜索结果不代表原站完整全量搜索。
- **热度可读性**：数字必须在标题右侧形成第二视觉焦点，至少采用当前类型对应的准确单位：HF 社区票、本周新增 Stars、累计 Stars、真实安装量。榜单排名始终来自对应来源，不因关键词筛选而重新编号；不可把年度论文日期冒充近日发表。
- **可访问与回归**：中文默认/英文切换必须覆盖动态文本；测试四来源总览、单类完整页、少量快照、搜索过滤、真实指标、链接安全、无水平溢出及手机布局，并保留截图做人工布局评审。

## 数据分组和真实口径

| 榜单模块 | 原始来源 | 获取途径 | 排序 / 数字含义 |
|---|---|---|---|
| Papers | [Hugging Face Papers](https://huggingface.co/papers/trending) | 官方 `huggingface_hub.HfApi.list_daily_papers(sort="trending")` | Hugging Face 自己的 trending 排序；显示 HF 社区 upvotes，**不是论文引用数** |
| GitHub | [GitHub Trending](https://github.com/trending?since=weekly) | 读取 GitHub 官方公共 weekly 页面，并仅抽取仓库直链和可识别的页面指标 | 保留原站排序；若能识别则显示 *stars this week*。**GitHub 没有对应的官方 Trending API** |
| Skills | [Skills.sh](https://skills.sh/trending) / [GitHub Search](https://github.com/search?q=topic%3Aagent-skills&type=repositories) | 优先官方 `/api/v1/skills?view=trending`；需要授权令牌或请求失败时回退 GitHub Search | 原榜成功时显示榜单次序 + **累计安装量**；回退时显式写出“过去 60 天创建、累计 Stars 排序”，不宣称是 Skills.sh 排名 |
| Workflows | [GitHub Search](https://github.com/search?q=research+workflow&type=repositories) | 使用 GitHub Search API 搜索近期创建的 workflow 相关仓库 | **过去 60 天创建、按累计 Stars 排序**，不是 GitHub 官方 Trending 也不是 60 天 Star 增长量 |

不同来源的点赞、Stars、累计安装量不可横向相加或计算总热度榜。**页面按来源分组、独立排序，不计算自创综合评分。** Discover feed 收录不限于 AI/Robotics；它可以反映跨学科、跨类型的新资产，但不等于专业审美筛选。

## 系统边界与治理

1. **静态站点可用：** 后端由 GitHub Actions 执行，前端只请求仓库生成的 `data/findings.json`，不暴露 GitHub Token 或第三方令牌，也不在用户浏览器里逐个抓取上游平台。
2. **独立来源状态：** 每个模块记录 `source`、`url`、`fetched_at`、`metric_note`、`status`（ok / stale / unavailable / pending）及具体 `items`。失败只标记旧快照或显示不可用，**不编造榜单、排名、票数或发布日期**。
3. **数据防护：** 对仓库和论文 ID 做合法性检查，HTTPS/来源域名验证，展示时对外部标题和描述进行 HTML escaping；不自动嵌入第三方内容、截图或脚本。
4. **准入分离：** Finds 的自动抓取不能直接变成 Curated 的人工精选，也不能伪装为 Community 用户本人投稿；如果用户想推荐某个 Findings 项目，应通过 GitHub Issue 投稿后进入社区。
5. **更新范围：** 单个采集任务只允许更新 `data/findings.json`，不改公共文档、源码、精选资产。真实来源不可用时展示最近成功快照和准确日期，不伪装实时。
6. **质量和用户安全：** 外部 Skills / Workflows 可能含不安全的自动化或过度权限操作，本站只做元数据导航，不替访客执行或安装代码；安装前应自行审查源码、权限与维护状态。

**English:** Findings is a public-source trends desk, separate from editorially Curated assets and user-submitted Community entries. HF upvotes, GitHub stars and Skills installs are source-specific signals, never a combined rating. The daily GitHub Actions job produces a self-contained JSON snapshot and openly indicates fallback sources, staleness or missing data. GitHub Trending is parsed from the public page because GitHub does not offer an official Trending REST endpoint.
