# 资产来源、许可与隐私规范 / Asset Policy

## 内容及版权

| 内容 | 当前许可/边界 |
|---|---|
| `assets/templates/*.svg` 原创可编辑模板 | CC BY 4.0，署名 OpenResearchAssets contributors，标注原仓库链接 |
| `assets/previews/*` 原创模板预览 | 同对应 SVG 的 CC BY 4.0 |
| `assets/editorials/*.svg` 原创案例分析图 | 本项目独立绘制的研究方法/信息结构分析，CC BY 4.0；不包含原作者论文图片或网站截图。复用时请注明 OpenResearchAssets 和研究原始来源 |
| `assets/third-party/{roborender,robodojo,supermimic}/*.jpg` | 三份真实论文 Figure 1 / 官方总览图缩略预览，以及三份 2026-10-25 实拍浏览器主页首屏截图；逐文件注明作者、准确图像类型、来源与裁切/缩放。RoboRender 论文 Figure 1 适用原论文 CC BY 4.0（需署名和注明修改），其余图像版权保留给权利人，本站作为具体评论/研究视觉参考的低清预览，不对第三方内容重新授权；有异议可通过 Issue 要求处理 |
| 网站源码、JavaScript、测试脚本、Skill | MIT（参见仓库 `LICENSE`） |
| `catalog/index.json` 外部参考 | 只包含链接、原创简评与复用建议；原论文图片、Logo、截图和下载物并**未**因此获得我们的许可 |

贡献者应确认作品确有相应授权。单纯署名不能替代转载、修改或商业再分发许可。

## 可核实授权的第三方原图优先入库

如果论文/作者已授予允许再分发的许可证（例如 CC BY 4.0），不必另行逐个请求许可；逐文件保留作者、原始地址、许可链接和改动说明。**许可只覆盖其实际权利范围**，图片内部若另有署名或第三方素材，仍需按具体情况检查。论文/网站可访问不等于获得再分发权。新增第三方媒体请统一登记 `assets/third-party/manifest.json`，不把它们混入本站原创 CC BY SVG 或 MIT 软件授权。

## 不要默认复制第三方内容

未经明确许可或其他充分合法依据，不批量下载或将论文截图、PDF、图标、字体、商业模板、原项目图片放进仓库。优先提供原站 URL、作者与我们的设计分析。必须区分：原创模板、概念草图、外部参考、真实实验结果。

## 科学真实性

当前五份 SVG 模板中的数据、示例标签均为**概念性内容**，不能作为任何真实论文实证结果发布。提供实际数值时应附相关实验设置、数据和对应引用。

## 隐私与数据处理

静态网页的人工自查功能不上传图片、论文和使用记录。用户自行调用外部模型与 Agent Skill 时，应了解模型供应商的数据使用政策。不要未经许可收录未发表论文、内部实验、私人仓库信息或联系方式。

## 商业化边界

未来商业产品可以独立存在，但开放社区素材不会自动变成专有商品；有收费项目时，必须重新明确创作者授权、贡献者权利和第三方许可。

## 版权异议、撤除与更正（Rights and removal requests）

**如果您是作者、版权方、出版方或其代理，认为 OpenResearchAssets 的某项图片、截图、预览、文字或链接不适合被收录或展示，请[提交素材撤除 / 更正申请](https://github.com/Suchenl/OpenResearchAssets/issues/new?template=asset-removal.yml)。** 我们会及时核查来源、权利依据及具体争议，并在必要时先停止相关展示，再撤除、替换或更正对应内容。即使我们此前标注了来源与署名，也欢迎权利人表达意愿。

申请时请提供：具体站内 URL 或资产 ID、所涉及作品或媒体的原始链接、您的权利关系或代理身份、希望撤除或更正的部分及简要说明。**Issue 属于公开页面，请勿提交私人证件、未公开文件、敏感联系方式。** 如果不适合公开提交权属材料，可先发起不含个人敏感信息的简短 Issue 询问安全联系方式，或使用 [GitHub 官方版权投诉渠道](https://github.com/contact/dmca)。

维护流程：记录请求 → 检查单条 catalog/index.json 及 assets/third-party/manifest.json → 对有争议的图片酌情先暂停展示 → 同步更新首页卡片、详情、原始文件及派生 AI JSON → 检查部署结果并回复处理结论。Git 历史、镜像和缓存可能保留旧字节；如果需要彻底清除历史，应单独处理，不能保证仅删除当前分支就能撤销已发生的复制。

我们提供的是**科研参考、来源导航和带评述的资源整理**，不是第三方官方发布或通用素材再授权。非盈利、署名、导流和设置撤除入口都**不能替代必要的授权或其他合法使用依据**。

**English:** Copyright owners, authors, publishers and authorized representatives can [request removal or correction](https://github.com/Suchenl/OpenResearchAssets/issues/new?template=asset-removal.yml). Please identify the affected asset URL, source work, rights relationship and requested action. Do not post sensitive personal data in public Issues. We will assess the concern promptly, restrict display where appropriate, and update catalog records, media files and derived indexes. For formal claims, use [GitHub's copyright reporting process](https://github.com/contact/dmca). Attribution, noncommercial operation and this removal channel do not themselves grant permission.

**English summary:** Original SVG templates and previews are CC BY 4.0; site code and the Skill are MIT. Linked third-party resources retain their own rights. Do not upload private manuscripts or unlicensed figures. Community contributions are not implicitly licensed for proprietary resale.

**原创案例分析 ≠ 原论文原图。** RoboRender、RoboDojo 与 SuperMimic 的六份分析图均由本项目独立绘制，描述原始工作中可迁移的信息组织思路；原作者论文和官网保留其独立版权。RoboDojo 提供其官方媒体服务器上的原图链接，而不是将图像下载进本仓库；官方源码许可证不必然覆盖外链媒体图。

## 外链真实源图的边界

除已按照许可保存在仓库的少量原图外，官网及作者页面的真实图片可作为外链预览并附来源和版权异议入口。**外链不是已获授权的图片库副本，也不是独立合法性保证**。当媒体与条目讨论的是同一项目的不同部分（如网站上的训练数据图与论文 Teaser），需标明准确身份，不得错误称为官网截图或论文 Figure 1。遇权利异议应优先停止相应展示并核实。

### 当前六个核心案例的准确媒体身份

| 案例 | 实际展示 | 不可混淆的对象 |
|---|---|---|
| RoboRender 论文 | 论文 PDF 首页 Figure 1 / Overview | 训练数据分布、生成质量图、模型架构图 |
| RoboRender 主页 | 官网当日浏览器首屏截图 | 论文 Teaser |
| RoboDojo 论文 | 官方 Figure 1 / Unified Benchmark 总览 | 42 个任务的完整场景网格 |
| RoboDojo 主页 | 官方站真实 Hero 截图 | 已失效的作者作品集图片链接 |
| SuperMimic 论文 | 论文 Figure 1 / World-Model Rollout 与算力 | 官网单独的 GPU 墙配图 |
| SuperMimic 主页 | 官方站真实标题与机器人展示首屏 | 网页 Demo poster |

图片原作者、版权、截取/缩放处理信息逐条见 [manifest.json](../assets/third-party/manifest.json)。有权利异议即按上方撤除流程处理；不要把「非商业＋标注出处」当成自动免责。
