# OpenResearchAssets：供 AI 直接使用的科研资产目录

> 公开入口：https://openresearchassets.github.io/for-agents/  
> 唯一资产目录：https://openresearchassets.github.io/catalog/index.json

## 使用流程

1. **先读取 [轻量索引](../catalog/manifest.json)**，按任务、阶段、领域与类型挑选少量条目，再沿各条目的 entry 路径读取完整 JSON；不要默认一次加载整个目录。
2. 结合任务、阶段、领域、中文及英文关键词进行筛选，随后打开独立记录检查适用条件、可迁移经验、限制、版权和官方来源。
3. 优先阅读最相关的 2–5 项，每项关注 \`learn\`、\`avoid\`、\`rights\` 和 \`links\`。
4. 对参考类资产，借鉴设计模式或方法经验，不冒充原作者图片；只有单条 `rights` 明确允许且保留署名/许可的媒体可以直接复用，其他图片需要独立使用依据。
5. 对原创可编辑资产，优先使用 \`links.editable\` 提供的源文件，并更换所有概念性数据与内容。
6. 对 Skill / Workflow，读取对应原文件，确认执行前提和能力边界。
7. 产出时说明使用了哪些资产、哪些属于可编辑原件、哪些只是外部参考；验证科学事实和最终交付文件。

## 适用范围与可靠性

本目录是人工精选的科研辅助资源，不是一个能自行运行实验或修改本地文件的远程执行服务。AI 必须有相应文件、浏览器或代码执行权限才能执行任务。当前收录只代表经过来源整理与描述，不代表所有工具都经过实测。

## 主要入口

- [轻量 AI 索引（JSON）](../catalog/manifest.json)
- [完整权威目录（JSON）](../catalog/index.json)
- [独立案例示例（JSON）](../catalog/entries/supermimic-teaser.json)
- [交互式检索（网页）](../index.html#references)
- [文献检索与证据筛选](../workflows/literature-triage.md)
- [论点驱动实验规划](../workflows/experiment-planning.md)
- [论文叙事与图表组织](../workflows/paper-evidence-story.md)
- [项目主页与科研成果发布](../workflows/research-release.md)
- [科研视觉质量检查 Skill](../skills/quality-critic/SKILL.md)
- [资产模型与贡献要求](../docs/ASSET_SCHEMA.md)
- [第三方内容与许可政策](../docs/ASSET_POLICY.md)

**中文是权威说明语言，英文用于国际检索与补充。**

---

English: Read the catalog first; select 2–5 matching resources by stage, domain, task and usage notes. Follow provenance, rights, and applicability. External visual references are inspiration only, not licensed local assets. Editable originals are linked explicitly. This is a resource library, not a remote autonomous execution service.

## 低 Token 检索与入口约定

`manifest.json` 的 `entry` 字段相对网站根目录，举例：`https://openresearchassets.github.io/catalog/entries/supermimic-teaser.json`。Agent 先选出最相关的 2–5 条，再取详细 JSON；如果不匹配可读取完整目录，但不得虚构已有的资产或授权。所有 JSON 分片都从唯一权威文件 `catalog/index.json` 自动生成；修改后运行 `python3 tools/sync_catalog.py`。只有具备网页读取能力的 AI 可以通过网址访问，实际执行还需要目标项目及工具权限。

## 获许可的真实论文图

已撤除 `roborender-model-architecture`，不得作为当前资产结果引用。六份 RoboRender/RoboDojo/SuperMimic 精选条目现已匹配原论文 Figure 1 或实际官网首屏，支持 `figureIdentity` 和 [第三方媒体台账](../assets/third-party/manifest.json) 检查来源及权限；Depth Anything 3 使用官方真实总览图外链，不能对其再授权。

## 六个精准对应的视觉案例

RoboRender、RoboDojo、SuperMimic 分别有 `*-teaser` 与 `*-site` 两个条目。当前其 `visual.kind` 不是普通配图，而是 `verified-paper-figure`（原论文 Figure 1）或 `verified-site-screenshot`（真实网页首屏）。Agent 须核对 `figureIdentity` 才能将其用于论文参考、HTML 视觉设计或素材引用，不得混用。截图不等于官网模板源码，所有第三方媒体遵循原作者权利及撤除机制。
