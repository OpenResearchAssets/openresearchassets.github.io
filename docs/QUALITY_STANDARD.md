# Research Quality Standard · Edition 01

This is an **editorial rubric**, not a validated psychometric instrument. Reviewer judgments should be traceable to the artifact and its evidence, and aesthetic preferences should be separated from factual issues.

## 1. Scientific faithfulness (non-negotiable)

- **Claim alignment:** figure title, labels, caption and manuscript must describe the same supported claim.
- **Numeric integrity:** no invented values; axes, scales, units, denominator, uncertainty and sample sizes must match source data.
- **Fair comparison:** compare like-for-like controls and report material differences in hardware, settings, baselines or budgets.
- **Causal restraint:** arrows and grouping must not visually imply causality where there is only correlation or architecture adjacency.
- **Image integrity:** no manipulated scientific imagery masquerading as observations; simulated or conceptual illustrations must be labeled.

**Hard-stop:** unsupported claims, material numerical inconsistencies, intentionally misleading transformations and unlicensed reuse cannot be offset by aesthetic quality.

## 2. Communication and narrative

- Can a reader identify the figure's *single main purpose* at a glance?
- Does the reading order follow a natural flow without forcing repetitive backtracking?
- Is every panel necessary to support a distinct claim?
- Is the graphic complementing, rather than reprinting, the manuscript and caption?
- Are abbreviations, notations and roles interpretable without guessing?

## 3. Visual craft

- Aesthetic coherence: controlled palette, limited type scale, consistent stroke and radius vocabulary.
- Visual hierarchy: deliberate emphasis through size, contrast, position and negative space.
- Alignment: meaningful grid, shared baselines and stable spacing rhythm.
- Visual encoding: colors/shapes represent concepts consistently across figures.
- Accessibility: sufficient contrast, color-independent legends, non-tiny essential labels.

Visual language is not prescribed as a single universal style. Minimalism is valuable only when it improves scientific communication; complex evidence sometimes requires dense graphics.

## 4. Publication readiness

- Inspect actual embedded figure on the **compiled final-size PDF**, not just a 4K source image.
- Ensure fonts, arrows, subfigures and tick labels survive print-scale reduction.
- Check margins, vector fidelity, raster source resolution and line weights.
- Check table width, row spacing, typographic hierarchy, alignment, references and page flow.
- Review accessibility requirements and actual target-venue formatting rules.

## 5. Document-level coherence

- Make a **claim → evidence → figure/table** map before selecting visuals for the paper body.
- Check redundant figure/table pairs and identify evidence missing from the main text.
- Keep terminology, semantic colors, panel nomenclature and visual grammar consistent.
- Prioritize space for distinct scientific evidence; do not choose a large figure solely for beauty.
- Test reading rhythm: introduction/teaser → method → experiment → conclusion.

## Context-specific criteria

| Artifact | Essential checks | Common failure modes |
|---|---|---|
| Teaser | Scientific story, focal evidence, fair visual comparison | Dense text, ornamental imagery, claim inflation |
| Method Figure | Distinct module roles, directional information flow, real assumptions | Ambiguous arrows, redundant boxes, opaque symbols |
| Results Figure | Units, baselines, intervals, ordering, data fidelity | Truncated scales, missing `n`, incompatible settings |
| Table | Emphasis, precision, caption completeness, source consistency | Small unreadable font, redundant columns, cryptic notation |
| Writing | Claim sequencing, evidence anchors, clarity and economy | Unsubstantiated conclusions, repetition, overlong problem setup |
| Full Paper | Evidence allocation, cohesion, layout, figure/table balance | Important experiments buried in appendix, redundant figure/table |

## Output of a good review

Each actionable issue should contain:

- **Location:** figure / panel / coordinate region / caption / manuscript section.
- **Observation:** what is directly visible or stated.
- **Concern:** why this materially affects fidelity, comprehension or craft.
- **Issue type:** `factual`, `visual`, `narrative`, `publication`, or `preference`.
- **Priority:** `blocking`, `high`, `medium`, `low` (no global score needed).
- **Evidence / uncertainty:** cite the source or say `needs verification`.
- **Change proposal:** one specific, minimal fix and how to validate it.

### Acceptance gate

Blocking scientific issues must be resolved or explicitly documented; high-priority readability issues must be inspected at target size. Record the remaining known limitations. Do not claim that a model-only review constitutes empirical validation or formal publication approval.

## Use of AI

A VLM can propose diagnostic hypotheses, identify likely clutter or inconsistency, and offer redesign ideas. It cannot establish truth of unseen data. When reviewing a PDF, render and inspect the pages as they will be read. Treat model confidence as uncertainty to report, not as a substitute for evidence.
