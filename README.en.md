# OpenResearchAssets — reusable research assets for humans and AI

**[简体中文](README.md) · English · [Website](https://suchenl.github.io/OpenResearchAssets/) · [For AI agents](https://suchenl.github.io/OpenResearchAssets/for-agents/)**

Research assets should be more than bookmarks. They should tell us **when to use them, what transfers, what to avoid, and where they came from**.

This Chinese-first, English-supported library spans research design, evaluation, writing and communication. The current public implementation includes:

- **15 structured entries** in [catalog/index.json](catalog/index.json), including separate teaser and project-site references for RoboRender, RoboDojo and SuperMimic.
- Browser-side search and facets for stages, domains and asset kinds, with per-asset usage and provenance pages.
- [Agent instructions](for-agents/) and [llms.txt](llms.txt) pointing to an openly readable machine catalog. These files do **not** mean there is an autonomous remote agent service.
- Three original, editable SVG concept diagrams; an author-guided manual [quality checklist](quality.html); and an unvalidated [Quality Critic Skill](skills/quality-critic/SKILL.md).

Search the [interactive asset directory](https://suchenl.github.io/OpenResearchAssets/#references), or hand its URL to an agent that has web or file-reading capability. The JSON requires HTTP hosting; run \`python3 -m http.server 8000\` locally rather than opening the page with \`file://\`.

**Copyright:** Third-party paper figures, videos and website screenshots are not bundled or relicensed; visual previews without explicit authorization are locally authored structural diagrams, clearly labeled. The diagrammatic previews are **not** source figures. Our original SVG templates are CC BY 4.0; the code and Skill are MIT. See [asset policy](docs/ASSET_POLICY.md), [schema](docs/ASSET_SCHEMA.md), [contribution guide](CONTRIBUTING.md) and [AI maintenance rules](AGENTS.md).

**Current limitations:** no vector semantic search, no automated image review model, no remote autonomous research execution service, and no validated paid products. We do not present future features as shipped.
