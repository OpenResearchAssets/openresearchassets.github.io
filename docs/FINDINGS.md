# Findings · 自动趋势发现

> 产品定位：**Curated（精选）是编辑判断，Community（社区）是用户贡献，Findings（发现）是公开数据源的自动捕捉。** 投稿 / Contribute 是独立操作按钮，不是第四类内容库。

- 页面：[findings.html](../findings.html)
- 快照：[data/findings.json](../data/findings.json)
- 唯一采集程序：[tools/update_findings.py](../tools/update_findings.py)
- 定时 GitHub Actions：[Refresh Findings](../.github/workflows/findings.yml)：每天 4 次（UTC 00:17、06:17、12:17、18:17），也可以在 Actions 手动运行。GitHub Actions 的 schedule 执行可能有延迟，不承诺分钟级实时。
- **重要：** Findings 不是本站精选，不表达论文质量、技能安全性、可复现性或工具使用效果。数据永远链接原站；不会将趋势直接写进 `catalog/index.json` 或自动晋级 Curated。

## 中文自动翻译：默认开启（无需外部密钥）

- **当前采用 Argos Translate 离线英中翻译模型**：采集工作流自动下载并缓存开源语言包，批量翻译公开论文标题/摘要及项目、Skills、Workflow 的简介/README 摘录，结果以 `*_zh` 字段保存到 `data/findings.json`。普通读者无需 Google 账号、API Key 或浏览器端翻译请求。
- **渐进且透明**：优先翻译四个来源的首屏三条和之后的连续内容，复用原文完全一致的历史译文，单轮计算设置时间上限，未完成的内容在后续更新继续翻译；快照记录实际 `translation_coverage`，页面不得把未翻译英语冒充中文简介。
- **中文排版职责**：中文页面以中文标题和中文说明为主体；GitHub 仓库 slug、产品商标、特定技术词保留原名。暂无译文时，英文原文必须与中文解读视觉分区，并明确标记其语言。英文页面始终读取原始英文数据，不展示中文翻译。
- **质量**：离线模型是机器翻译而非人工学术解读。所有译文须有原始公开摘要或 README 可追溯，支持在站内展开英文原文核查。遇到来源文本为中英混合时，不应因为出现个别中文字符就认为全段已翻译。
- **可选 Google Cloud**：管理员也可以配置 `GOOGLE_TRANSLATE_API_KEY`，届时优先使用 Google Cloud Translation Basic API；但并非正常自动翻译的必需前提。两种引擎都只在 GitHub Actions 运行，绝不向访客暴露令牌。

## 站内完整阅读与自动翻译

- **默认总览保持四组各前三条。** 选择论文、项目、Skills 或 Workflows 后，浏览器在站内展示详细简介，每次最多加载 8 条，点击“在这里再看”继续阅读；不强制打开 Hugging Face/GitHub 的完整榜单。原站仍提供可选入口用于下载、安装、代码核验和原始出处。
- **论文最多抓取 100 条。** 使用 Hugging Face 官方 `HfApi.list_daily_papers(sort="trending", limit=100)`，保留真实摘要到约 6000 字符，并提供原论文摘要展开。可能因平台实际返回不足而少于 100 条；仅代表当前自动快照，不声称复制平台所有历史论文。原文发表日期与趋势日期分别显示，不混为一谈。
- **项目描述增强。** 对 GitHub Trending、Skills / Workflows 中各前 10 个 GitHub 仓库，尽量读取官方 GitHub README 的介绍性段落；额外内容标记为 `repository README`，不使用 LLM 虚构内容、不执行仓库代码。不成功则只显示原站已公开的 repository description；因请求配额有上限，剩余条目不承诺全文介绍。相同条目优先复用之前快照中抓取的 README，避免反复访问。
- **Google Cloud Translation（可选、付费替代引擎）**：在仓库 **Settings → Secrets and variables → Actions → New repository secret** 创建 `GOOGLE_TRANSLATE_API_KEY`，密钥来自已开启计费与 Cloud Translation API 的 Google Cloud 项目。配置后定时 GitHub Actions 以 Cloud Translation Basic v2 POST 批量翻译标题/摘要/README，写入与英文原文对应的 `title_zh` / `subtitle_zh` / `detail_zh` 字段，站点中文优先显示译文，英文页面和原始信息保持不变。浏览器不访问 Translation API，也不包含密钥。**未配置 Google 凭证时默认使用开源 Argos 离线译文**；若模型暂时不可用，则如实标记英文原文和翻译覆盖率。
- **控制成本与重用**：译文按原始源文本比对缓存；仅新增或变更字段调用翻译，每次最大约 53,000 输入字符，单批最多 12 条；HF 完整摘要译文用于生成摘要预览，避免同一段文字重复计费。Google Cloud 计费按输入字符执行，请配置预算和 API 配额。机器译文可能有专业术语错误，始终留有英文原文和链接用于校核；不将翻译冒充人工学术解读。
- **数据保护**：仅翻译已经公开的摘要与仓库介绍，不发送用户个人投稿、聊天或私人仓库内容。API 出错后保留可复用的旧翻译或者显示原文。用户无需 API Key 即可访问全部研究发现数据。

## 页面信息架构与阅读体验

- **默认总览（四个来源）**：采用两列宽屏/单列窄屏的卡片布局；每个来源仅展示 **前三条**，同时给出名称、为什么要关注、指标定义、真实采集时间、总数和“查看完整榜单”操作。不再把大量完整榜单条目一次性铺开。
- **单类聚焦**：点击类别 Tab 或“查看完整”，切换为全宽独立榜单，左侧完整阅读、右侧来源与指标解释（移动端自动下移）；站内分批展示最多 100 条论文 / 每组 14 条项目记录，保留原始来源顺序及排名。支持“返回发现总览”，URL `?feed=papers|github|skills|workflows` 可复制打开。
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
