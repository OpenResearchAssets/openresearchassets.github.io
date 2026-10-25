# 来源核实 → 可编辑科研证据图 / Source-to-Figure Workflow

**类别：项目实践积累，非通用自动化程序。** 来源：OpenResearchAssets 已完成的 RoboRender 公开视觉分析和结果核对。这里记录的是已发生的公开制作流程，不声称已经对其他论文做效果对照或跨团队复现。

## 何时使用 / When to use

需要从已有论文和官方项目页制作原创可编辑 Method/Result SVG，又必须区分原作者事实、本站解释及第三方图片版权时。

## 已有公开产物 / Evidence of actual use

- [作者结果来源逐项核验](../examples/roborender-provenance.md)；[逐任务原始转录 CSV](../examples/roborender-results.csv)。
- [原创 Method SVG](../assets/examples/roborender-method.svg)；[原创 Evidence SVG](../assets/examples/roborender-evidence.svg)（含英文版）。
- [对外说明页](../examples/roborender.html)；[静态内容与浏览器验收](../tests/check_project.py)。

注意：上述结果由论文作者报告，我们只核实公开来源、绘制分析图和验证网页，并**没有**复现机器人实验。

## 可迁移步骤 / Reusable process

1. **锁定主张与一手出处。** 对每条数字、方法模块、图像身份记录原始论文图表、官网地址和核验日期。
2. **分离原图与解释图。** 原论文图保留作者版权、许可和来源。我们的二次绘图必须有自己的 SVG 源文件和明确标注。
3. **先建立可追溯数据表。** 逐项记录任务名、条件、分母、结果数值；没有原始日志时不要虚构误差条或统计显著性。
4. **把语义转换为结构。** 模块、箭头、对照组和主张必须与文本一致；不要用视觉并列暗示不存在的实验因果性。
5. **输出原生 SVG。** 文字、线条、图形保持可编辑；可以在修改前保存原有优良布局作对照。
6. **执行验收。** XML/链接/数字一致性检查 + 实际浏览器截图检查 + 最终版面下的人工审美和可读性复核。
7. **交付审核链。** 提供可编辑 SVG、数据 CSV、来源审计、使用边界，而不仅是一张漂亮截图。

## 预期输出 / Outputs

**必备：** 可编辑图稿、来源记录、数字核对表、最终渲染文件、尚未验证的事项清单。

**禁止：** 作者论文的原图被标为本站原创；把引用的作者性能提升写成我们的独立实验；使用未授权第三方图像。

**English:** This repeatable editorial workflow was applied to the public RoboRender analysis files linked above. Check primary sources, transcribe results, preserve author rights, draw editable SVGs and verify real rendered output. It has **not** undergone independent utility benchmarking.
