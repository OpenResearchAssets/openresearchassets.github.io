# 第三方真实来源图片 / Authentic source media

本目录当前**仅保留经过原图/原网页核对的六张图片**：三张来自论文 Figure 1 或作者官方 Teaser，三张为当日实际截取的项目主页首屏。此前误用的 RoboRender 训练数据图、生成质量曲线、SuperMimic GPU 墙和 Demo poster，均**不再作为论文 Figure 1 或网站截图出现**。

| 案例 | 当前实际媒体 | 源头 |
|---|---|---|
| RoboRender · Figure 1 论文首页 Teaser | [roborender/figure1-overview.jpg](roborender/figure1-overview.jpg) | https://arxiv.org/pdf/2610.09254#page=1 |
| RoboRender · 官方项目主页首屏 | [roborender/homepage-viewport.jpg](roborender/homepage-viewport.jpg) | https://robo-render.github.io/ |
| RoboDojo · Figure 1 论文总览图 | [robodojo/figure1-overview.jpg](robodojo/figure1-overview.jpg) | https://media.luminis-sim.com/media/home/teaser.png |
| RoboDojo · 官方项目主页首屏 | [robodojo/homepage-viewport.jpg](robodojo/homepage-viewport.jpg) | https://robodojo-benchmark.com/ |
| SuperMimic · Figure 1 论文首页图 | [supermimic/figure1-overview.jpg](supermimic/figure1-overview.jpg) | https://arxiv.org/pdf/2610.28480#page=1 |
| SuperMimic · 官方项目主页首屏 | [supermimic/homepage-viewport.jpg](supermimic/homepage-viewport.jpg) | https://supermimic.github.io/ |

论文图仅裁切、缩小、JPEG 压缩，保留信息内容；网页首屏在 1370×810 的实际浏览器中截取（视频瞬时帧随时间变化）。

- **RoboRender Figure 1**：原论文以 CC BY 4.0 公开，使用中注明作者、论文和裁切压缩修改。
- **RoboDojo 和 SuperMimic**：低分辨率、具体研究评论及设计分析参考，原作者保留版权；本仓库不对原图重新授权，有异议可通过 [素材撤除/更正模板](https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/new?template=asset-removal.yml) 联系。
- **网站截图**：作为评论网站信息架构的参考，不能当成代码版权许可证、可编辑源码，也不是完整页面归档。

每张图片的独立来源、身份、修改说明和署名参见 [manifest.json](manifest.json)。`assets/editorials/*.svg` 是本站原创的结构分析，与这里的原始媒体**不是同类素材**。
