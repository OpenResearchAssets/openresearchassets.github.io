# OpenResearchAssets — reusable research assets for humans and AI

**[简体中文](README.md) · English · [Website](https://openresearchassets.github.io/) · [For AI agents](https://openresearchassets.github.io/for-agents/)**

Research assets should be more than bookmarks. They should tell us **when to use them, what transfers, what to avoid, and where they came from**.

## Mission and intended use

**Our long-term goal is to make research experience directly usable by AI agents.** Given a task and one OpenResearchAssets URL, a web-capable agent should be able to discover relevant, trustworthy research lessons, tools, editable assets, and actionable workflows across the research lifecycle—from ideation and literature review to methods, experiments, evaluation, writing, websites, and release—without repeated manual searches or elaborate instructions. Using the assets in a real project still requires appropriate file and tool permissions.

We are **not merely a gallery of attractive paper figures or a directory of links**. Each curated asset should state when to use it, what can be learned or reused, how to apply it, its scientific and licensing constraints, provenance, and how to verify the result. The goal is to reduce repeated searching, prompting, trial-and-error, human corrections, elapsed time, and unnecessary tokens. Success must be measured on real tasks by relevance, outcome quality, intervention count, time, and token usage—not by collection size alone.

The initial focus is AI, computer vision, robotics and research communication. Full-lifecycle support is an ambition, **not a claim that an autonomous research service is already deployed**.

## Open community trajectory (long-term vision)

OpenResearchAssets is an **independent open-source project**, not a personal portfolio. Its intended progression is: **(1)** a useful project that researchers discover and reuse; **(2)** a healthy community where independent researchers contribute and review assets, methods, and tools; **(3)** open research infrastructure with interoperable asset conventions, workflows, tools, and AI agents.

![Three-stage OpenResearchAssets community vision (Chinese-first source SVG)](assets/diagrams/community-trajectory.svg)

These are **aspirational stages, not shipped features or promised milestones**. We value verified reuse, scientific fidelity, source attribution, contributor retention, and transparent review more than stars alone. [Star the repository](https://github.com/OpenResearchAssets/openresearchassets.github.io), [contribute](CONTRIBUTING.md), or [propose an asset](https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/new/choose). The [project strategy](docs/PRODUCT_STRATEGY.md) is the authoritative statement of current and future scope.

This Chinese-first, English-supported library spans research design, evaluation, writing and communication. The current public implementation includes:

- **22 structured entries** in [catalog/index.json](catalog/index.json), including separate teaser and project-site references for RoboRender, RoboDojo and SuperMimic.
- Browser-side search and facets for stages, domains and asset kinds, with per-asset usage and provenance pages.
- [Agent instructions](for-agents/) and [llms.txt](llms.txt) pointing to an openly readable machine catalog. These files do **not** mean there is an autonomous remote agent service.
- Four original Markdown research workflows covering literature, experiments, paper narratives and research release.
- Five original, editable SVG concept designs; an author-guided manual [quality checklist](quality.html); and an unvalidated [Quality Critic Skill](skills/quality-critic/SKILL.md).

Search the [interactive asset directory](https://openresearchassets.github.io/#references), or hand its URL to an agent that has web or file-reading capability. The JSON requires HTTP hosting; run \`python3 -m http.server 8000\` locally rather than opening the page with \`file://\`.

**Copyright:** Third-party paper figures, videos and website screenshots are not bundled or relicensed; visual previews without explicit authorization are locally authored structural diagrams, clearly labeled. The diagrammatic previews are **not** source figures. Our original SVG templates are CC BY 4.0; the code and Skill are MIT. See [asset policy](docs/ASSET_POLICY.md), [schema](docs/ASSET_SCHEMA.md), [contribution guide](CONTRIBUTING.md) and [AI maintenance rules](AGENTS.md).

**Current limitations:** no vector semantic search, no automated image review model, no remote autonomous research execution service, and no validated paid products. We do not present future features as shipped.

## Low-token AI catalog access

Agents should first read [the compact manifest](catalog/manifest.json), select a few relevant assets by task, stage and domain, then open only the corresponding [per-entry JSON files](catalog/entries/supermimic-teaser.json). The full [canonical catalog](catalog/index.json) remains the only authored data. Edit it, run `python3 tools/sync_catalog.py`, then `python3 tools/sync_catalog.py --check` before publishing. This is not a remotely executing AI service.

## Authentic, specifically verified source images

The three featured papers are represented by their **actual Figure 1** and the corresponding project-site references use actual homepage viewport screenshots. All six media files live in [the third-party ledger](assets/third-party/manifest.json), with precise origin, credit, capture date and transformations. The RoboRender paper figure carries CC BY 4.0 attribution; other previews retain source-owner rights and a correction/removal channel.

## Real-reference previews

Depth Anything 3 and third-party galleries link to original source images. All six featured RoboRender/RoboDojo/SuperMimic paper/site references instead have individually verified local previews. The discontinued RoboRender model-architecture record is not part of the current catalog.

### Verified paper figures versus genuine first-view website captures

The six featured RoboRender/RoboDojo/SuperMimic references now use their actual paper Figure 1 images and actual screenshots of each project's first website viewport, respectively. We do not substitute training-data charts for teasers, GPU decorations for scientific paper figures, or broken author-portfolio links for website captures. Each image records the source, original credit, processing and removal request channel; authored editorial SVG analyses remain optional detail-page aids.
