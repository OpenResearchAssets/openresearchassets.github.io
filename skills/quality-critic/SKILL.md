---
name: research-quality-critic
description: 用证据约束审查并改进科研配图、图表及论文视觉叙事。Scientific figure quality review: scientific fidelity, clarity, editability and final-page legibility.
license: MIT
---

# Research Quality Critic · 科研表达质量审核

> 中文为权威说明，末尾附 English summary。**这是一份可供 Agent 执行的审核 Skill，不是已训练或已验证准确率的独立质量模型，也不等于网页已经能自动分析科研图片。**

## 目标

帮助研究者把已经存在、但表达不够理想的 Teaser / Method Figure / Results / Table / Paper 改得更准确、更清晰、更有审美完成度，避免泛泛地“优化布局”。**优先形成可执行修改方法，而不是只建立评分 Benchmark。**

## 输入

- **真实素材**：用户提供的图像、SVG、PPTX、表格或论文 PDF。没有看到文件不得宣称已看过或评过美学质量。
- **科学上下文**：论文主张、caption、方法、数据以及已知实验条件。缺什么证据明确标注。
- **排版要求**：单/双栏、目标论文模板、最终图宽及读者群体（如果已知）。
- **任务范围**：只诊断、建议修改、实际改源文件或检查成品。

## 工作流程

### 1. 首先确定表达目标

用一句话写清楚读者应该从图中学到什么。标记素材类型：真实实证图、概念示意、生成参考图、设计草图。明确哪些事实无法验证。

### 2. 科学真实性硬门槛

核对数值、轴、单位、分母、对照条件、caption、箭头含义、视觉比较公正性、图像真实性。缺乏证据时写“待核验”，**不得猜测正确或错误的实验结果**。

### 3. 信息结构与可读性

定位具体面板、坐标或文字区域：重点是否明确、阅读路径是否顺畅、面板是否重复、图例是否明确、缩小后是否可读。

### 4. 审美与视觉工艺

检查字体层级、配色语义、线宽、对齐、留白、视觉均衡。客观可读性问题与个人风格偏好必须分别列出。不要把所有作品强制改成同一种极简风。

### 5. 真实版面检查

如果有 PDF 或源文件，在**最终论文排版尺寸**检查图表、caption、浮动体顺序、表格宽度和重点证据；没有真实排版不得宣称出版级验证完成。

### 6. 给出可执行输出

每个问题必须包含：`位置 → 实际观察 → 影响 → 严重程度 → 最小修改方案 → 验证方法`。

先列 **Blocking（事实错误）**，再列 **High（阅读问题）**、Medium、Low。尽量只给三个最值得改的问题，保留当前作品中已经做得好的设计。避免缺乏依据的 9.4/10 之类综合分数。

### 7. 当用户要求实际改稿

- 优先**局部修改**，保留内容、原有矢量编辑性和已经满足的要求；多轮修改时列出不能破坏的约束。
- 修改后重新渲染，检查文本溢出、线条、字体和对齐。
- 将修改前后嵌入相同实际版面比较；有条件时请独立人类给出偏好与原因。
- 清楚说明哪些检查已执行、哪些尚未执行，以及哪些事实仍需原作者核对。

## 输出样例

```text
素材：Figure 1 · Method overview
已收到：图 + caption；没有实验数据
主要意图：……
保留：……
问题一：High · Panel B 左下
  可见现象：……
  影响：……
  最小修复：……
  复核：……
未验证：……
修改顺序：1. …… 2. ……
```

## 工具和隐私

使用 Agent 实际可用的图片查看、文档/PDF 渲染、代码和科学数据核对能力。用户未授权时，不将未发表稿件传给外部模型服务。**本 Skill 可免费使用，但审核与修改效果取决于执行它的 Agent、实际证据以及人工复核。**

详细质量边界见 `../../docs/QUALITY_STANDARD.md`（单独安装 Skill 时可不依赖这个文件）。

## English summary

Review real user-provided scientific artifacts against scientific fidelity, communication, craft and final publication layout. Locate issues precisely, propose minimal verifiable edits and preserve existing scientific constraints. Never hallucinate data or claim quality improvements without actual checks. This is an agent instruction protocol, not a separately trained or benchmarked AI reviewer.
