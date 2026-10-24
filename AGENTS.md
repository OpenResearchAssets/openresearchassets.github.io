# OpenResearchAssets · AI 维护规则 / Agent instructions

**中文为主、英文为辅。科学真实性、页面实际功能和版权是不可妥协的要求。**

1. **只宣传已存在并验证过的公开功能**。当前 Quality Critic 网页是人工勾选检查表，不是上传论文自动分析；Skill 是指导协议，不代表已有经过训练与评估的审美模型。未来研究和付费方案不得写作已上线能力。
2. 公开网站**中文默认、英文完整可切换**。新增或改动 HTML、JS 动态文本、ARIA、图片替代文字和报告时，必须维护两个语言，测试首次中文显示以及两端切换。公共文档用中文做权威版本，英文说明作为辅助。
3. 网站风格遵循 **Apple × SuperMimic**：冷白/灰、石墨黑、简洁标题、真实素材和证据；避免暖黄纸感与无意义的卡片。视觉效果必须实际渲染检查。
4. 事实正确性先于审美：严禁伪造数值、改动研究结论或将概念图冒充实验结果；编辑图形必须保留其真实含义。
5. 第三方论文图片、Logo、图标和字体只在许可明确时入库；否则只保留官方来源链接与我们原创的评论。不得在公开代码中泄漏私有稿件、实验资料、凭据或个人隐私。
6. SVG 模板应保持文字及核心图形真正可编辑，附对应预览及来源信息；修改后检查原生编辑性。
7. `data/references.js` 是公开参考信息的唯一来源。只更新权威内容，不复制一套图库数据库、版本文件或多份互相冲突的路线图。
8. 不把 Agent 自评当作客观用户质量改善；真正的质量结果需要用户/专家评价、科学上下文和最终 PDF。
9. 优先开发**对用户有直接价值的方法与工具**，Benchmark 仅用于检验有效性；研究路线可在私有研发仓库讨论，但不能把它的内部内容自动发布出来。
10. 公开仓库只维护已发布的产品信息。商业化假设、未发布设计或内部研究计划留在私人工作区。任何跨仓库发布都需人工审查授权、事实与隐私。
11. 每次更改运行 `python3 tests/check_project.py`，重要视觉/交互改动运行 `python3 tests/browser_offline_smoke.py`，包含桌面/平板/手机、中英切换、筛选、手工质量报告和导航。报告必须说明哪些测试执行、哪些没有。
12. 文档与代码均保持单一当前版本：直接维护权威文件，避免 `v2`、`final`、`latest` 等平行副本，不以长篇更新日志代替当前状态。

**English summary:** Keep the public site Chinese-first with complete English UI support. Show only implemented capabilities. Preserve scientific fidelity, licensing and privacy. Prefer useful methods over benchmark-building. Validate real rendering and interaction before release.
