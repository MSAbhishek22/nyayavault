# NyayaVault — Interaction Inventory

**Checked:** 8 Nov 2026, against `nyayavault/web.py` (the page as
served) and the live local server smoke test. Every control below
was exercised or read in the served HTML/JS. No dead buttons.

## Page structure

| Region | Element | Works? |
|---|---|---|
| Hero | Title, tagline, disclaimer | Yes — static text |
| Mode bar | Mode badge (`[mock]` / `real`), mode line (gateway · model · provision count) | Yes — populated from `/api/status` |
| Constellation | Canvas (1000×300), drag to rotate, click a star to open its provision, arrow keys rotate, Enter opens selected star, auto-rotate every 50 ms unless reduced-motion | Yes — JS in page; reduced-motion → static |
| Shelves | 5 Act groups, 17 provisions, click or Enter to open | Yes — opens the preview below |
| Provision preview | Title, citation, source, first 1200 chars of the body | Yes — from `/api/document` |
| Ask | Question textarea, language select, Ask button | Yes — POST `/api/ask` |
| Presets | Identity theft / Free speech online / Refusal demo | Yes — fill the question and ask |
| Answer | Answer block, citation chips (click to open provision), mode/model/language line | Yes |
| Refusal | Red-bordered "No grounded answer" box | Yes — shown when `ok` is false |
| Brief | "Generate research brief" button, "Download brief (.md)" button | Yes — POST `/api/brief`, Blob download |
| Ledger | API, mode, model, reason, attempted routes, fallback warning, no-call line | Yes — from `/api/status` + last ask |
| Budget | Meter, used/limit line, Reset budget button | Yes — POST `/api/reset-budget` |
| Samples | Sample list (3), click to load into a `<pre>` | Yes — GET `/api/samples`, `/api/sample` |
| Footer | Corpus credit line | Yes — static text |

## API endpoints (all verified by the live-server smoke test)

| Method | Path | Verified |
|---|---|---|
| GET | `/` | 200, contains "NyayaVault", "Authority constellation", "not legal advice", provision data embedded |
| GET | `/api/status` | 200, `mode: "mock"`, `notes_count: 17`, `budget.limit: 10` |
| GET | `/api/document?path=it-act-s66c.md` | 200, title + body with "password" |
| GET | `/api/document?path=nope.md` | 404, `{"ok": false}` |
| POST | `/api/ask` (identity theft) | 200, `ok: true`, answer starts `[mock]`, citation `it-act-s66c.md` |
| POST | `/api/ask` (DPDP) | 200, `ok: false`, error contains "not in the NyayaVault corpus" |
| POST | `/api/brief` | 200, `ok: true`, brief contains "## What the law says" |
| GET | `/api/samples` | 200, 3 samples listed |
| GET | `/api/sample?name=...` | 200, body contains "not legal advice" |
| POST | `/api/reset-budget` | 200, `budget.used: 0` |

## Known gaps (honest)

- **No live browser render was verified in this session.** The page
  was verified by serving it locally and fetching it with curl, plus
  reading the HTML/JS. A real browser render (constellation canvas
  visuals, 390px mobile layout, drag interaction) still needs a
  browser check after deployment.
- **Hindi/Hinglish answers in mock mode are English extracts.**
  The mock provider returns corpus sentences (English); the
  language select is honoured by the real provider's prompt, not
  by the mock. The UI does not hide this — the `[mock]` badge is
  on every answer.
- **The constellation's star labels are short codes** ("Art 19",
  "s. 66C", "DPDP Act") — the full title is in the caption and the
  shelves. A first-time user may need the caption to read the map.
