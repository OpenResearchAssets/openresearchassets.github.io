# Publish the website / 网站发布

The website is entirely static. No API key, server, database, hosted model, payment processor, or custom GitHub Actions workflow is required.

## Option A — GitHub Pages (for the current free, non-commercial library)

1. Open [Repository Settings → Pages](https://github.com/Suchenl/OpenResearchAssets/settings/pages).
2. Under **Build and deployment**, select **Deploy from a branch**.
3. Choose **main** and **/(root)**, then **Save**.
4. Once GitHub reports deployment completed, visit **https://suchenl.github.io/OpenResearchAssets/**.

If the URL returns 404 before deployment is enabled or finished, it does **not** mean the project files were not committed.

The website uses relative asset links, so it supports the repository subpath without custom routing. GitHub handles its own Pages publishing; this repository includes no custom Actions pipeline.

GitHub Pages should **not** be used to host a future commercial SaaS or transaction-focused service. Follow GitHub's current [Pages limits and terms](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages).

## Option B — Cloudflare Pages (recommended if commercial offerings are added)

1. Create a Cloudflare Pages project and connect the GitHub repository.
2. Use **no build command** and **/** (repository root) as the publish directory for this plain-HTML website.
3. Deploy and use the provided `*.pages.dev` hostname; add a custom domain only if desired.
4. Keep user-provided unpublished manuscripts and any payment or AI API keys out of this public repository.

## Verify locally

```bash
python3 tests/check_project.py
python3 -m http.server 8000
```

Open `http://localhost:8000` for the landing page and `/quality.html` for the manual review checklist.

**Acceptance boundary:** the static checks are not visual acceptance. Test desktop/mobile layout in a real browser before actively promoting the site, and independently verify all external reference links. The current Quality Critic browser page is **human self-assessment**, not automated scientific verification.

---

**中文摘要：** 首版是免费静态网站，无需购买服务器。现在可以在 GitHub 仓库的 Settings → Pages 设置 `main / (root)` 发布；未来如用于商业化收费，建议独立使用 Cloudflare Pages 等适当的托管服务。上线前需要人工检查桌面/移动端实际排版。
