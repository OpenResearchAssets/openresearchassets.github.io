# 官网视觉设计规范 / Website Design System

## 当前品牌方向：Apple × SuperMimic

强调 SuperMimic 的**论点与真实证据驱动叙事**，借鉴 Apple 的**克制留白与精密排版**。不是抄袭任一网站的素材或样式源码。

## 视觉硬约束

- 主背景为 `#FFFFFF`，浅冷灰层级为 `#F6F8FB`；不要重新使用大面积象牙白、米黄和奶油色。
- 文本采用石墨色 `#12161D`，次级文本 `#586273`，交互蓝色 `#2C5DB2`，深色重点分区 `#111827`。
- 系统无衬线字体栈；中文优先保证字间距、行高和移动端折行。英文不以装饰性大斜体制造“高级感”。
- Hero 提供**已实现价值主张**，应在首屏展示真实素材；避免假数据、假评价、付费客户标识及未实现产品 mockup。
- 适当使用真实科研图、对照、SVG 或交互，而不是堆砌空卡片。
- 视觉风格不应控制整个图库内容：社区科学资产可以具有多样的学科审美，只需符合质量准则。

## 中文默认、英文可切换

公开 HTML 页面以中文实际文本作为默认内容，使用右上角语言按钮切换到英文；资产目录卡片、筛选、详情页和人工检查报告也应同步。新增静态文案须维护 `data-i18n-*` 属性及双语；新增 JS 文案用语言对象分别定义两版。中文是编辑权威版本，英文是为国际读者准备的完整辅助界面。不要只翻译菜单或放一个 inert 的语言图标。

## 当前产品事实

- 3 张原创可编辑 SVG **概念**模板；15 条结构化科研资产（含 6 个论文视觉/主页案例）；5 类人工检查对象。
- `quality.html` 不做自动图像分析，不训练或调用美学模型，不上传论文。
- 无账号、云端协作、在线收费、托管推理或自动修图；这些不是已上线模块。

## 验收清单

运行 `python3 tests/check_project.py` 和可用时的 `python3 tests/browser_offline_smoke.py`；确认 1440、768、390、320px 的无横向溢出、导航/筛选可用、中英往返、质量问题勾选保留、报告生成正常。真实发布后还需核查 GitHub Pages 加载及浏览器实际效果。只通过构建不等于审美达标。

**English summary:** Neutral-white Apple × SuperMimic direction. Strong scientific claims, real evidence and editable artifacts, precise typography and restraint. Chinese is the default complete UI; English is a working secondary language. Never advertise unimplemented AI features.
