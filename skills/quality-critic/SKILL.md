---
name: research-quality-critic
description: Diagnose and improve the quality of scientific figures, tables and manuscript visual narratives. Check scientific faithfulness, clarity, aesthetic craft, editability and final-publication fit. Produce prioritized, evidence-bound design advice rather than generic scores.
license: MIT
---

# Research Quality Critic

This Skill reviews **teasers, method figures, result charts, tables, writing and whole-paper figure organization**. It is a structured reviewing protocol, not proof that an AI can judge all aesthetics or independently validate experimental results.

## User inputs

1. **Artifact:** image, SVG, PPTX, table, or PDF; inspect the actual provided asset. If the artifact is unavailable, ask for it rather than pretending to have evaluated its appearance.
2. **Type:** teaser / method / results / table / manuscript / other.
3. **Scientific context:** research question, precise claim, caption, relevant method and underlying evidence when available.
4. **Publication context:** target venue, single/two column target size, page or slide constraints, intended reader.
5. **Editing goal:** diagnose only, prioritized plan, redesign proposal or source-file revisions.

If optional inputs are absent, proceed with what is available and label uncertain claims. Never invent source data, target margins, numerical measurements or publication requirements.

## Review workflow

### A. First classify the artifact

- What is it attempting to communicate? State its **one-sentence reader takeaway**.
- Is it a scientific result, schematic illustration, visual analogy, reference screenshot or speculative design? Mark the class explicitly.
- Identify what **cannot be checked** without data, text, original source, screenshots or compiled PDF.

### B. Fidelity gate (blocking issues first)

Cross-check numerics, axes, units, conditions, citations, labels, arrow semantics, image authenticity, data comparability and consistency with the manuscript. Unsupported or suspicious claims should be marked **needs verification**, not silently accepted.

### C. Reader-comprehension test

Examine information hierarchy, reading path, redundancy, main-finding visibility, semantic grouping, cross-panel consistency and caption dependence. For each problem, specify **where** it occurs and why it matters.

### D. Visual-craft diagnosis

Inspect typography, contrast, whitespace, alignment, color semantics, stroke weight, balance, focal point, artifact quality and unnecessary decorative content. Separate objective legibility issues from taste-dependent suggestions. A high-quality result may be dense when the content demands it; do not enforce a single minimalist style.

### E. Publication reality check

When a manuscript PDF or layout is available, inspect at the **final intended size**. Check float placement, figure/table duplication, key evidence location, caption distance, tiny labels, excess whitespace, split panels and consistent style. An attractive full-resolution image that fails after downscaling is not publication ready.

### F. Output actionable review

Provide:

1. **Short verdict:** current communication strengths and the single most important obstacle. Do not give an unsupported aggregate numerical score.
2. **Findings:** each as location → observed issue → category → priority → why it matters → minimal fix → validation step. Priorities: blocking / high / medium / low.
3. **Keep / change:** what is already working and must not be damaged by a redesign.
4. **Revision plan:** up to five changes ordered by impact and implementation cost; call out any changes that could alter scientific meaning.
5. **Remaining uncertainty:** which judgments rely on subjective preference or absent evidence.

### G. If asked to revise the artifact

- Preserve scientific content and editable structure; do not substitute a flattened screenshot for an editable SVG/PPTX.
- Favor targeted changes over wholesale redesign of established figures.
- Render the revised result; inspect clipping, alignment, fonts, final dimensions and readability; compare against original.
- Report exactly which files changed and which checks were actually run. Never imply a human or publisher verified the result if they did not.

## Example response contract

```
Artifact: Figure 1 — method overview
Context received: figure + caption; no underlying experiment data
Reader takeaway: [one sentence]

Keep:
- [observed strength]

Issues:
- HIGH · Panel B, lower-left
  Observation: [specific visible issue]
  Consequence: [reader/scientific problem]
  Minimal fix: [concrete edit]
  Verify: [render/logic check]

Unverified:
- [claim or number not checkable from supplied evidence]

Revision order:
1. [highest impact]
2. [next]
```

## For agents with tools

Use available image viewing/rendering tools, document/PDF inspection and data checks rather than judging from file names. No outside service is required by this Skill. If deploying with a remote VLM, disclose to the user where private files are transmitted and obtain suitable approval. Do not create fake before/after examples or claim quality gains not tested with real readers.

Read `../../docs/QUALITY_STANDARD.md` for the detailed first-edition rubric (when installed alongside the repository). This relative link is optional for standalone Skill installation; this file is usable by itself.
