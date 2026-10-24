# OpenResearchAssets

[简体中文说明](README.zh-CN.md) · English (this page)

**Craft better research.** A selective, quality-first library for excellent research communication.

> **Status:** first public-ready starter release (2026-10-24). The initial references are attributed external links, and the SVGs are original **conceptual templates**, not real paper findings. The browser quality checklist is **manual**, not an AI vision judge.

## What makes this different?

We're not trying to collect the most figures. We're building a **reliable standard of quality**: scientific faithfulness, clarity, composition, editing freedom and final-page legibility. The library combines four things:

1. **Inspiration** — a carefully explained shortlist of external research projects, visual references and creative tools.
2. **Editable assets** — original, source-editable SVG templates with explicit rights and limitations.
3. **Quality Critic** — a rigorous, human-readable standard; browser-based self-review and an agent-compatible skill.
4. **Craft & practice** — workflows, quality checks, contribution protocols and eventually real before/after case studies with permission.

### What's usable today?

| Output | How to use | Status |
|---|---|---|
| Homepage & reference gallery | Open `index.html` | Functional, searchable; eight external references |
| Quality Critic self-check | Open `quality.html` | Local-only manual checklist for five artifact types, report-to-Markdown copy |
| Quality Critic Agent Skill | `skills/quality-critic/SKILL.md` | Usable instructions for a multimodal agent with access to the artifact and relevant evidence; performance not independently validated |
| Editable SVG templates | `assets/templates/` | Three original conceptual layouts, not empirical results |
| Quality Standard | `docs/QUALITY_STANDARD.md` | First-edition rubric and evidence requirements |
| Licensing & provenance | `docs/ASSET_POLICY.md` | Strict separation of original assets from external reference links |

## Use locally — no server or AI API required

```bash
# Open the two static pages directly in your browser
open index.html
open quality.html

# Or serve the directory locally
python3 -m http.server 8000
# then browse http://localhost:8000

# Validate files
python3 tests/check_project.py
```

No dependency installation, database, account, GPU, tracking script or server-side inference. Existing third-party models can use the Skill on user-owned infrastructure, but their running and privacy terms are controlled by the user.

## Repository map

```text
index.html                   Editorial landing page and curated reference index
quality.html                 Human-operated, browser-only Quality Critic
css/site.css                 Shared visual design system
js/site.js                   Search and category filters
js/quality.js                Review questionnaire and Markdown output
data/references.js           Canonical external-reference metadata
assets/templates/           Three original editable SVG sources
assets/previews/            PNG previews of original SVGs only
skills/quality-critic/       Agent Skill and structured review workflow
docs/QUALITY_STANDARD.md     Quality rubric and review criteria
docs/ASSET_POLICY.md        Licensing, provenance and privacy
docs/PRODUCT_STRATEGY.md    Open-first strategy and future commercialization gate
CONTRIBUTING.md              Editorial rules and community workflow
tests/                       Offline smoke checks
```

## Editorial standard

**Quality over quantity** is a review criterion, not an excuse to exclude unfamiliar aesthetics. Submissions should demonstrate superior clarity and execution **for their stated scientific purpose**. We welcome different research fields, design languages and cultural styles.

- Every public figure reference needs a traceable original source and a reason for inclusion.
- No unlicensed reposting or redistributing authors' paper images.
- No fabricated metrics, datasets, model comparisons or experimentally unsupported claims.
- Original templates must remain edit-friendly; embedding one flattened image into an SVG does not qualify.
- Review against the *compiled publication layout* where applicable.
- Distinguish original artwork, third-party reference links, speculative examples and verified experimental figures.
- Community contributions remain open under their declared license. No automatic conversion to proprietary paid assets.

## Agent review (copy into your local agent)

> Follow `skills/quality-critic/SKILL.md` to review this figure or paper. Read the artifact and the supplied caption, research claim and supporting evidence. Separate objective errors, design problems and subjective style suggestions. Identify affected regions, prioritize specific fixes, and verify changes at final publication size. Do not make up a quality score, scientific results or evidence you have not seen.

## Distribution and hosting

This is a static website suitable for Cloudflare Pages (or any static hosting platform). Set the publish directory to the repository root, with no build command. Don't treat GitHub Pages as a default commercial SaaS host; select hosting appropriate to the deployment terms. A later product can remain separate without rewriting this open library.

## Project values & contribution

See [CONTRIBUTING.md](CONTRIBUTING.md). Suggestions and pull requests are reviewed for source integrity, copyright, reproducibility, information value and design craft. See [docs/PRODUCT_STRATEGY.md](docs/PRODUCT_STRATEGY.md) for the deliberate choice to start with a free product rather than charging users or incurring server costs.

## Licensing

- Source code (HTML/CSS/JS/Python/Skill instructions): MIT — see [LICENSE](LICENSE).
- Original editable templates in `assets/templates/` and their previews: **CC BY 4.0** — see [docs/ASSET_POLICY.md](docs/ASSET_POLICY.md).
- External projects listed in `data/references.js`: **not relicensed or redistributed** here; see their original authors' terms.
- New contributions require an explicit license and provenance; see [CONTRIBUTING.md](CONTRIBUTING.md).

Made for researchers who care about the science **and** the way it's explained.


**Publishing guide:** [Deploy the public website](docs/DEPLOYMENT.md) (GitHub Pages / Cloudflare Pages, including browser acceptance checklist).
