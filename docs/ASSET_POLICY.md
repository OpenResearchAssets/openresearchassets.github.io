# 资产来源、许可与隐私规范 / Asset Policy

## 内容及版权

| 内容 | 当前许可/边界 |
|---|---|
| `assets/templates/*.svg` 原创可编辑模板 | CC BY 4.0，署名 OpenResearchAssets contributors，标注原仓库链接 |
| `assets/previews/*` 原创模板预览 | 同对应 SVG 的 CC BY 4.0 |
| `assets/editorials/*.svg` 原创案例分析图 | 本项目独立绘制的研究方法/信息结构分析，CC BY 4.0；不包含原作者论文图片或网站截图。复用时请注明 OpenResearchAssets 和研究原始来源 |
| `assets/third-party/roborender/model-architecture.png` | 来自 RoboRender 官方项目仓库 `fig2_model.png`，原封不动复制；对应论文 arXiv:2610.09254 标注 CC BY 4.0；作者、来源、许可链接、blob SHA、注意事项见 `assets/third-party/manifest.json`，**不纳入本站原创 SVG/代码统一许可** |
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

## 下架申请

权利人可以通过 GitHub Issue 指出存在争议的具体素材和权属。维护者应及时限制问题素材的展示并核实合法性。

**English summary:** Original SVG templates and previews are CC BY 4.0; site code and the Skill are MIT. Linked third-party resources retain their own rights. Do not upload private manuscripts or unlicensed figures. Community contributions are not implicitly licensed for proprietary resale.

**原创案例分析 ≠ 原论文原图。** RoboRender、RoboDojo 与 SuperMimic 的六份分析图均由本项目独立绘制，描述原始工作中可迁移的信息组织思路；原作者论文和官网保留其独立版权。RoboDojo 提供其官方媒体服务器上的原图链接，而不是将图像下载进本仓库；官方源码许可证不必然覆盖外链媒体图。
