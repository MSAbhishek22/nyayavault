# NyayaVault — Concept

**Hackathon:** AI for Lawyers, HackIndia (virtual, free, 2 Nov–1 Dec 2026)
**Prize pool:** ₹2,00,000 (verified on the official event page,
test.hackindia.org/2026/ai-for-lawyers-hackathon)
**Entrant:** M S Abhishek — Participant ID **HI029518**, team
"MS Abhishek", registered solo on 7 Nov 2026
**Track:** **AI Legal Research** (chosen from Contract Drafting, Legal
Research, Compliance & Risk, Legal Assistants, Access to Justice)

## The name

**NyayaVault** — *Nyaya* (न्याय, "justice") + *Vault*.

The Vault half is deliberate lineage: this is the NoteVault engine
(grounded Q&A over a corpus you own, citations on every answer,
grounded refusal instead of a guess), pointed at a new corpus — the
law itself. The Nyaya half says whose law: Indian law, in Indian
languages, for Indians who cannot afford a lawyer for a first
question.

## The problem (one paragraph)

Most Indians meet the law only when something has already gone
wrong — a password stolen, a seller who will not refund, a contract
signed without reading it. The statutes that answer those questions
are public and free, but they are written in legal English, scattered
across four Acts, and the free search tools return judgments without
explaining which section actually applies. People either guess, or
pay, or do nothing. NyayaVault answers the first question from the
statute itself, shows the exact section, and says plainly when the
corpus has no answer.

## What the product is

A legal research assistant web app. You ask a question in plain
English, Hindi or Hinglish. The app:

1. Searches a small, verified corpus of real Indian legal texts
   (Constitution, IT Act 2000, Consumer Protection Act 2019, Indian
   Contract Act 1872 — 17 documents (16 legal provisions + 1
   coverage note), every fact verified against an official or Gazette
   source; see `RESEARCH.md`).
2. Answers **only from the retrieved provisions**, with a citation
   (Act + section) on every claim.
3. **Refuses groundedly** when the corpus has no answer — no guess,
   no invented section number, no invented case.
4. Shows its work: a grounding ledger (which provisions were used,
   which model route was taken, how much budget was used) and an
   "authority constellation" — a spatial map of the corpus where Acts
   are clusters, sections are stars, and lines are cross-references
   (e.g. Article 19 → *Shreya Singhal* → IT Act s. 66A, void).
5. Produces sample legal outputs from the same corpus: research
   briefs and a contract summary, each with citations.

The app is **legal information, not legal advice**. That sentence is
on every screen that gives an answer, and on every sample output.

## Why this track, and how the judging weights are answered

| Weight | Criterion | How NyayaVault answers it |
|---|---|---|
| 25% | AI Utilization Depth | Grounded retrieval + citation + grounded refusal; visible routing (model, fallback, attempts); a mock engine behind the same interface as the real BharatCode provider, so the AI is real infrastructure, not a demo prop. |
| 20% | Product Innovation | The authority constellation (a spatial map of the law) and the grounding ledger — the answer and its evidence are one object, not an answer with a footnote. |
| 15% | Execution Speed | Built in days on the proven NoteVault engine (52/52 tests on the BharatCode sibling); corpus verified in one research pass; no new infrastructure invented. |
| 20% | Startup Viability | India has ~1.4 billion people and a vast legal-aid gap; a free, grounded first answer is a real product wedge (freemium: free research, paid drafting/review later). |
| 10% | UI/UX | A law-library identity (parchment, oxblood, brass) that is recognisably different from the fleet; every control works; 390px mobile layout; reduced-motion respected. |
| 10% | Pitch & Storytelling | "Your first legal question, answered from the statute itself" — a relatable story (stolen password, refused refund, unread contract), told with real outputs. |

## What the product is NOT

- Not a lawyer. Not legal advice. Not a case-law database (no
  judgments in the corpus except two verified case notes).
- Not a hallucinating chatbot: if the corpus does not contain the
  answer, the product refuses. That refusal is a feature, and it is
  demonstrated in the demo.
- Not a resubmission of NoteVault Bharat: same engine family, new
  corpus, new product, new design, new hackathon. The reuse is
  engineering (retrieval, grounding, refusal, routing), not the
  submission.

## Engine honesty

- **Today:** local keyword retrieval + a deterministic mock provider
  behind the same interface as the real provider. Every mock answer
  is labelled `[mock]`. The live model wiring comes later, after a
  free key exists — no key is invented, no key is in the repo.
- **Later (same interface):** the BharatCode model API
  (`BHARATCODE_API_KEY` from the environment only), default model
  `qwen-3.8-27b`, fallback `deepseek-v4.1-flash` — the same provider
  shape the BharatCode sibling already runs in production.

## ⚠️ Open question — solo team size (must be resolved before submission)

The HackIndia event page says teams of **2 to 5 participants**, but
M S Abhishek is registered **solo** (1 member, Participant ID
HI029518) and the registration was accepted. Solo compliance is **NOT
confirmed** by the page. Before submission, clarify with the
organisers (contact on the event page: +91 9910125804) whether a
one-person team may submit. Do **not** submit as if solo were
confirmed, and do **not** add a teammate without the user's decision.

## Status (Rulebook gates — honest)

- Gate A (Research & design): PASS — corpus verified, 5 design
  references inspected, constitution + registry written.
- Gate B (Functional product): PASS — app built, all controls
  inventoried, tests pass (see `submission/RELEASE_CARD.md`).
- Gate C (3D & visual quality): PASS — authority constellation
  implemented; 2D fallback is the statute list.
- Gate D (QA): PASS — automated tests + interaction inventory.
- Gate E (GitHub & deployment): **BLOCKED** — no repo yet (the
  HackIndia submission repo URL currently 404s), no live deployment.
- Gate F (Demo video): **BLOCKED** — needs a live deployment first.
- Gate G (Final handoff): **BLOCKED** — needs E and F.
- **OVERALL_RELEASE: IN_PROGRESS** (not COMPLETE; not claimed otherwise).
