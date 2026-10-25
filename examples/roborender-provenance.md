# RoboRender 真实论文案例 · 来源与可复核性 / Provenance

> 本页是 OpenResearchAssets 的**原创二次研究解读**，不是论文原作者的官方复现报告。论文方法和结果均是**作者报告**；我们只校对了公开来源并重绘图表，没有训练模型或运行真机实验。所有素材截至 2026-10-25 核验。

## 主要一手来源

- 作者项目主页：[RoboRender](https://robo-render.github.io/) — 方法架构、数据规模、生成性能与 **Real-world success rate across tasks** 表；8 任务×每任务 10 rollouts 的说明。
- 论文初稿：[arXiv:2610.09254](https://arxiv.org/abs/2610.09254) — 2026-10-07 提交，作者 Huang Huang, Wensi Ai, Ziyu Chen, Youhui Wang, Zijian Du, Yang Liu, Jiaolong Yang, Li Fei-Fei, Jiajun Wu。
- 作者公开代码：[robo-render/RoboRender-Video-Model](https://github.com/robo-render/RoboRender-Video-Model) — 查询时有推理入口、README、依赖与命令；**这不等于我们验证过端到端训练代码/完整原始训练数据公开**。
- 作者模型入口：[RoboRender Hugging Face](https://huggingface.co/RoboRender/models) — 公开模型列表；在声明可复现前仍需核对 checkpoint、license 和环境。
- 已收录的**核实 Figure 1**：[本站 RoboRender 资产](../asset.html?id=roborender-teaser)；其版权、原始来源、修改记录见 [第三方媒体台账](../assets/third-party/manifest.json)。我们的流程图和证据图是全新 SVG，**不是原始 Figure 1 复刻**。

## 逐项来源表与数字复核

数据文件：[real-robot-results.csv](real-robot-results.csv)。逐任务数字全部按作者官网表录入，未插值、未臆造，字段 `provenance=author-reported`、`independent_replication=no` 明确证据等级。

| 指标 | Sim | Sim + DR | RoboRender |
|---|---:|---:|---:|
| 8 项任务等权平均（由逐项数字计算） | 10.00% | 20.00% | **71.25%** |
| 作者公开页面整数平均 | 10% | 20% | **71%** |

- 每任务 **10** 次 rollout，8 任务共 **80** 次/方法；不是跨多实验室的大样本验证。每项的 10% 变化对应 1 次成功变化。
- 官网的约 **7.1× / 3.6×** 是对这组基线的比例，不能解释成普遍跨所有机器人的倍率。
- 视频生成器训练使用约 **126,950** 份真实操作片段（DROID/AgiBot），策略训练使用模拟轨迹生成视频，真机策略评估为零样本部署。**禁止把“零样本部署”混写成“整个系统不使用真实数据”。**
- 本案例没有公开 raw rollout logs、方差、任务难度分布的独立审计，无法单凭此 CSV 计算可信的跨环境置信区间或认定统计显著性。图上不提供虚构误差线。
- 在作者官网还有生成质量 FID/FVD/PSNR/SSIM/LPIPS 对照、depth-only 与视频生成模型对照；本站本案例集中审查“生成的视频作为训练数据是否提升真机任务”，没有擅自将其他指标合并为总分。

## 素材与版权边界

- 中文版 `assets/examples/roborender-method.svg`、`assets/examples/roborender-evidence.svg` 与英文版 `assets/examples/roborender-method.en.svg`、`assets/examples/roborender-evidence.en.svg` 是本站原创**可编辑分析图**。只使用公开事实和我们绘制的文字、框、连线；不含外部论文图片、Logo 或视频。
- 页面里引用已有的 `assets/third-party/roborender/figure1-overview.jpg`，仅作为带作者署名、明示来源的**论文 Figure 1 评论缩略图**，保留既有台账记录和撤除入口。该 JPEG **不获得**本站原创 SVG 的授权。
- **不能复现**：未下载训练数据、未启动模型训练、未对实际机器人跑实验。任何重新训练、部署或科研数据复用都需要独立核实资源、许可证和环境条件。

## 未来贡献者如何审计或升级

1. 按官方发布页对照每一个结果单元格与训练/评估口径。
2. 当作者论文或官网更新时，记录核对日期与变化；不要把旧表与新表无说明混合。
3. 如果有第三方独立复现，单独记录运行硬件、数据划分、代码 commit、rollout 级日志和环境差异，绝不覆盖原作者结果。
4. 审阅每个对外主张是否能够链接到具体表格、方法描述或真实操作视频；不借“论文已发表/代码公开”暗示完全复现。

**English summary:** Original editorial case built on authors' public results (8 tasks, 10 rollouts per task; 10%/20%/71% displayed averages). We have not reproduced the experiments. The renderer used real robot videos during its own training; the downstream policy was trained on generated simulation-based data and deployed zero-shot. The included SVGs are editable editorial drawings, not official paper figures.
