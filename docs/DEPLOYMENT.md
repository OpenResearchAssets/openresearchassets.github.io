# 网站部署与验收 / Deployment

> 当前为**静态免费资源网站**：无需自建服务器、API 密钥、数据库、付费模型、支付服务或额外 GitHub Actions。页面默认中文，英文可切换。

## GitHub Pages（当前正在使用）

1. 打开 [Settings → Pages](https://github.com/OpenResearchAssets/openresearchassets.github.io/settings/pages)。
2. **Build and deployment** 选择 **Deploy from a branch**。
3. 选择 **main**、**/(root)**，保存。
4. 从 [Actions](https://github.com/OpenResearchAssets/openresearchassets.github.io/actions) 确认部署成功后，打开 [正式网站](https://openresearchassets.github.io/)。

资产清单通过 `fetch('catalog/index.json')` 加载，不能依赖 `file://` 方式打开首页。当前仓库就是组织根站点仓库 `OpenResearchAssets/openresearchassets.github.io`，源码使用相对路径，正式页面直接从根路径 `/` 访问，不再以 `/OpenResearchAssets/` 为正式前缀。404 可能是 Pages 尚未部署，不代表 Git 内容未提交。

**注意**：GitHub Pages 的使用边界应遵循当前 [GitHub 官方规定](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages)。将来如果变成商业交易/SaaS，请选择适合商业用途的独立托管平台。

## Cloudflare Pages（未来可选，不是现有服务依赖）

连接 GitHub 仓库，无需构建命令，发布目录是仓库根目录 `/`。只有在真正需要收费产品时再配置域名、认证和支付，不要提前公开未实现的服务。

## 本地验收

```bash
python3 tests/check_project.py
python3 tests/browser_offline_smoke.py   # 需 Python Playwright + Chromium
python3 -m http.server 8000
```

在浏览器中打开 `http://localhost:8000`。确认：中文默认、中英切换、导航、22 条资产的三维筛选与搜索、独立详情页、AI 目录读取、五份原创 SVG 下载、五种人工自查类型、Markdown 报告生成、移动端布局。测试桌面 1440px、平板 768px、手机 390/320px。

**能力边界**：通过测试不意味着审美已经得到用户认可。当前 Quality Critic 网页是**人工自查**，不自动读取、上传或分析论文；Skill 不是训练好的质量模型。外部引用的许可与有效性需要独立复核。

## English summary

A static bilingual website (Chinese default, English available). Deploy GitHub Pages from `main / (root)`. No backend, API keys, accounts or hosted inference. Run the static and browser smoke tests; never advertise the manual Quality Critic checklist as an AI vision judge.

外链真实媒体必须另外打开官方图片 URL 人工核查。离线 Playwright 测试只验证真实图片的来源地址、加载失败时的占位提示与本地许可媒体是否有效，**不能宣称对外部图片 CDN 的真实可用性已经做了持续测试**。
