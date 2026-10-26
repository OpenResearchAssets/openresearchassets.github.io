# Skill 来源核验与入库流程 / Skill Source Intake & Audit

> 本流程针对**收录之前的来源核验**，不是安装或运行第三方 Skill，也不是效益验证。中文为主；下方保留英文快速说明。

## 适用场景

整理准备加入 OpenResearchAssets 的具体 `SKILL.md`：确认其真实功能、最低依赖、输入/输出、许可及来源版本。与人工审查独立，自动检查仅用于发现目录字段缺失和来源标记错误。

## 输入

- 拟收录仓库 owner/name，原始 Skill 相对路径（必须落到具体 `SKILL.md`）
- 实际科研任务以及需要的输入、输出、验证目标
- 上游 LICENSE、`SKILL.md` 声明的环境/鉴权/联网前提

## 步骤

1. 打开**上游原仓库**具体 SKILL.md，读取功能、依赖与代码/权限范围，判断是否具有可操作的科研任务价值。
2. 通过 GitHub 仓库源数据记录当前 Stars 和日期；如收录单项 Skill，明确这是**母仓库 Stars**，不得将之冒充单项使用量。
3. 用 GitHub Contents API 获取上游独立文件的 Blob SHA，登记 `execution.source_file_sha` 和 `source_checked_on`，不复制第三方 Skill 原文。
4. 在唯一权威目录 `catalog/index.json` 编写中文权威+英文辅助的 `inputs, outputs, requirements, steps, checks`，说明尚未执行。
5. 运行 `python3 tools/sync_catalog.py` 更新派生 manifest 与单条 JSON；运行 `python3 tools/audit_skill_intake.py` 更新审计报告。
6. 运行 `python3 tools/sync_catalog.py --check`、`python3 tools/audit_skill_intake.py --check` 和 `python3 tests/check_project.py`，再通过浏览器测试对照详情页面。
7. 只有真正运行 Skill 后并形成可追溯的公开输出和验证日志，才能另行考虑升级验证状态；来源审核不等于真实效益证据。

## 输出与验收

- 唯一资产档案和派生的 AI 单项索引
- [独立 Skill 审阅报告](../docs/SKILL_INTAKE_AUDIT.md)
- GitHub Actions 的可复核测试结果（含浏览器回归）

**边界：** 离线检查不证明远程链接现在仍有效、依赖仍可用、许可证没有变化，更不证明 Skill 功能或安全性。不得自动将 Findings 的热门候选提升为精选；人工审查必须独立完成。

## English quick guide

Verify the *individual* upstream SKILL.md and rights before curation. Save a source blob SHA, dated GitHub repository Stars, and the task-specific bilingual inputs, outputs, requirements, steps and checks. Run the sync and offline audit scripts, review the generated dossier in a browser, and keep **source review** explicitly separate from **independent execution evidence**.
