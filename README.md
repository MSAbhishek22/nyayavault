<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:1f6feb,100:8957e5&height=190&section=header&text=NyayaVault&fontSize=44&fontColor=ffffff&animation=fadeIn&desc=Grounded%20AI%20legal%20research%20over%20real%20Indian%20law&descSize=16"/>

> **📖 The Story** Ask a generic AI a legal question and it may quote a section that doesn't exist — in law, a confident wrong answer is worse than no answer. NyayaVault was built for AI for Lawyers (HackIndia), and later submitted to SLAY, to do legal research the slow, honest way: grounded in the actual texts of Indian law.
>
> **🎯 The Problem** People facing a legal question need research they can verify against the statute itself, not hallucinated sections and invented case law.
>
> **👥 Who It's For** Lawyers, law students, and citizens trying to understand their rights before they pay for advice.
>
> **🔑 The USP** Research grounded in real Indian law — the Constitution, the IT Act, the Consumer Protection Act and the Contract Act — instead of a model's memory.
>
> **🚀 What's Next** Wider coverage of Indian statutes and deeper citation checking on every answer.
>
> **🔗 Live: [nyayavault-iota.vercel.app](https://nyayavault-iota.vercel.app) · 🎥 Demo: [YouTube](https://youtu.be/by4iPbj2i5w)**

---

# NyayaVault — Your first legal question, answered from the statute itself

**AI for Lawyers, HackIndia 2026** · Track: **AI Legal Research** · Prize pool: **₹2,00,000**
**Entrant:** M S Abhishek — Participant ID **HI029518**, team "MS Abhishek" (solo)

NyayaVault is a legal research assistant that answers plain-language
questions from a small, verified corpus of Indian law — and says
plainly when the corpus has no answer. Every answer cites the Act
and section it comes from. It never invents a case, a section number,
or a judgment.

> **General legal information, not legal advice.** Every answer and
> every sample output says so.

## The corpus (17 documents, all verified)

- **Constitution of India** — Articles 14, 19, 21, 32 (+ case notes:
  *Shreya Singhal* (2015) 5 SCC 1, *Anuradha Bhasin* (2020) 3 SCC 637)
- **Information Technology Act, 2000** — ss. 43, 66, 66C, 66D, 79
  (+ a note that s. 66A is **void**)
- **Consumer Protection Act, 2019** — ss. 2(7), 2(9), 34, 35, 69
- **Indian Contract Act, 1872** — ss. 2(h), 10, 73
- **Coverage note** — the DPDP Act 2023 is **not** in the corpus,
  stated explicitly so a question about it gets a grounded
  "not covered" answer instead of a guess.

Every fact was verified against India Code, the Gazette of India, or
bare-Act text. See `RESEARCH.md` for the verification table.

## Run it locally

```bash
python3 run.py
# open http://localhost:8000/
```

Stdlib only — no dependencies, no key needed. Without
`BHARATCODE_API_KEY` the app runs in clearly labelled `[mock]` mode
(deterministic, offline, extractive). With a key in the environment,
it uses the BharatCode model API (`qwen-3.8-27b`, fallback
`deepseek-v4.1-flash`) behind the same interface.

```bash
# Ask from the CLI
python3 -m nyayavault.cli ask "Someone stole my password and used my bank account."
python3 -m nyayavault.cli brief "Can the government shut down the internet?" --out brief.md
python3 -m nyayavault.cli list
```

## How it works

1. **Guardrails** — secrets, passwords, tokens, card numbers and
   12-digit personal numbers are refused before anything leaves
   the machine.
2. **Retrieval** — keyword search over the local corpus (title ×3,
   tag ×3, whole-word body ×1; stopwords filtered; minimum score 2;
   needs score ≥ 5 or ≥ 2 distinct words).
3. **Grounding** — the provider answers only from the retrieved
   provisions; every answer carries citations and a mode badge.
4. **Refusal** — no hit, or a coverage-note hit, means a grounded
   refusal. A refusal costs no budget and is shown in red.
5. **Routing** — primary model first, fallback once, per-run
   budget of 10 attempts; the ledger shows what was tried.

See `docs/AI_WORKFLOW.md` for the full explanation.

## The app

- **Ask** — question + language (English / Hindi / Hinglish) +
  three presets (identity theft, free speech online, refusal demo).
- **Authority constellation** — the corpus as a map: four Acts as
  clusters, provisions as stars, 12 cross-reference lines. Drag to
  turn it; click a star to read its provision. The statute shelves
  below work the same way (the 2D fallback).
- **Research brief** — generate a structured brief from any answer
  and download it as Markdown.
- **Sample outputs** — two generated research briefs and a contract
  summary (synthetic, labelled) in `samples/`.
- **Grounding ledger** — model, reason, attempted routes, fallback,
  budget meter.

## Tests

```bash
python3 -m unittest discover -s tests
# 52 tests, all passing (Linux sandbox, Python 3.12.3)
```

## Status (Rulebook gates — honest)

- Gate A (Research & design): PASS — corpus verified, 5 design
  references inspected, constitution + registry written.
- Gate B (Functional product): PASS — app built, all controls
  inventoried, 52/52 tests pass.
- Gate C (3D & visual quality): PASS — authority constellation
  implemented; 2D fallback is the statute list.
- Gate D (QA): PASS — automated tests + interaction inventory.
- Gate E (GitHub & deployment): **BLOCKED** — no repo yet, no live
  deployment.
- Gate F (Demo video): **BLOCKED** — needs a live deployment first.
- Gate G (Final handoff): **BLOCKED** — needs E and F.
- **OVERALL_RELEASE: IN_PROGRESS**

## ⚠️ Open question — solo team size

The HackIndia rules say teams of **2 to 5 participants**, but the
registration is **solo** (1 member, HI029518) and was accepted.
Solo compliance is **not confirmed** — clarify with the organisers
(contact on the event page: +91 9910125804) before submitting.

## Files

| Path | What it is |
|---|---|
| `CONCEPT.md` | Concept, name justification, judging-weight strategy |
| `RESEARCH.md` | Corpus verification table + sources |
| `BUILD_PLAN.md` | Phases 1–7, what is done and what is not |
| `design/` | Design references, constitution, registry |
| `corpus/` | 17 verified legal documents |
| `nyayavault/` | The app (stdlib only) |
| `samples/` | 3 sample legal outputs |
| `docs/AI_WORKFLOW.md` | AI workflow / model explanation |
| `qa/INTERACTION_INVENTORY.md` | Every control, and whether it works |
| `submission/` | Submission draft + release card |
| `deployment/` | Deploy runbook + release manifest |
