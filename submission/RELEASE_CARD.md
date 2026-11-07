# NyayaVault — Release Card

**Project:** NyayaVault (AI for Lawyers, HackIndia 2026)
**Entrant:** M S Abhishek — Participant ID HI029518, team "MS Abhishek" (solo)
**Track:** AI Legal Research
**Date:** 8 Nov 2026
**OVERALL_RELEASE: IN_PROGRESS** (not COMPLETE; not claimed otherwise)

## Rulebook gates

| Gate | Result | Evidence |
|---|---|---|
| A — Research & design | PASS | `RESEARCH.md` (17-document verification table); `design/DESIGN_REFERENCES.md` (5 references inspected); `design/DESIGN_CONSTITUTION.md`; `design/PROJECT_DESIGN_REGISTRY.md` (UI_DISTINCTIVENESS: PASS) |
| B — Functional product | PASS | App built (`nyayavault/`), 17 provisions load, ask/brief/samples/document/status/reset endpoints all verified live on localhost |
| C — 3D & visual quality | PASS | Authority constellation implemented (canvas 2D perspective, fixed Act sectors, 12 cross-reference lines, click/arrow-key navigation); 2D fallback is the statute shelves list. **Not verified in a real browser yet** — canvas visuals and 390px layout need a browser check after deployment. |
| D — QA | PASS | 52/52 automated tests PASS (Linux sandbox, Python 3.12.3); `qa/INTERACTION_INVENTORY.md` — no dead buttons |
| E — GitHub & deployment | **BLOCKED** | No repo yet (HackIndia submission repo URL currently 404s); no live deployment |
| F — Demo video | **BLOCKED** | Needs a live deployment first (video must be recorded from the live URL) |
| G — Final handoff | **BLOCKED** | Needs E and F |

## Test receipt

- **Command:** `python3 -m unittest discover -s tests`
- **Result:** 52 tests, 0 failures
- **Environment:** Linux sandbox, Python 3.12.3, stdlib only
- **Date:** 8 Nov 2026
- **Live server smoke test:** `python3 run.py` on localhost — status,
  ask (grounded + refusal), document, brief, samples, reset-budget
  all returned 200 with correct payloads.

## Known honest limits

- Mock mode today: answers are extractive corpus sentences, labelled
  `[mock]`. No live model key exists; none is invented.
- No real browser render verified (canvas visuals, mobile layout).
- Hindi/Hinglish answers in mock mode are English extracts.
- The solo-team-size question is unresolved (rules say 2–5, the
  registration is solo) — clarify with organisers before submitting.
- No deployment, no video, no deck, no submission yet.

## What is still missing for submission

1. Resolve the solo-team-size question (+91 9910125804).
2. Create the public GitHub repo and push.
3. Deploy to Vercel (runbook in `deployment/DEPLOYMENT_RUNBOOK.md`).
4. Record the demo video from the live URL (60–120 s).
5. Build the pitch deck.
6. Submit via the HackIndia team page ("Mark as Submitted").
