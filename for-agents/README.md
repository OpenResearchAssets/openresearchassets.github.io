# OpenResearchAssets：供 AI 直接使用的科研资产目录

> 公开入口：https://suchenl.github.io/OpenResearchAssets/for-agents/  
> 唯一资产目录：https://suchenl.github.io/OpenResearchAssets/catalog/index.json

## 使用流程

1. 读 \`catalog/index.json\` 中的 \`facets\` 与 \`entries\`，不要先逐页抓取全部外部网站。
2. 根据当前任务匹配 \`tasks\`、\`stages\`、\`domains\`，并对中英文 \`keywords\`、\`description\` 与 \`applicability.use_when\` 做语义匹配。不要只凭字符串硬匹配。
3. 优先阅读最相关的 2–5 项，每项关注 \`learn\`、\`avoid\`、\`rights\` 和 \`links\`。
4. 对参考类资产，借鉴设计模式或方法经验，但不得冒充原作者原始图片；未经明确授权，不能复制论文图或主页截图。
5. 对原创可编辑资产，优先使用 \`links.editable\` 提供的源文件，并更换所有概念性数据与内容。
6. 对 Skill / Workflow，读取对应原文件，确认执行前提和能力边界。
7. 产出时说明使用了哪些资产、哪些属于可编辑原件、哪些只是外部参考；验证科学事实和最终交付文件。

## 适用范围与可靠性

本目录是人工精选的科研辅助资源，不是一个能自行运行实验或修改本地文件的远程执行服务。AI 必须有相应文件、浏览器或代码执行权限才能执行任务。当前收录只代表经过来源整理与描述，不代表所有工具都经过实测。

## 主要入口

- [结构化目录（JSON）](../catalog/index.json)
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
