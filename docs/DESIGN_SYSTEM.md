# Website design system — current canonical direction

The visual reference direction is **SuperMimic × Apple**: research evidence and concise claims, combined with precise product typography and cool-neutral whitespace. This is an editorial interpretation, not a copy of either site's artwork or markup.

## Hard visual rules

- Use **white** `#FFFFFF` for the page; light neutral `#F6F8FB` for secondary surfaces. Do not use ivory, yellow-beige or cream as primary backgrounds.
- Use graphite `#12161D` for main text; muted slate `#586273`; cool blue `#2C5DB2` only for interaction/emphasis. Deep navy `#111827` is reserved for one strong focus section.
- Use the native system sans-serif stack. Headlines are bold and closely tracked. Avoid faux luxury flourishes, italic serif headings, warm accent dots or oversized ornamental letterspacing.
- Favor editorial section spacing, well-framed real research artifacts, clear captions and modest rules; avoid ornamental cards, fake 3D mockups, stock-looking gradients and abstract thumbnails presented as source figures.
- SuperMimic informs the **narrative**: one concise headline and supporting evidence. Apple informs restrained typography, whitespace and alignment. Never clone their distinctive artwork or content.
- Keep first-edition claims accurate: **3** original SVG design studies, **8** external references, **5** guided review categories. The local Quality Critic is **manual**, not an AI judging model. No invented performance metrics, testimonials or logos.
- Verify desktop 1440px, tablet 768px and mobile 390px, image legibility, menu keyboard behavior, interaction states and no horizontal overflow.

## Maintenance

`css/site.css` contains the existing layout and shared components; `css/design.css` is the current canonical visual layer loaded second. When refactoring, consolidate rather than proliferating versions. The `v2` basename describes the historical migration; new styling should update this layer rather than adding another numbered stylesheet. Original template source artwork may use more colors; do not silently recolor third-party work or trade scientific meaning for monochrome branding.
