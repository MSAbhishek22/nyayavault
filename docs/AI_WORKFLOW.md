# NyayaVault — AI Workflow & Model Explanation

**Hackathon:** AI for Lawyers, HackIndia 2026 — track: AI Legal Research
**Product:** NyayaVault, a grounded legal research assistant
**Date:** 8 Nov 2026
**Honest status:** the app runs today in **mock mode** (deterministic,
offline, extractive). The live model wiring is the same interface
and is documented below; no key exists yet, and none is invented.

## 1. The problem with a plain chatbot

A general-purpose language model asked a legal question will
answer fluently — and will invent section numbers, cases and
quotations when it does not know. In law, a confident wrong answer
is worse than no answer: a person who acts on an invented section
loses time, money, or a case. NyayaVault is built so that the
failure mode is a visible refusal, never a confident invention.

## 2. Architecture (one picture, in words)

```
User question
    │
    ▼
Guardrails (guardrails.py) — secrets / personal numbers refused
    │  (never sent to any model; costs nothing)
    ▼
Retrieval (index.py) — keyword search over the local corpus
    │  17 Markdown documents, 4 Acts + 1 coverage note
    │  title ×3, tag ×3, whole-word body ×1, stopwords filtered,
    │  minimum score 2, and either score ≥ 5 or ≥ 2 distinct words
    ▼
  No hit? ──► Grounded refusal (no model call, no budget spent)
  Coverage note top hit? ──► Grounded "not covered" refusal
    │
    ▼
Provider (llm.py) — one interface, two implementations
    ├─ MockProvider: deterministic extractive answer — the first
    │  substantive sentence (60+ chars) from the top provision's
    │  Statutory text section. No network, no key, no pretence.
    └─ BharatCodeProvider: BharatCode model API
       (POST /api/model/v1/chat/completions, OpenAI-compatible),
       system prompt instructs: answer ONLY from the provisions,
       cite Act + section for every claim, refuse when the
       provisions do not answer, never invent a case or section.
    │
    ▼
Routing (routing.py) — primary model first; on failure, the
fallback model once; per-run budget counts attempts (cap 10);
a refusal never costs a call.
    │
    ▼
Answer + citations + mode badge + grounding ledger
    (every answer carries "general legal information, not legal advice")
```

## 3. Retrieval — how a question finds its law

- **Corpus:** 17 Markdown files in `corpus/`, one per provision,
  each with `Act:`, `Section:`, `Source:` header lines and `#tag`
  lines. Loaded at startup, sorted, deterministic.
- **Scoring:** title tokens ×3, tag tokens ×3, whole-word body
  tokens ×1 (with a simple plural tolerance: "product" finds
  "products"). Substring matching is deliberately **not** used —
  "data" must not match "damage". Stopwords (e.g. "act", "law",
  "what", "used", "corpus") are filtered so a generic question
  cannot match the whole corpus.
- **Threshold:** a provision counts as a hit only if it scores
  ≥ 2 **and** either scores ≥ 5 or matches ≥ 2 distinct words.
  One stray word in a title (e.g. "punishment" in a question about
  murder) is not a grounded answer.
- **Determinism:** the same question always retrieves the same
  provisions in the same order (score descending, filename ascending
  as the tiebreak).

## 4. Grounding — how an answer stays inside the corpus

- The provider receives **only** the retrieved provisions as
  context, plus a system prompt that forbids answering outside
  them and forbids inventing cases, section numbers or judgments.
- In mock mode the answer is **extractive**: the first substantive
  sentence from the top provision's Statutory text section
  (verbatim text from the corpus). The mock never generates new
  legal claims.
- Every answer is shown with its **citations** (Act + section +
  source URL, clickable to open the provision) and a **mode badge**
  (`[mock]` or `real BharatCode API`).
- The **grounding ledger** (right rail) shows which model was
  used, why, which models were attempted, whether the fallback was
  used, and how much of the per-run budget was spent.

## 5. Refusal — the feature, not the failure

NyayaVault refuses in three cases, all before any model call:

1. **No hit** — the corpus has no provision for the question
   (e.g. "What is the punishment for murder under the IPC?").
   The refusal lists what the corpus *does* cover.
2. **Coverage note** — the question is about something the corpus
   explicitly does not cover (e.g. the DPDP Act 2023). The corpus
   carries a coverage note for the DPDP Act so the answer is a
   grounded "not covered", not a guess borrowed from another Act
   (the word "breach" also appears in Contract Act s. 73 — a
   different kind of breach).
3. **Guardrail** — the question contains something that looks like
   a secret, a password, a token, a card number or a 12-digit
   personal number. It is refused before anything leaves the
   machine.

A refusal costs no budget and is shown in a red-bordered box so it
cannot be mistaken for an answer.

## 6. Models — what is real, what is mock

| Layer | Today (8 Nov 2026) | Later (same interface) |
|---|---|---|
| Retrieval | Real (local, deterministic) | Same |
| Answering | **Mock** — `MockProvider`, extractive, offline, labelled `[mock]` on every answer | **Real** — `BharatCodeProvider`, BharatCode model API, default model `qwen-3.8-27b`, fallback `deepseek-v4.1-flash` |
| Key | None exists; none invented; `.env.example` has an empty `BHARATCODE_API_KEY` | Read from `BHARATCODE_API_KEY` in the environment only — never from a file, never committed |
| Budget | 10 attempts per run (mock calls count too, so the ledger is honest in both modes) | Same cap |

The mock and the real provider share one interface
(`ask(question, context, language) -> ProviderResult`), so swapping
in the live model changes no other code. The BharatCode provider is
the same shape already running in production in the sibling
NoteVault Bharat app (https://notevault-bharat.vercel.app).

## 7. What the model does NOT do

- It does not decide the law. It retrieves provisions and (in real
  mode) composes an answer from them.
- It does not see the user's personal facts: the corpus is public
  law, and guardrails strip secrets before any call.
- It does not store questions or answers server-side. The ledger is
  per-run, in memory, and resets with the process.
- It does not give legal advice. Every answer and every sample
  output says so.

## 8. Sample outputs — how they are made

- **Research briefs** (`samples/sample-research-brief-*.md`) are
  generated by the app itself (`LegalAgent.research_brief`):
  short answer from the provider, provisions quoted from the
  corpus, an explicit "What is NOT covered" section, and next
  steps. The two briefs in `samples/` were generated with the CLI
  (`python3 -m nyayavault.cli brief ... --out samples/...`).
- **Contract summary** (`samples/sample-contract-summary-*.md`) is
  a hand-written summary of a **synthetic** contract (fictional
  parties, fictional figures), checked against Contract Act s. 10
  (the five essentials) and s. 73 (damages). It is labelled
  SYNTHETIC in the file.

## 9. Testing

52 automated tests (Python `unittest`, stdlib only), all passing on
8 Nov 2026 in the Linux sandbox (Python 3.12.3):

- `tests/test_index.py` — corpus loads (17 documents, 5 groups),
  retrieval finds the right provision for identity theft, free
  speech, consumer refund and broken contract; DPDP returns the
  coverage note; a truly unknown topic returns nothing.
- `tests/test_guardrails.py` — secrets, tokens, card numbers and
  12-digit numbers refused; normal questions pass.
- `tests/test_llm_routing.py` — mock answers are extractive corpus
  sentences; routing counts budget; exhausted budget raises.
- `tests/test_agent.py` — grounded answers with citations; DPDP
  refuses via the coverage note; refusal costs no budget; budget
  cap blocks the third call; briefs have all four sections.
- `tests/test_samples.py` — 3 samples exist, all carry the
  disclaimer, all cite only sections that exist in the corpus.
- `tests/test_web.py` — live HTTP server smoke tests (home page,
  status, ask, refusal, document, brief, samples, reset-budget)
  plus WSGI dispatch tests.

Run: `python3 -m unittest discover -s tests`
