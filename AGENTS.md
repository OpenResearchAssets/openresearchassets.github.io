# OpenResearchAssets · AI 维护规则 / Agent instructions

**中文为主、英文为辅。科学真实性、页面实际功能和版权是不可妥协的要求。**

## 产品北极星（所有维护 Agent 必须遵守）

OpenResearchAssets 是**面向人类与 AI 的科研全过程可复用资产库**，不是只收藏漂亮图片的图库。长期希望研究者仅提供当前科研任务、网站 URL 和所需文件/工具权限，Agent 就能自行查找、理解并选择最相关的经验、方法、工具、Skill、工作流或可编辑素材，并推动实际任务，减少重复检索、重复提示、人工返工、时间和 Token 消耗。

维护时必须优先回答：**新增资源解决了哪个科研任务？AI 何时该使用它，如何操作，哪些科学/授权边界不可越过，怎样验证收益？** 从选题、文献、方法、实验、评估、写作到投稿/传播均可收录；起步重点 AI/CV/Robotics 与科研表达，不是永久边界。衡量价值须看真实任务的质量、耗时、人工干预与 Token，而非收藏量。不得把 URL-only Agent 完成科研说成现有功能。

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

**English summary:** Keep the public site Chinese-first with complete English UI support. Show only implemented capabilities. Preserve scientific fidelity, licensing and privacy. Prefer useful methods over benchmark-building. Validate real rendering and interaction before release.

13. **AI 节约上下文**：首选 `catalog/manifest.json`，再沿 `catalog/entries/<id>.json` 取少量详情。唯一手工维护源是 `catalog/index.json`；编辑后运行 `python3 tools/sync_catalog.py` 并用 `--check` 核对派生文件。CI 需要同时验证静态结构与浏览器行为。

15. **真实媒体优先但逐文件确权**：允许复制 CC BY 等已有授权的第三方图片，不需要再发邮件逐项申请，但必须在 `assets/third-party/manifest.json` 登记作者、原始路径、版权依据、原图 Git blob SHA、修改状态，单条 catalog 的 rights 须可查；不要把外部图重新赋予本站 MIT 或原创 SVG 许可。来源不明者默认仅链接，合法例外需针对具体用途单独审查。
