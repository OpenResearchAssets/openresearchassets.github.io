# OpenResearchAssets · 科研设计精品资产库

**中文（默认）** · [English](README.en.md) · [在线主页](https://suchenl.github.io/OpenResearchAssets/)

> **Quality over quantity. 科学真实先于美观。**
>
> 面向科研工作者，精选值得研究的视觉表达参考、提供原创可编辑素材，以及可实际使用的质量检查方法。

这个项目不追求收录最多的论文图，也不声称已经开发出自动审美模型。我们希望每项内容都有明确用途、可信来源和可复用的设计经验。

## 现在能用什么

| 功能 | 入口 | 真实状态 |
|---|---|---|
| 静态双语主页与参考检索 | [首页](https://suchenl.github.io/OpenResearchAssets/) | 支持中文/英文切换，8 条链接式外部参考及分类/关键词过滤 |
| 原创可编辑 SVG | [首页·原创素材](https://suchenl.github.io/OpenResearchAssets/#assets) | 三张概念示意模板，可直接下载；**不代表真实实验成果** |
| 科研图表人工质量自查 | [质量自查](https://suchenl.github.io/OpenResearchAssets/quality.html) | 五类对象的手动检查清单；支持标记问题、导出 Markdown 报告；**不会自动识别图片** |
| Agent 审核指导 Skill | [SKILL.md](skills/quality-critic/SKILL.md) | 可供支持文件查看的 Agent 参考执行；效果未经独立专家评估，运行由用户自行提供 |
| 设计与版权规范 | [质量规范](docs/QUALITY_STANDARD.md) · [资产授权](docs/ASSET_POLICY.md) | 可阅读的编辑规则和来源约束，不构成学术结论或出版认证 |

## 使用方式

无需注册、托管后端、GPU、数据库或付费 API。下载仓库后，直接在浏览器中打开 HTML，或使用本地服务器：

```bash
python3 -m http.server 8000
python3 tests/check_project.py
# 需要已安装 Playwright 与 Chromium 时可选：
python3 tests/browser_offline_smoke.py
```

浏览器质量自查始终是**人工选择问题**：网页无法读取用户论文内容，不自动分析图像或上传文件。如果你选择用外部 Agent 和 Skill 处理未发表稿件，请自行确认模型提供方的数据处理条款。

## 社区与项目标准

1. **科学真实为硬门槛**：图中的数值、比较和研究结论不得随意改写。
2. **少而精**：每条参考都应说明为什么值得学，不只附链接。
3. **真正可编辑**：形状与文字需可独立调整，不能把一张截图放进 SVG 外壳。
4. **实际版面审核**：所有投稿用图需在最终 PDF 尺寸检查可读性。
5. **版权与隐私优先**：第三方图像优先外链，未公开论文与商业资料不进入公共仓库。
6. **公开部分保持开放**：未来商业服务需另行确权，不将社区贡献直接转为专有资产。

欢迎通过 [Issue](https://github.com/Suchenl/OpenResearchAssets/issues/new/choose) 和 [Pull Request](https://github.com/Suchenl/OpenResearchAssets/pulls) 贡献高质量参考、原创模板和可复核的问题案例。详情见 [贡献规范](CONTRIBUTING.md) 与 [AI 维护规则](AGENTS.md)。

## 仓库结构

- `index.html`、`quality.html`、`principles.html`、`contribute.html`：中文默认、英文可切换的网站页面。
- `data/references.js`：参考资源的唯一结构化来源，含中英文字段。
- `assets/templates/`、`assets/previews/`：原创 SVG 与对应 PNG 预览。
- `skills/quality-critic/`：用于其他 Agent 的质量审核工作说明。
- `docs/`：公开质量规范、设计规则、许可、部署和公开产品边界。
- `tests/`：不需要后端的静态检查与浏览器验收脚本。

## 开源与许可

- 程序、网站和 Skill：MIT（参见 [LICENSE](LICENSE)）。
- 仓库原创 SVG 模板和预览图：CC BY 4.0（参见 [资产政策](docs/ASSET_POLICY.md)）。
- 第三方参考链接所指内容不因此获得上述许可证，版权仍属于原权利人。

**当前公开项目不提供自动图像诊断、AI 改图服务、在线付费设计或已训练的审美质量模型。** 未来想法不会以未实现的产品功能进行宣传。
