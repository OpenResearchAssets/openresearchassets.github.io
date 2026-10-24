# OpenResearchAssets — reusable research assets for humans and AI

**[简体中文](README.md) · English · [Website](https://suchenl.github.io/OpenResearchAssets/) · [For AI agents](https://suchenl.github.io/OpenResearchAssets/for-agents/)**

Research assets should be more than bookmarks. They should tell us **when to use them, what transfers, what to avoid, and where they came from**.

## Mission and intended use

**Our long-term goal is to make research experience directly usable by AI agents.** Given a task and one OpenResearchAssets URL, a web-capable agent should be able to discover relevant, trustworthy research lessons, tools, editable assets, and actionable workflows across the research lifecycle—from ideation and literature review to methods, experiments, evaluation, writing, websites, and release—without repeated manual searches or elaborate instructions. Using the assets in a real project still requires appropriate file and tool permissions.

We are **not merely a gallery of attractive paper figures or a directory of links**. Each curated asset should state when to use it, what can be learned or reused, how to apply it, its scientific and licensing constraints, provenance, and how to verify the result. The goal is to reduce repeated searching, prompting, trial-and-error, human corrections, elapsed time, and unnecessary tokens. Success must be measured on real tasks by relevance, outcome quality, intervention count, time, and token usage—not by collection size alone.

The initial focus is AI, computer vision, robotics and research communication. Full-lifecycle support is an ambition, **not a claim that an autonomous research service is already deployed**.

This Chinese-first, English-supported library spans research design, evaluation, writing and communication. The current public implementation includes:

- **21 structured entries** in [catalog/index.json](catalog/index.json), including separate teaser and project-site references for RoboRender, RoboDojo and SuperMimic.
- Browser-side search and facets for stages, domains and asset kinds, with per-asset usage and provenance pages.
- [Agent instructions](for-agents/) and [llms.txt](llms.txt) pointing to an openly readable machine catalog. These files do **not** mean there is an autonomous remote agent service.
- Four original Markdown research workflows covering literature, experiments, paper narratives and research release.
- Five original, editable SVG concept designs; an author-guided manual [quality checklist](quality.html); and an unvalidated [Quality Critic Skill](skills/quality-critic/SKILL.md).

Search the [interactive asset directory](https://suchenl.github.io/OpenResearchAssets/#references), or hand its URL to an agent that has web or file-reading capability. The JSON requires HTTP hosting; run \`python3 -m http.server 8000\` locally rather than opening the page with \`file://\`.

**Copyright:** Third-party paper figures, videos and website screenshots are not bundled or relicensed; visual previews without explicit authorization are locally authored structural diagrams, clearly labeled. The diagrammatic previews are **not** source figures. Our original SVG templates are CC BY 4.0; the code and Skill are MIT. See [asset policy](docs/ASSET_POLICY.md), [schema](docs/ASSET_SCHEMA.md), [contribution guide](CONTRIBUTING.md) and [AI maintenance rules](AGENTS.md).

**Current limitations:** no vector semantic search, no automated image review model, no remote autonomous research execution service, and no validated paid products. We do not present future features as shipped.

## Low-token AI catalog access

Agents should first read [the compact manifest](catalog/manifest.json), select a few relevant assets by task, stage and domain, then open only the corresponding [per-entry JSON files](catalog/entries/supermimic-teaser.json). The full [canonical catalog](catalog/index.json) remains the only authored data. Edit it, run `python3 tools/sync_catalog.py`, then `python3 tools/sync_catalog.py --check` before publishing. This is not a remotely executing AI service.

## Authentic media with traceable licenses

An official, unmodified RoboRender multiview architecture PNG is now included as its **own** asset ([model architecture](asset.html?id=roborender-model-architecture)), distinct from the authored teaser dissection. The upstream PNG and paper's CC BY 4.0 record are tracked in [the third-party media ledger](assets/third-party/manifest.json). The license on our own SVG templates and source code does not transfer to third-party images. Other unlicensed source media remain linked only.

## Copyright concerns and removal

Third-party works remain the property of their original rights holders. OpenResearchAssets collects research references with attribution and commentary, not as an official publication or a sublicensed image library. If you are an author, rights holder or authorized representative and object to an item, [request removal or correction](https://github.com/Suchenl/OpenResearchAssets/issues/new?template=asset-removal.yml). Identify the affected page/asset ID, original work and the change requested; do not publish sensitive personal documents in an Issue. We will review the report promptly and restrict, remove or correct the content as appropriate. Our [asset policy](docs/ASSET_POLICY.md) explains the process; [GitHub's formal copyright channel](https://github.com/contact/dmca) is also available. Free access, attribution and this takedown mechanism do not themselves establish permission.
