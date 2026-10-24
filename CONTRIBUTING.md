# Contributing to OpenResearchAssets

We care more about **one exceptional, useful contribution** than fifty unreviewed links. Contributions are welcome from researchers, designers and research engineers.

## Contributions we accept

- **Excellent external reference:** canonical source URL, original author/project, one focused design observation, why it helps researchers and its likely context.
- **Original editable asset:** SVG / HTML / source PPTX / reproducible code with preview, edit instructions, clear ownership, explicit license and the distinction between conceptual and empirical content.
- **Quality example:** permission-cleared before/after artifact with a concrete problem, minimal intervention and validated improvement.
- **Quality Standard / Skill improvements:** a test case, failure mode, proposed change and, ideally, a reproducible example.

## Quality bar

1. **Scientific fidelity:** no altered experiments, numbers, uncertainty, hidden context or misleading comparisons.
2. **Communication:** reviewer can state the unique scientific information conveyed.
3. **Visual craft:** high-quality typography, contrast, spacing and final-size legibility.
4. **Editability:** editable means genuine individual shapes and text, not a giant embedded image.
5. **Provenance:** original author and permission; don't mirror protected paper figures or proprietary fonts.
6. **Privacy:** no private manuscripts, internal reports, unpublished lab assets or repository details without permission.

## Submit an external reference

Edit `data/references.js`. Reuse the existing keys and choose `Research`, `Gallery`, or `Toolkit` for category. Include a concise, grounded design note; avoid empty superlatives like “very beautiful.” External materials should be **linked, not copied**. Open a pull request explaining the design principle others can learn.

## Submit an original template

- Add a uniquely named editable SVG in `assets/templates/`.
- Export a PNG preview to `assets/previews/` (matching base filename).
- Verify editing in an SVG-capable editor; inspect final size and typography.
- Confirm licensing and author credit in the PR description; contributions in the original template collection are licensed CC BY 4.0.
- Explicitly mark non-empirical illustrations and placeholders.

## Review process

Maintainers check provenance and scientific correctness first, then information structure, visual execution and compatibility. PR feedback must be specific and respectful. If a submission is rejected, provide actionable reasons; prefer revisions over vague taste judgments. Aesthetic diversity is welcome — the goal is fidelity and craft, not a single house style.

## Before making a PR

```bash
python3 tests/check_project.py
```

No private implementation or material is included or required. Repository maintainers reserve the right to remove material with unresolved ownership or scientific-integrity problems.
