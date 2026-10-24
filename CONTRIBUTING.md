# 如何向 OpenResearchAssets 贡献内容 / Contributing

欢迎研究者、设计师、开发者贡献经过认真打磨的作品。这里遵循**质量重于数量、科学真实优先、中文主文档 + 英文辅助**。

## 接受哪些贡献

- **优秀参考**：原始官方链接、作者、论文/项目名称和至少一条**具体可学习**的设计分析；禁止只说“很漂亮”。
- **原创可编辑资产**：SVG、可编辑 PPTX、HTML 或源代码，配预览、使用说明、明确版权归属和许可。
- **设计诊断案例**：获得合法展示授权的 Before/After，说明原问题、修改、科学事实核对与最终 PDF 复核。
- **审核标准与 Skill 改进**：指出当前规则错漏的具体案例、建议和最小可复现检查。

## 提交规则

1. 先核验科学事实：图形的标注、数值、轴、实验条件和 caption 不能误导。
2. 解释信息价值：读者应该能指出这项设计让什么信息变得更易理解。
3. 检查真实尺寸：在期望发表环境确认字体、线宽、箭头和留白可读。
4. 确认真正可编辑：不接受用一个位图充当 SVG/PPTX 内容的“伪矢量”。
5. 说明来源和版权：第三方论文图片默认**只链接**，不能随意镜像或转售。
6. 不提交未授权的私人论文、用户数据、商业资源和内部实验资料。
7. 修改站点和元数据时，**中文与英文同步**；网站 `data/references.js` 必须包含简洁的中文注释（`tagZh`、`kindZh`、`noteZh`、`shortZh`），英文保留对应字段。

## 两类提交方式

**外部参考**：修改 `data/references.js` 中对应条目或新增经过检验的条目；`category` 使用 `Research`、`Gallery`、`Toolkit`，通过提交说明解释高质量的具体原因，不搬运图片。

**原创模板**：提供 `assets/templates/<name>.svg` 与 `assets/previews/<name>.png`，需有源文件、允许的许可证、概念/实验属性说明及实际编辑检查。公开原创模板按仓库 [资产政策](docs/ASSET_POLICY.md) 授权，贡献前确认同意相应条款。

## 提交与审核

运行：

```bash
python3 tests/check_project.py
python3 tests/browser_offline_smoke.py  # 若已安装 Playwright 与 Chromium
```

维护者首先审核科学真实性、授权和隐私，然后审阅表达质量、可编辑性及排版。拒绝投稿时提供可操作原因，而不是空泛审美评价。我们欢迎不同风格和学科。

[提交 Issue](https://github.com/Suchenl/OpenResearchAssets/issues/new/choose) · [查看 Pull Requests](https://github.com/Suchenl/OpenResearchAssets/pulls)

**English summary:** Submit traceable references, genuinely editable original artwork, or permission-cleared quality cases. Include source, license, scientific context, design rationale, and Chinese/English metadata. Never upload private manuscripts or unlicensed third-party figures.
