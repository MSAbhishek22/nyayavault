# NyayaVault — Design Constitution

> Written 8 Nov 2026 as a Rulebook Gate A document, from the UI as
> it actually exists in `nyayavault/web.py` (single-page HTML, inline
> CSS, canvas constellation, no external assets, no CDN, no custom
> fonts). Nothing in this file claims a design that is not in the
> code. Where the current UI falls short of the Rulebook, that is
> stated as a gap, not papered over.

## Product personality and emotional tone

A law library at first light: quiet, serious, warm. The product's
promise is "your first legal question, answered from the statute
itself". Tone in copy: plain, factual, careful — never hype, never
legalese for its own sake. The mock badge is deliberately loud
(amber) so a mock answer can never be mistaken for a live one, and
the refusal box is red-bordered so "I don't know" is unmissable.
Every answer carries the sentence "This is general legal
information, not legal advice."

## Target user, environment, context of use

A solo Indian student / citizen / small-business owner with a legal
question and no lawyer on call, working on a laptop or phone
browser. The judge/demo viewer is the primary audience: they must be
able to see, in one screen, the question, the grounded answer, its
citations, and the grounding ledger. The CLI is the secondary
surface (same agent, same rules).

## Visual metaphor / central design idea

**A law library with an authority constellation above the desk.**
The shelves (left rail) hold the four Acts; the desk (centre) is
where you ask and where the answer lands, with its citations pinned
to it like exhibit tags; the ledger (right rail) is the clerk's
record of what was consulted and what it cost. Above the desk hangs
the constellation: Acts as clusters, sections as stars, lines as
cross-references. The constellation is not decoration: it is the
spatial map of the corpus (which provisions exist, how they connect),
and clicking a star opens the provision. The routing ledger is the
audit trail under the desk lamp.

## Colour palette (semantic roles, from `web.py` — exact values)

| Role | Value | Used for |
|---|---|---|
| Oxblood / courtroom wood | `#5c1a24` | Hero, header accents, primary buttons |
| Oxblood deep | `#3f1119` | Hero gradient base, constellation canvas |
| Parchment | `#f7f1e3` | Page background |
| Card | `#fffdf6`, border `#e2d9bd`, radius `14px` | Ask / shelves / ledger cards |
| Brass accent | `#b08d3c` | Stars, highlights, meter fill, focus outlines |
| Brass deep | `#8a6d2b` | Meter fill |
| Ink text | `#23201b` | Body text |
| Muted text | `#6b6455` | Small print, footnotes |
| Primary button | `#5c1a24` bg, `#fff` text, radius `10px` | Ask |
| Secondary button | `#fff` bg, `#5c1a24` text | Presets |
| Mock badge | bg `#ffe8c2`, text `#7a3e00` | `[mock]` |
| Real badge | bg `#dcefd8`, text `#145214` | `real BharatCode` |
| Citation chip | bg `#f3e9c8`, border `#d9c48a` | Source provision titles |
| Refusal / error | border `#a62b2b`, bg `#fdf0f0` | Grounded refusal, API errors |
| Answer block | bg `#fbf6e8` | Answer text |
| Grounded answer marker | `#2e6b3a` | "Grounded" label on cited answers |
| Star colours (per Act) | `#e8c268` Constitution, `#8fce7a` IT Act, `#8fb7d9` CPA, `#d98f8f` Contract Act, `#a89f8d` coverage note (grey — a boundary marker, not a provision) | One per Act (fixed, not hashed); brightened from the page palette so stars read on the dark oxblood canvas |

No gradients except the hero, no glassmorphism, no glow, no
floating blobs. The restraint is intentional and matches the library
metaphor.

## Typography and type hierarchy

- **Display:** Georgia serif for the title and card headings — a
  bookish, library voice. (A loaded web font was considered and
  rejected: no external dependency; Georgia is on every machine.)
- **Body/UI:** `system-ui, -apple-system, "Segoe UI", Roboto,
  "Noto Sans", sans-serif` — Noto Sans in the stack so Devanagari
  (हिन्दी) renders correctly on systems that have it.
- **Hierarchy:** hero `h1` 2em serif → card `h3` serif → body →
  `small` muted footnotes. Answer text is rendered in `<pre>` with
  wrapping, inherited font (not monospace — answers are prose, and
  Hindi in monospace renders poorly).
- Gap vs Rulebook: no loaded web font, so the type system is
  size/weight/serif-vs-sans only. Accepted: the product is a tool,
  and offline rendering matters more than a display face.

## Layout grid, spacing, composition

- Page: `max-width: 1160px`, centred, hero full-bleed above.
- Hero: centred, 32px top padding, title + tagline + one-paragraph
  pitch + the "not legal advice" line.
- Constellation card: full-width, 300px canvas, oxblood background,
  rounded 14px. Below it, a three-column grid (`0.9fr / 1.6fr /
  1fr`): Statute shelves | Ask + answer | Grounding ledger.
  Tablet/mobile (`≤900px`): single column, shelves first, then ask,
  then ledger.
- No sidebar navigation, no multi-page routing: the page is a single
  route (`/`), and that is the whole product surface.

## Navigation and information architecture

- One route: `/`. Information architecture is hero → constellation
  → shelves → ask → answer → ledger. The mode bar (`[mock]` badge +
  API/model line) sits between hero and constellation.
- API routes (not navigation): `GET /`, `GET /api/status`,
  `GET /api/document?path=`, `POST /api/ask`, `POST /api/brief`,
  `POST /api/organise`, `POST /api/reset-budget`.

## Component behaviour and interaction patterns

- Ask: question input + language select (en/hi/hinglish) + Ask
  button + three preset buttons (identity theft, free speech,
  refusal demo). Asking shows "Consulting the corpus…" then the
  answer, citation chips, mode badge and language chip. Refusal
  renders a red-bordered "No grounded answer" box with the refusal
  text.
- Research brief: a "Generate research brief" button on an answered
  question, producing a structured brief (question, short answer,
  what the law says with citations, what is not covered, next steps)
  in a `<pre>` block; a "Download brief" button downloads it as a
  `.md` file.
- Constellation: pointer drag rotates (Y + slight X, clamped
  ±0.6 rad); click / tap a star opens its provision in the preview;
  arrow keys rotate when the canvas is focused; Enter opens the
  selected star; auto-rotate every 50ms (+0.004 rad) unless
  `prefers-reduced-motion` — then static.
- Shelves list: grouped by Act; click or Enter opens the preview;
  hover highlights. This list is the 2D fallback for the
  constellation — every constellation action is doable here.
- Ledger panel: API, mode label, chosen model + reason, fallback
  chain, attempted routes, fallback-used warning, or "No API call
  made" on refusal. Budget: meter + used/limit + exhausted state +
  reset button.
- All buttons have `:focus-visible` brass outlines; all inputs have
  labels; the canvas has an `aria-label` describing keyboard use.

## Motion language

Slow, dignified, restrained: the sky drifts (auto-rotate), stars do
not twinkle, nothing bounces. Drag rotation is 1:1 with the pointer.
Motion communicates "this is a map you can turn", nothing else.
Reduced-motion users get a static sky with full list access.

## 3D concept and its connection to the product's purpose

The constellation is the corpus's map. A flat list hides structure;
the constellation shows it: four Acts as clusters, seventeen
provisions as stars (sixteen legal provisions plus one grey coverage
note marking what the corpus does not contain), and cross-reference
lines that teach the law's shape (Article 19 → *Shreya Singhal* →
s. 66A void; Article 21 → identity theft provisions; Contract Act
s. 10 → s. 73). Act clusters
are fixed sectors (not hashed), so the same corpus always renders
the same sky and a returning user can read it. Implementation:
canvas 2D with a perspective projection (focal length 420), no
dependency, no WebGL — the data is 17 documents and the effect is
depth, not a model viewer. Fallbacks: reduced-motion → static
render; no canvas / no pointer → the shelves list below (always
rendered). Performance: trivial at this size; the draw is one pass
over projected points. Keyboard alternative: arrow keys + Enter,
plus the fully keyboard-accessible list.

## Responsive behaviour

- Desktop: hero + constellation + three-column grid.
- Tablet/mobile (`≤900px`): single column; constellation canvas
  scales to container width (1000×300 internal resolution, CSS
  width 100%). Touch: pointer events handle drag + tap.
- No horizontal overflow: the grid collapses, inputs are 100%
  width, `pre` wraps.

## Accessibility and reduced-motion behaviour

- `prefers-reduced-motion: reduce` → auto-rotate off, static sky.
- Focus visible everywhere (brass outline). Labels on every input.
- Canvas has `tabindex="0"` + `aria-label` with keyboard
  instructions.
- Colour is never the only signal: the mock badge has text, the
  fallback warning has text, the selected star has a white ring + a
  text line naming the selected provision; refusal has text, not
  just colour.
- Contrast: ink on parchment and parchment on oxblood both pass at
  body sizes; muted `#6b6455` on parchment is used only for small
  print.

## Reference links and original design decisions

- References: see `design/DESIGN_REFERENCES.md` (Indian Kanoon, SCC
  Online, Harvey AI, PRS Legislative Research, CourtListener).
- Original decisions: parchment + oxblood + brass (not NoteVault
  Bharat's ink navy + marigold on cream, not Digest Room's slate +
  lime, not Spec Ghost's near-black candlelit document); a
  three-column library layout with statute shelves and a grounding
  ledger (not a hero + galaxy + two-column grid); an authority
  constellation with fixed Act sectors and cross-reference lines
  (not a tag-hash galaxy); serif display type kept, but the
  interaction is turning a map of authorities, not spinning notes.
