# NyayaVault — Build Plan

**Hackathon:** AI for Lawyers, HackIndia 2026 (2 Nov–1 Dec 2026)
**Entrant:** M S Abhishek — Participant ID HI029518, team "MS Abhishek" (solo)
**Track:** AI Legal Research
**Status at writing (8 Nov 2026):** product + docs + tests DONE;
deployment, video, deck and submission NOT started (see below).

## Phase 1 — Research (DONE, 7–8 Nov 2026)

- [x] Read the HackIndia event page + submission rules (deliverables,
      judging weights, tracks, team-size tension).
- [x] Verify the corpus: 16 legal provisions + 1 coverage note,
      every fact checked against India Code / Gazette of India /
      bare-Act text (see `RESEARCH.md`).
- [x] Inspect 5 design references (Indian Kanoon, SCC Online,
      Harvey AI, PRS Legislative Research, CourtListener) — text
      fetch; visual layout honestly noted as unverified.
- [x] Read the ABHI_22 rulebook in full; write the design
      constitution + registry before building.

## Phase 2 — Concept (DONE, 8 Nov 2026)

- [x] `CONCEPT.md`: NyayaVault (Nyaya + Vault), AI Legal Research
      track, judging-weight strategy, the solo-team-size open
      question flagged.

## Phase 3 — Product (DONE, 8 Nov 2026)

- [x] Corpus: 17 Markdown documents in `corpus/`.
- [x] Engine (`nyayavault/`): config, guardrails, index
      (retrieval), llm (mock + BharatCode providers), routing
      (primary/fallback/budget), agent (Q&A + research brief),
      web (single-page app + authority constellation + API),
      wsgi (Vercel entrypoint), cli.
- [x] Design: parchment + oxblood + brass; three-column library
      layout; authority constellation (canvas 2D perspective,
      fixed Act sectors, 12 cross-reference lines, click/arrow-key
      navigation, reduced-motion static fallback, shelves-list 2D
      fallback).
- [x] Sample outputs: 2 generated research briefs + 1 contract
      summary (synthetic, labelled) in `samples/`.
- [x] Tests: 52/52 PASS (Linux sandbox, Python 3.12.3).
- [x] Live server smoke test (localhost): status, ask, refusal,
      document, brief, samples all verified.

## Phase 4 — Deployment (NOT STARTED — next step)

- [ ] Create the public GitHub repo (the HackIndia submission repo
      URL currently 404s: https://github.com/HackIndiaXYZ/
      ai-for-lawyers-hackathon-ms-abhishek — the organisers create
      it, or the team creates it; verify which).
- [ ] Push the code (snapshot-push via the GitHub connector, same
      procedure as the fleet).
- [ ] Deploy to Vercel (proven recipe from NoteVault Bharat /
      SchemeSathi; `vercel.json` + `pyproject.toml` entrypoint are
      already in the repo). Stop if a card is asked for.
- [ ] Verify the live URL: `/api/status` reports 17 provisions,
      mode `[mock]`; ask the three preset questions on the live
      app; confirm the constellation renders.
- [ ] Optional, after a free key exists: set `BHARATCODE_API_KEY`
      on Vercel and re-verify a real-mode answer. (The BharatCode
      student-verification thread is separate; do not block the
      deployment on it.)

## Phase 5 — Demo video (NOT STARTED — needs Phase 4)

- [ ] Record one continuous 60–120 s screen recording of the
      **live** URL (never screenshots/slides): ask the identity-
      theft question, show the citations + ledger, generate a
      research brief, show the refusal demo (DPDP question), spin
      the constellation.
- [ ] Upload to YouTube as Public; link in the submission.

## Phase 6 — Pitch deck (NOT STARTED)

- [ ] 8–10 slides: problem, product, demo, AI workflow, corpus +
      grounding, judging-weight mapping, startup viability, team,
      ask. (The CageCheck deck built 7 Nov 2026 is a format
      reference, not content to copy.)

## Phase 7 — Submission (NOT STARTED — blocked on one question)

- [ ] **Resolve the solo-team-size question FIRST:** the rules say
      teams of 2–5, but the registration is solo (HI029518).
      Clarify with the organisers (contact on the event page:
      +91 9910125804) before submitting. Do not submit as if solo
      were confirmed.
- [ ] Submit: working product (live URL) + sample legal outputs +
      AI workflow explanation (`docs/AI_WORKFLOW.md`) + demo video
      + pitch deck, via the HackIndia team page ("Mark as
      Submitted").
- [ ] No separate submission deadline is stated; the event ends
      1 Dec 2026 — treat that as the working deadline.

## What is deliberately NOT in this build

- No live model key (none exists; none invented).
- No deployment, no video, no deck, no submission (Phases 4–7).
- No case law beyond two verified case notes; no DPDP Act 2023
  (covered by a coverage note that says so).
