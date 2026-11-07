# NyayaVault — Design References

**Inspected:** 7 Nov 2026, by text fetch (browser.open) from this
environment. Visual layout, colour and motion could **not** be
verified from a text fetch — that limit is stated per reference, not
hidden. Nothing here claims a visual inspection that did not happen.

## 1. Indian Kanoon — same category (legal research, India)

- **URL:** https://indiankanoon.org/
- **Inspected:** homepage text, 7 Nov 2026 (page crawled 4 Nov 2026).
  The fetch returned only the navigation: "API · Browse laws ·
  Browse judgments · Recent judgments · Advanced search" — the
  homepage is JS-heavy and its content did not render in text fetch.
- **What was actually inspected:** the information architecture
  (laws vs judgments vs recent judgments vs advanced search) and the
  product's core promise (a search engine for Indian law).
- **Worth learning:** search-first entry; "Browse laws" and "Browse
  judgments" as separate doors; advanced search as a first-class
  citizen, not a hidden filter.
- **Do NOT copy:** the bare, utilitarian density; the absence of any
  explanation of what a provision means; no citation trail on
  answers.
- **Translation into NyayaVault:** a search-first ask box, but with
  a "what the law says" plain-language layer and a citation on every
  claim — the two things Kanoon does not do.

## 2. SCC Online — same category (legal research, India)

- **URL:** https://www.scconline.com/
- **Inspected:** homepage text, 7 Nov 2026. Headline: "The Surest
  Way to Legal Research!™"; "Authentic and reliable content from
  India's leading law publisher… Spend less time researching, and
  have more time to focus on crafting your arguments." Scale stats:
  600 databases, 6.4M documents, 32M pages, 20+ jurisdictions.
  Brand line: "Rooted in Legacy. Ruled by Authority." — 75 years of
  Supreme Court Cases (SCC) law reports.
- **Worth learning:** authority as the brand (legacy + citation
  counts); the promise is time saved for argument-crafting, not
  search itself; scale numbers used as trust signals.
- **Do NOT copy:** the paywalled, enterprise voice; the "most cited
  law report" authority claim (we cannot claim it); the dense
  product-grid homepage.
- **Translation into NyayaVault:** trust is earned by showing the
  source (Act + section + source URL) on every answer, not by
  claiming authority; the corpus size is stated honestly (17
  documents), never inflated.

## 3. Harvey AI — same category, exceptional interaction model (legal AI)

- **URL:** https://www.harvey.ai/
- **Inspected:** homepage text, 7 Nov 2026. "Build a Frontier Legal
  Organization"; "One Platform for Legal Work"; "Introducing Harvey
  II — smarter agents can now deliver more complex work in exactly
  the way you like it." Impact stats: 25+ hours saved per month,
  200,000+ professionals, 3,500+ legal organisations, 85+ countries,
  80+ AmLaw 100 firms. A "Command Center" tracking adoption, active
  users and product usage.
- **Worth learning:** the platform framing (one place for legal
  work, not one chatbot); agents that deliver work "in exactly the
  way you like it" (output formats as a product feature); measurable
  impact stated as hours saved.
- **Do NOT copy:** the enterprise sales voice; the firm-logo wall;
  the "frontier" hype; any claim of hours saved (we have no such
  measurement).
- **Translation into NyayaVault:** outputs as a product feature —
  the research brief and the contract summary are first-class
  outputs, not chat replies; the grounding ledger is our "command
  center" (a small, honest one: routes attempted, budget used).

## 4. PRS Legislative Research — typography, composition, information hierarchy

- **URL:** https://www.prsindia.org/
- **Inspected:** homepage text, 7 Nov 2026 (crawled minutes before
  the fetch). "Follow the Latest Under: Parliament · Committees ·
  Videos · Blogs · Articles"; "Parliament Today" with dated entries
  (Rajya Sabha adjourned sine-die); long-form explainers (e.g. the
  no-confidence motion, Article 75(3); state laws on exam cheating;
  a Constitution amendment bill to raise the Lok Sabha to 850).
- **Worth learning:** hierarchy by recency + by institution
  (Parliament / Committees / Blogs); the explainer voice — a legal
  development stated plainly, then the provision it rests on
  (Article 75(3) cited in the text); dated, factual, no hype.
- **Do NOT copy:** the newsroom density; the long homepage.
- **Translation into NyayaVault:** the answer format — a short
  plain-language answer first, then the provision it rests on, then
  the citation. The PRS explainer pattern (fact → provision →
  citation) is the shape of every NyayaVault answer.

## 5. CourtListener (Free Law Project) — spatial idea + same category

- **URL:** https://www.courtlistener.com/
- **Inspected:** homepage text, 7 Nov 2026 (page crawled 31 Oct
  2026). "Search millions of legal decisions by case name, topic,
  or citation." 472 jurisdictions. "Latest Opinions" and "Latest
  Oral Arguments" lists with docket numbers and citations. Scale
  stats: 8,300,000 precedential opinions; 10,055 cases added in the
  last ten days; 11,269,475 queries in the last ten days.
- **Worth learning:** citation as the primary key (search by case
  name, topic, **or citation**); free access to primary legal
  materials as a mission; scale stats as transparency, not marketing.
- **Do NOT copy:** the opinion-list homepage; the US-jurisdiction
  focus.
- **Translation into NyayaVault:** the authority constellation —
  CourtListener's world is a citation network, and NyayaVault shows
  its small corpus as one: Acts as clusters, sections as stars,
  cross-reference lines (Article 19 → Shreya Singhal → s. 66A void).
  The 3D/spatial view is a map of authorities, not decoration.
  Scale is stated honestly (17 documents), never inflated.

## Technique reference (3D implementation)

- **Proven in-workspace:** the canvas 2D perspective-projection
  galaxy in `~/workspace/hackathons/bharatcode/notes_bharat/web.py`
  (inspected directly, 8 Nov 2026) — deterministic layout, drag to
  rotate, click to open, arrow-key navigation, reduced-motion static
  fallback, 2D list fallback. NyayaVault reuses the **technique**
  (not the visual identity): same projection maths, new data
  (authorities, not notes), new palette, new layout.
- **three.js examples** (https://threejs.org/examples/) was fetched
  7 Nov 2026 but returned only the page title — the gallery is
  JS-rendered and its content did not render in text fetch. It is
  **not** claimed as an inspected reference; the canvas technique
  above is the actual implementation reference. WebGL was evaluated
  and rejected: the corpus is 17 documents and the effect needed is
  depth, not a model viewer — a dependency would add weight for no
  product gain.
