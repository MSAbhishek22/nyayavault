# NyayaVault — Submission Draft (AI for Lawyers, HackIndia 2026)

**Status: DRAFT — do not submit yet.** The product is built; the
deployment, demo video and pitch deck are not. The solo-team-size
question is unresolved (see below).

## Event facts (verified 7 Nov 2026)

- Event: AI for Lawyers, HackIndia — virtual, free, 2 Nov–1 Dec 2026
- Prize pool: ₹2 Lakhs (official page:
  test.hackindia.org/2026/ai-for-lawyers-hackathon)
- Entrant: M S Abhishek — Participant ID **HI029518**, team
  "MS Abhishek" (solo), invite code ZZUMYE
- Track: **AI Legal Research**
- Deliverables: working legal AI product/prototype + sample legal
  outputs (contracts/research) + AI workflow/model explanation +
  demo video + pitch deck
- Judging: AI Utilization Depth 25%, Product Innovation 20%,
  Execution Speed 15%, Startup Viability 20%, UI/UX 10%,
  Pitch & Storytelling 10%
- Submission repo: https://github.com/HackIndiaXYZ/
  ai-for-lawyers-hackathon-ms-abhishek (currently 404 — not yet
  public/created)
- Team page: "Project Submission — Not Started", "Problem
  Statement — No problem statement selected yet"
- Contact on the event page: +91 9910125804

## ⚠️ Resolve before submitting — solo team size

The rules say teams of **2 to 5 participants**. The registration is
**solo** (1 member, HI029518) and was accepted. Solo compliance is
**not confirmed** by the page. Clarify with the organisers
(+91 9910125804) whether a one-person team may submit. Do not
submit as if solo were confirmed, and do not add a teammate without
the user's decision.

## Project summary (for the submission form)

**Name:** NyayaVault
**Tagline:** Your first legal question, answered from the statute itself.
**What it is:** A legal research assistant that answers
plain-language questions (English, Hindi, Hinglish) from a small,
verified corpus of Indian law — Constitution Arts. 14, 19, 21, 32;
IT Act 2000 ss. 43, 66, 66C, 66D, 79; Consumer Protection Act 2019
ss. 2, 34, 35, 69; Indian Contract Act 1872 ss. 2(h), 10, 73 — with
a citation (Act + section) on every claim, and a grounded refusal
when the corpus has no answer. It also generates structured research
briefs and contract summaries from the same corpus, and shows its
work in a grounding ledger and an "authority constellation" — a
spatial map of the law.
**What it is not:** a lawyer, legal advice, or a hallucinating
chatbot. The failure mode is a visible refusal, never a confident
invention.
**AI used:** grounded retrieval + citations + grounded refusal;
mock extractive provider today (labelled `[mock]`), BharatCode
model API (`qwen-3.8-27b`, fallback `deepseek-v4.1-flash`) behind
the same interface when a free key exists. Full explanation in
`docs/AI_WORKFLOW.md`.
**Built with:** Python 3.12 stdlib only (no dependencies), HTML/CSS/
JS (no CDN, no custom fonts).

## Links (fill in after Phases 4–6)

- Live app: _TBD — deploy first (see `deployment/DEPLOYMENT_RUNBOOK.md`)_
- GitHub repo: _TBD — repo does not exist yet_
- Demo video: _TBD — record from the live URL only_
- Pitch deck: _TBD_
- Sample outputs: `samples/` (2 research briefs + 1 contract
  summary, all with citations)
- AI workflow: `docs/AI_WORKFLOW.md`

## Judging-weight mapping (for the pitch)

| Weight | How NyayaVault answers it |
|---|---|
| 25% AI Utilization Depth | Grounded retrieval + citations + grounded refusal; visible routing and budget ledger; mock and real providers share one interface |
| 20% Product Innovation | Authority constellation (spatial map of the law) + grounding ledger; the answer and its evidence are one object |
| 15% Execution Speed | Built in days on the proven NoteVault engine; corpus verified in one research pass |
| 20% Startup Viability | India's legal-aid gap; free grounded first answer as a wedge (freemium: free research, paid drafting/review later) |
| 10% UI/UX | Law-library identity (parchment + oxblood + brass), distinct from the fleet; every control works; mobile + reduced-motion handled |
| 10% Pitch & Storytelling | "Your first legal question, answered from the statute itself" — stolen password, refused refund, unread contract |
