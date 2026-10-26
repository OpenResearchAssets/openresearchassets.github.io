# Skill A/B 对照实验（第一轮）

**当前状态：配对任务与自动评分已就位。真实模型实验需要一个经授权的模型调用凭据。缺少凭据时，绝不捏造结果。**

## 科学问题和实验设计

同一个模型，使用固定系统提示词、相同任务、相同输出格式、同样温度与最大生成 Token，**唯一变动为是否插入已审阅 Skill 的通用指导**，能否改变受控科研任务的正确性与调用成本？

- 六道冻结任务，三个方向各两题：文献证据核验/筛选；机器人实验设计/人类评测；统计图误导/作者报告结果。
- A（`no_skill`）：只有固定系统说明与当前任务。
- B（`skill`）：相同信息额外加入对应 Skill 的**来源指导精简版**。这不是上游完整 SKILL.md，也不是在 Agent Harness 里自动加载能力。
- 六道题各运行 A/B 一次，固定随机种子 `20261026` 交替实验顺序，最多 12 次真实模型请求；任何接口错误立即停止，保留部分输出与失败原因。
- Gold 与任务分别放在 [gold.json](gold.json) 和 [tasks.json](tasks.json)，不发送 Gold 到模型；条件 prompt 除 Skill 文本外完全一致。
- **主指标：** 每个配对任务的 F1，算六个差值 B−A 的平均；附 Exact Match、Precision、Recall。
- **次指标：** API 返回的输入与输出 Token、请求执行时间、解析失败率以及原始 JSON。不得以 prompt 字符数代替实际 Token。
- 单轮文本、多选题结构化评测，**不是多步骤 Agent 自主调用工具、实验设计实践能力、科研结论可靠性或机器人部署的最终评测**。
- 六道任务是受控小样本预实验，不计算或宣称统计显著性，不通过调整题目迎合结果。

## 如何运行

代码 push 后，GitHub Actions 会自动运行**纯离线预检**：

```bash
python tools/run_skill_ab.py --dry-run
python tests/check_skill_ab.py
```

**真实 A/B 需要外部 API 授权**。在公开仓库的 GitHub → Settings → Secrets and variables → Actions 设置私有 Secret `AB_API_KEY`。然后通过 [Skill A/B Actions 页面](https://github.com/OpenResearchAssets/openresearchassets.github.io/actions/workflows/skill-ab.yml) 点击 **Run workflow**，填写由该 API 提供商支持的模型标识和 Chat Completions HTTPS Base URL。默认值示范 OpenAI 兼容接口，**没有配置凭证时推理任务不会运行**。

可本地运行：先在私有环境中设置 `AB_API_KEY`，然后执行：

```bash
python tools/run_skill_ab.py --model gpt-4.1-mini --api-base https://api.openai.com/v1 --max-calls 12
```

结果以 [GitHub Actions Artifact](https://github.com/OpenResearchAssets/openresearchassets.github.io/actions/workflows/skill-ab.yml) 的 `skill-ab-evidence/ab-results.json` 提供，记录真实模型回答、配对结果、Prompt 摘要、Token、耗时和任何失败。只留 60 天，公开题目请不要加入私人资料。运行前请确认提供商的费用与项目预算；脚本最多十二次调用，无自动重试。

## 官方 Skill 来源（精简版）

- [K-Dense Literature Review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/literature-review/SKILL.md)
- [K-Dense Experimental Design](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/experimental-design/SKILL.md)
- [K-Dense Scientific Visualization](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-visualization/SKILL.md)

指令来自这些文件的一般方法原则，由我们归纳成固定、简短且对所有题目通用的上下文。Skill 原始文本未被完整复制到项目，母仓库热度不视为效果证据。

## 未能由本轮回答的问题

三类研究能力的实际泛化，真实 Agent 工具调用、自动选择 Skill、不同强度基座模型、时间与 Token 更大规模重复，以及真正科研产物盲审。必须在本轮校验完成且没有数据泄漏后另设计独立的 holdout 实验。

**English:** This is a frozen six-task, twelve-inference, same-model **Skill-context injection A/B pilot**, not a native agent skill deployment. A push checks inputs without calling a model. Only a manual GitHub Actions dispatch with your authorized API key can run real model inference.
