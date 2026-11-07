"""NyayaVault web app: a law library at first light.

Single-page HTML (inline CSS, canvas constellation, no external
assets, no CDN). Palette: parchment + oxblood + brass. Layout:
hero → authority constellation → three columns (statute shelves |
ask + answer | grounding ledger) → sample outputs. Every answer
shows citations and a mode badge; refusal is a red-bordered box.
"""

from __future__ import annotations

import json
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .agent import LegalAgent
from .config import NyayaVaultConfig

# One star colour per Act — fixed, not hashed, so the sky is stable.
ACT_COLOURS = {
    "Constitution of India, 1950": "#e8c268",
    "Information Technology Act, 2000 (Act 21 of 2000)": "#8fce7a",
    "Consumer Protection Act, 2019 (Act 35 of 2019)": "#8fb7d9",
    "Indian Contract Act, 1872 (Act 9 of 1872)": "#d98f8f",
    "Coverage notes": "#a89f8d",
}

# Cross-reference lines: (rel, rel). The law's shape, drawn.
CROSS_LINKS = [
    ("constitution-art-19.md", "it-act-s66a-void.md"),
    ("constitution-art-19.md", "case-note-anuradha-bhasin.md"),
    ("constitution-art-21.md", "it-act-s66c.md"),
    ("constitution-art-21.md", "it-act-s66d.md"),
    ("it-act-s43.md", "it-act-s66.md"),
    ("it-act-s66c.md", "it-act-s66d.md"),
    ("contract-s10.md", "contract-s73.md"),
    ("cpa-s2-definitions.md", "cpa-s34-35-complaint.md"),
    ("cpa-s34-35-complaint.md", "cpa-s69-limitation.md"),
    ("constitution-art-14.md", "constitution-art-19.md"),
    ("constitution-art-19.md", "constitution-art-21.md"),
    ("constitution-art-21.md", "constitution-art-32.md"),
]

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NyayaVault — Your first legal question, answered from the statute itself</title>
<style>
:root{
  --oxblood:#5c1a24; --oxblood-deep:#3f1119; --parchment:#f7f1e3;
  --card:#fffdf6; --card-border:#e2d9bd; --brass:#b08d3c; --brass-deep:#8a6d2b;
  --ink:#23201b; --muted:#6b6455; --mock-bg:#ffe8c2; --mock-ink:#7a3e00;
  --real-bg:#dcefd8; --real-ink:#145214; --chip-bg:#f3e9c8; --chip-border:#d9c48a;
  --refusal-border:#a62b2b; --refusal-bg:#fdf0f0; --answer-bg:#fbf6e8;
  --grounded:#2e6b3a; --radius:14px;
}
*{box-sizing:border-box}
body{margin:0;background:var(--parchment);color:var(--ink);
  font-family:system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans",sans-serif;line-height:1.55}
.hero{background:linear-gradient(160deg,var(--oxblood),var(--oxblood-deep));
  color:#f7ead0;text-align:center;padding:32px 16px 26px}
.hero h1{font-family:Georgia,serif;font-size:2em;margin:0 0 6px}
.hero p{margin:6px auto;max-width:640px}
.hero .disclaimer{font-size:.85em;opacity:.85}
.modebar{display:flex;gap:10px;align-items:center;justify-content:center;flex-wrap:wrap;
  padding:10px 16px;font-size:.9em}
.badge{display:inline-block;padding:2px 8px;border-radius:999px;font-weight:600;font-size:.82em}
.badge.mock{background:var(--mock-bg);color:var(--mock-ink)}
.badge.real{background:var(--real-bg);color:var(--real-ink)}
main{max-width:1160px;margin:0 auto;padding:0 16px 48px}
.card{background:var(--card);border:1px solid var(--card-border);border-radius:var(--radius);padding:16px}
h3{font-family:Georgia,serif;margin:0 0 10px}
.sky{margin:6px 0 16px;padding:0;overflow:hidden}
#sky{width:100%;height:300px;display:block;background:var(--oxblood-deep);border-radius:var(--radius);cursor:grab}
#sky:focus-visible{outline:3px solid var(--brass);outline-offset:2px}
.sky-caption{font-size:.85em;color:var(--muted);margin:8px 4px 0}
.grid{display:grid;grid-template-columns:.9fr 1.6fr 1fr;gap:16px}
@media(max-width:900px){.grid{grid-template-columns:1fr}}
.act h4{margin:12px 0 4px;font-size:.85em;letter-spacing:.04em;text-transform:uppercase;color:var(--oxblood)}
.act ul{list-style:none;margin:0;padding:0}
.act li{padding:7px 8px;border-radius:8px;cursor:pointer;border:1px solid transparent}
.act li:hover{background:var(--chip-bg)}
.act li.selected{background:var(--chip-bg);border-color:var(--chip-border)}
.act li small{color:var(--muted)}
textarea,input[type=text]{width:100%;padding:10px;border:1px solid var(--card-border);border-radius:10px;font:inherit}
label{font-size:.85em;color:var(--muted);display:block;margin:10px 0 4px}
button{background:var(--oxblood);color:#fff;border:0;border-radius:10px;padding:10px 16px;font:inherit;cursor:pointer}
button.secondary{background:#fff;color:var(--oxblood);border:1px solid var(--oxblood)}
button:disabled{opacity:.5;cursor:default}
button:focus-visible,textarea:focus-visible,input:focus-visible,.act li:focus-visible{outline:3px solid var(--brass);outline-offset:2px}
.presets{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.presets button{padding:6px 10px;font-size:.85em}
.answer{background:var(--answer-bg);border-radius:10px;padding:12px;margin-top:12px;white-space:pre-wrap}
.refusal{border:2px solid var(--refusal-border);background:var(--refusal-bg);border-radius:10px;padding:12px;margin-top:12px}
.citations{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
.chip{background:var(--chip-bg);border:1px solid var(--chip-border);border-radius:999px;padding:3px 10px;font-size:.82em;cursor:pointer}
.meter{height:10px;background:#eadfc2;border-radius:999px;overflow:hidden;margin:6px 0}
.meter>div{height:100%;background:var(--brass-deep)}
.muted{color:var(--muted);font-size:.85em}
.ledger p{margin:6px 0;font-size:.92em}
.samples{margin-top:16px}
.samples ul{list-style:none;margin:0;padding:0}
.samples li{padding:8px;border-radius:8px;cursor:pointer}
.samples li:hover{background:var(--chip-bg)}
.samples pre{white-space:pre-wrap;font:inherit;background:var(--answer-bg);border-radius:10px;padding:12px;margin-top:10px}
footer{text-align:center;color:var(--muted);font-size:.85em;padding:8px 16px 24px}
</style>
</head>
<body>
<header class="hero">
  <h1>NyayaVault</h1>
  <p>Your first legal question, answered from the statute itself.</p>
  <p class="disclaimer">General legal information, not legal advice. Every answer cites the Act and section it comes from — and says plainly when the corpus has no answer.</p>
</header>
<div class="modebar">
  <span id="mode-badge" class="badge mock">[mock] offline stand-in — no live model call</span>
  <span id="mode-line" class="muted">Loading…</span>
</div>
<main>
  <section class="card sky" aria-label="Authority constellation">
    <canvas id="sky" width="1000" height="300" tabindex="0"
      aria-label="Authority constellation. Drag to rotate, click a star to open its provision, arrow keys rotate, Enter opens the selected provision."></canvas>
    <p class="sky-caption" id="sky-caption">The corpus as a constellation: four Acts and one coverage note, seventeen provisions, twelve cross-references. Drag to turn it; click a star to read its provision. The list below works the same way.</p>
  </section>
  <div class="grid">
    <section class="card act" aria-label="Statute shelves">
      <h3>Statute shelves</h3>
      <div id="shelves">Loading…</div>
      <div id="doc-preview" class="muted" style="margin-top:12px">Select a provision to preview it here.</div>
    </section>
    <section class="card" aria-label="Ask">
      <h3>Ask the corpus</h3>
      <label for="q">Your question (plain English, Hindi or Hinglish)</label>
      <textarea id="q" rows="3" placeholder="e.g. Someone stole my password and used it — what does the law say?"></textarea>
      <label for="lang">Answer language</label>
      <select id="lang">
        <option value="en" selected>English</option>
        <option value="hi">हिन्दी (Hindi)</option>
        <option value="hinglish">Hinglish</option>
      </select>
      <div style="margin-top:10px"><button id="ask">Ask</button></div>
      <div class="presets">
        <button class="secondary" data-q="Someone stole my password and used my account. What does Indian law say?">Identity theft</button>
        <button class="secondary" data-q="Can the government restrict free speech online or shut down the internet?">Free speech online</button>
        <button class="secondary" data-q="What does the DPDP Act 2023 say about a data breach?">Refusal demo (not in corpus)</button>
      </div>
      <div id="answer" aria-live="polite"></div>
      <div id="brief-actions" style="margin-top:10px;display:none">
        <button class="secondary" id="brief">Generate research brief</button>
        <button class="secondary" id="download-brief" disabled>Download brief (.md)</button>
      </div>
      <div id="brief-out"></div>
    </section>
    <section class="card ledger" aria-label="Grounding ledger">
      <h3>Grounding ledger</h3>
      <p><strong>API:</strong> <span id="api-line">—</span></p>
      <p><strong>Mode:</strong> <span id="mode-label">—</span></p>
      <p><strong>Model:</strong> <span id="model-line">—</span></p>
      <p><strong>Reason:</strong> <span id="reason-line">—</span></p>
      <p><strong>Attempted:</strong> <span id="attempted-line">—</span></p>
      <p id="fallback-line" class="muted" hidden>Fallback model was used.</p>
      <p id="no-call-line" class="muted">No API call made yet.</p>
      <h3 style="margin-top:16px">Budget</h3>
      <div class="meter"><div id="meter-fill" style="width:0%"></div></div>
      <p class="muted"><span id="budget-line">0 / 10 calls used this run</span></p>
      <button class="secondary" id="reset-budget">Reset budget</button>
      <p class="muted" style="margin-top:12px">Budget counts attempts, not tokens. A grounded refusal costs nothing.</p>
    </section>
  </div>
  <section class="card samples" aria-label="Sample legal outputs">
    <h3>Sample legal outputs</h3>
    <p class="muted">Generated from the same corpus, with citations. Each is general legal information, not legal advice.</p>
    <ul id="sample-list"><li>Loading…</li></ul>
    <div id="sample-out"></div>
  </section>
</main>
<footer>NyayaVault — AI for Lawyers, HackIndia 2026. Corpus: Constitution of India; IT Act 2000; Consumer Protection Act 2019; Indian Contract Act 1872. Sources verified against India Code and the Gazette of India.</footer>
<script>
const PROVISIONS = __PROVISIONS__;
const ACT_COLOURS = __ACT_COLOURS__;
const CROSS_LINKS = __CROSS_LINKS__;
const ACT_ORDER = ["Constitution of India, 1950", "Information Technology Act, 2000 (Act 21 of 2000)", "Consumer Protection Act, 2019 (Act 35 of 2019)", "Indian Contract Act, 1872 (Act 9 of 1872)", "Coverage notes"];
const ACT_SECTOR = {"Constitution of India, 1950":0, "Information Technology Act, 2000 (Act 21 of 2000)":Math.PI/2, "Consumer Protection Act, 2019 (Act 35 of 2019)":Math.PI, "Indian Contract Act, 1872 (Act 9 of 1872)":Math.PI*1.5, "Coverage notes":Math.PI*1.25};

// --- constellation: deterministic layout, fixed Act sectors ---
const stars = PROVISIONS.map((p, i) => {
  const actIdx = ACT_ORDER.indexOf(p.act);
  const inAct = PROVISIONS.filter(q => q.act === p.act);
  const pos = inAct.indexOf(p);
  const spread = (pos - (inAct.length - 1) / 2) * 0.45;
  const angle = ACT_SECTOR[p.act] + spread;
  const ring = pos % 2 === 0 ? 1 : 0.62;
  const R = 120;
  return {i, p, x: Math.cos(angle) * R * ring, y: (Math.sin(angle) * R * ring) * 0.55, z: Math.sin(angle) * R * ring * 0.6,
          colour: ACT_COLOURS[p.act] || "#b08d3c"};
});
const linkIdx = CROSS_LINKS.map(([a, b]) => [PROVISIONS.findIndex(p => p.rel === a), PROVISIONS.findIndex(p => p.rel === b)]).filter(([a, b]) => a >= 0 && b >= 0);

const canvas = document.getElementById("sky");
const ctx = canvas.getContext("2d");
let rotY = 0.4, rotX = 0.1, selected = -1;
const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
function project(s) {
  const cy = Math.cos(rotY), sy = Math.sin(rotY), cx = Math.cos(rotX), sx = Math.sin(rotX);
  let x = s.x * cy - s.z * sy, z = s.x * sy + s.z * cy, y = s.y;
  y = y * cx - z * sx; z = y * sx + z * cx;
  const f = 420, scale = f / (f + z + 160);
  return {x: 500 + x * scale, y: 150 + y * scale, scale, z};
}
function draw() {
  ctx.clearRect(0, 0, 1000, 300);
  const pts = stars.map(project);
  ctx.strokeStyle = "rgba(232,194,104,0.35)"; ctx.lineWidth = 1;
  for (const [a, b] of linkIdx) {
    ctx.beginPath(); ctx.moveTo(pts[a].x, pts[a].y); ctx.lineTo(pts[b].x, pts[b].y); ctx.stroke();
  }
  pts.forEach((pt, i) => {
    const r = Math.max(2, 4.5 * pt.scale);
    ctx.beginPath(); ctx.arc(pt.x, pt.y, r, 0, Math.PI * 2);
    ctx.fillStyle = stars[i].colour; ctx.fill();
    if (i === selected) { ctx.beginPath(); ctx.arc(pt.x, pt.y, r + 4, 0, Math.PI * 2); ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.stroke(); }
    ctx.fillStyle = "rgba(247,234,208,0.9)"; ctx.font = "11px system-ui, sans-serif";
    ctx.fillText(stars[i].p.short, pt.x + r + 4, pt.y + 4);
  });
  const sel = selected >= 0 ? stars[selected].p : null;
  document.getElementById("sky-caption").textContent = sel
    ? "Selected: " + sel.title + " — " + sel.citation + ". Press Enter or click to open it in the shelves."
    : "The corpus as a constellation: four Acts and one coverage note, seventeen provisions, twelve cross-references. Drag to turn it; click a star to read its provision. The list below works the same way.";
}
let dragging = false, lastX = 0, lastY = 0;
canvas.addEventListener("pointerdown", e => { dragging = true; lastX = e.clientX; lastY = e.clientY; canvas.setPointerCapture(e.pointerId); });
canvas.addEventListener("pointermove", e => {
  if (!dragging) return;
  rotY += (e.clientX - lastX) * 0.005; rotX = Math.max(-0.6, Math.min(0.6, rotX + (e.clientY - lastY) * 0.003));
  lastX = e.clientX; lastY = e.clientY; draw();
});
canvas.addEventListener("pointerup", e => {
  if (Math.abs(e.clientX - lastX) < 3 && Math.abs(e.clientY - lastY) < 3) {
    const rect = canvas.getBoundingClientRect();
    const mx = (e.clientX - rect.left) * (1000 / rect.width), my = (e.clientY - rect.top) * (300 / rect.height);
    const pts = stars.map(project);
    let best = -1, bestD = 22;
    pts.forEach((pt, i) => { const d = Math.hypot(pt.x - mx, pt.y - my); if (d < bestD) { bestD = d; best = i; } });
    if (best >= 0) { selected = best; openProvision(stars[best].p.rel); draw(); }
  }
  dragging = false;
});
canvas.addEventListener("keydown", e => {
  if (e.key === "ArrowLeft") { rotY -= 0.1; draw(); }
  else if (e.key === "ArrowRight") { rotY += 0.1; draw(); }
  else if (e.key === "ArrowUp") { rotX = Math.max(-0.6, rotX - 0.05); draw(); }
  else if (e.key === "ArrowDown") { rotX = Math.min(0.6, rotX + 0.05); draw(); }
  else if (e.key === "Enter" && selected >= 0) { openProvision(stars[selected].p.rel); }
});
if (!reduced) setInterval(() => { if (!dragging) { rotY += 0.004; draw(); } }, 50);
draw();

// --- shelves ---
const shelves = document.getElementById("shelves");
shelves.innerHTML = ACT_ORDER.map(act => {
  const items = PROVISIONS.filter(p => p.act === act);
  return "<h4>" + act + "</h4><ul>" + items.map(p =>
    '<li tabindex="0" data-rel="' + p.rel + '"><strong>' + p.short + '</strong><br><small>' + p.citation + '</small></li>').join("") + "</ul>";
}).join("");
shelves.addEventListener("click", e => { const li = e.target.closest("li[data-rel]"); if (li) openProvision(li.dataset.rel); });
shelves.addEventListener("keydown", e => { if (e.key === "Enter") { const li = e.target.closest("li[data-rel]"); if (li) openProvision(li.dataset.rel); } });

async function openProvision(rel) {
  const res = await fetch("/api/document?path=" + encodeURIComponent(rel));
  const data = await res.json();
  document.querySelectorAll("#shelves li").forEach(li => li.classList.toggle("selected", li.dataset.rel === rel));
  const idx = PROVISIONS.findIndex(p => p.rel === rel);
  if (idx >= 0) { selected = idx; draw(); }
  if (!data.ok) { document.getElementById("doc-preview").textContent = "Could not load that provision."; return; }
  const body = data.body.replace(/^# .*$/m, "").trim();
  document.getElementById("doc-preview").innerHTML =
    "<strong>" + data.title + "</strong><br><span class='muted'>" + data.citation + " — Source: " + data.source + "</span><pre style='white-space:pre-wrap;font:inherit;margin:8px 0 0'>" + escapeHtml(body.slice(0, 1200)) + "</pre>";
}
function escapeHtml(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

// --- status / ledger ---
async function refreshStatus() {
  const res = await fetch("/api/status");
  const s = await res.json();
  document.getElementById("mode-badge").className = "badge " + (s.mode === "real" ? "real" : "mock");
  document.getElementById("mode-badge").textContent = s.mode === "real" ? "real BharatCode API" : "[mock] offline stand-in — no live model call";
  document.getElementById("mode-line").textContent = s.gateway + " · model " + s.model + " · " + s.notes_count + " provisions in the corpus";
  document.getElementById("api-line").textContent = s.gateway;
  document.getElementById("mode-label").textContent = s.mode_label;
  document.getElementById("model-line").textContent = s.model + " (fallback: " + s.fallback + ")";
  document.getElementById("reason-line").textContent = s.reason || "—";
  document.getElementById("attempted-line").textContent = (s.attempted_models && s.attempted_models.length) ? s.attempted_models.join(" → ") : "—";
  document.getElementById("fallback-line").hidden = !s.fallback_used;
  document.getElementById("no-call-line").hidden = !!(s.attempted_models && s.attempted_models.length);
  const used = s.budget.used, limit = s.budget.limit;
  document.getElementById("meter-fill").style.width = Math.min(100, used / limit * 100) + "%";
  document.getElementById("budget-line").textContent = used + " / " + limit + " calls used this run" + (s.budget.exhausted ? " — budget exhausted" : "");
}
refreshStatus();

// --- ask ---
let lastQuestion = "", lastBrief = "";
document.getElementById("ask").addEventListener("click", async () => {
  const q = document.getElementById("q").value.trim();
  const lang = document.getElementById("lang").value;
  const out = document.getElementById("answer");
  if (!q) { out.innerHTML = "<div class='refusal'>Ask a legal question about the corpus — for example, what happens if someone steals my password?</div>"; return; }
  out.innerHTML = "<p class='muted'>Consulting the corpus…</p>";
  lastQuestion = q;
  const res = await fetch("/api/ask", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({question: q, language: lang})});
  const data = await res.json();
  if (!data.ok) {
    out.innerHTML = "<div class='refusal'><strong>No grounded answer.</strong><br>" + escapeHtml(data.error || data.answer || "No grounded answer.") + "</div>";
  } else {
    const chips = (data.citations || []).map(c =>
      '<span class="chip" data-rel="' + c.rel + '">' + escapeHtml(c.title) + " — " + escapeHtml(c.citation) + "</span>").join("");
    out.innerHTML = "<div class='answer'>" + escapeHtml(data.answer) + "</div>" +
      (chips ? "<div class='citations'>" + chips + "</div>" : "") +
      "<p class='muted'>Mode: " + escapeHtml(data.mode) + " · Model: " + escapeHtml(data.model) +
      (data.fallback_used ? " · fallback used" : "") + " · Language: " + escapeHtml(data.language) + "</p>";
    out.querySelectorAll(".chip").forEach(ch => ch.addEventListener("click", () => openProvision(ch.dataset.rel)));
    document.getElementById("brief-actions").style.display = "block";
    document.getElementById("download-brief").disabled = true;
    document.getElementById("brief-out").innerHTML = "";
  }
  refreshStatus();
});
document.querySelectorAll(".presets button").forEach(b => b.addEventListener("click", () => {
  document.getElementById("q").value = b.dataset.q;
  document.getElementById("ask").click();
}));
document.getElementById("brief").addEventListener("click", async () => {
  const lang = document.getElementById("lang").value;
  const out = document.getElementById("brief-out");
  out.innerHTML = "<p class='muted'>Drafting the brief…</p>";
  const res = await fetch("/api/brief", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({question: lastQuestion, language: lang})});
  const data = await res.json();
  if (!data.ok) { out.innerHTML = "<div class='refusal'>" + escapeHtml(data.error || "Could not draft the brief.") + "</div>"; return; }
  lastBrief = data.brief;
  out.innerHTML = "<pre style='white-space:pre-wrap;font:inherit;background:var(--answer-bg);border-radius:10px;padding:12px;margin-top:10px'>" + escapeHtml(data.brief) + "</pre>";
  document.getElementById("download-brief").disabled = false;
});
document.getElementById("download-brief").addEventListener("click", () => {
  const blob = new Blob([lastBrief], {type: "text/markdown"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "nyayavault-research-brief.md";
  a.click();
  URL.revokeObjectURL(a.href);
});
document.getElementById("reset-budget").addEventListener("click", async () => {
  await fetch("/api/reset-budget", {method: "POST"});
  refreshStatus();
});

// --- samples ---
(async () => {
  const res = await fetch("/api/samples");
  const data = await res.json();
  const list = document.getElementById("sample-list");
  if (!data.ok || !data.samples.length) { list.innerHTML = "<li>No sample outputs yet.</li>"; return; }
  list.innerHTML = data.samples.map(name => '<li data-name="' + name + '">' + name.replace(/\\.md$/, "").replace(/-/g, " ") + "</li>").join("");
  list.addEventListener("click", async e => {
    const li = e.target.closest("li[data-name]");
    if (!li) return;
    const r = await fetch("/api/sample?name=" + encodeURIComponent(li.dataset.name));
    const d = await r.json();
    document.getElementById("sample-out").innerHTML = d.ok
      ? "<pre>" + escapeHtml(d.body) + "</pre>"
      : "<p class='muted'>Could not load that sample.</p>";
  });
})();
</script>
</body>
</html>
"""


def _short_title(title: str) -> str:
    """Short label for a constellation star, e.g. 'Art 19' or 's. 66C'."""
    if "Article 14" in title:
        return "Art 14"
    if "Article 19" in title:
        return "Art 19"
    if "Article 21" in title:
        return "Art 21"
    if "Article 32" in title:
        return "Art 32"
    for marker in ("s. 66A", "s. 66C", "s. 66D", "s. 66", "s. 43", "s. 79",
                   "s. 2(7)", "s. 2(9)", "ss. 34", "s. 69", "s. 10", "s. 73"):
        if marker in title:
            return marker
    if "Anuradha Bhasin" in title:
        return "Bhasin"
    if "Coverage note" in title:
        return "DPDP Act"
    return title[:12]


def _page(agent: LegalAgent) -> str:
    provisions = [
        {
            "title": p.title,
            "short": _short_title(p.title),
            "rel": p.rel,
            "act": p.act,
            "citation": p.citation,
        }
        for p in agent.provisions
    ]
    return (
        PAGE.replace("__PROVISIONS__", json.dumps(provisions))
        .replace("__ACT_COLOURS__", json.dumps(ACT_COLOURS))
        .replace("__CROSS_LINKS__", json.dumps(CROSS_LINKS))
    )


class NyayaVaultHandler(BaseHTTPRequestHandler):
    """HTTP handler: page + JSON API. stdlib only, no framework."""

    agent: LegalAgent
    config: NyayaVaultConfig
    samples_root: str

    def log_message(self, fmt: str, *args) -> None:  # quiet
        pass

    def _json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return {}

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            html = _page(self.agent).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
            return
        if parsed.path == "/api/status":
            self._json(_status_payload(self.agent, self.config))
            return
        if parsed.path == "/api/document":
            query = urllib.parse.parse_qs(parsed.query)
            rel = (query.get("path") or [""])[0]
            provision = next((p for p in self.agent.provisions if p.rel == rel), None)
            if provision is None:
                self._json({"ok": False, "error": "Provision not found."}, status=404)
                return
            self._json({
                "ok": True,
                "title": provision.title,
                "rel": provision.rel,
                "act": provision.act,
                "section": provision.section,
                "source": provision.source,
                "citation": provision.citation,
                "body": provision.body,
            })
            return
        if parsed.path == "/api/samples":
            self._json({"ok": True, "samples": self.agent.list_samples(self.samples_root)})
            return
        if parsed.path == "/api/sample":
            query = urllib.parse.parse_qs(parsed.query)
            name = (query.get("name") or [""])[0]
            body = self.agent.read_sample(self.samples_root, name)
            if body is None:
                self._json({"ok": False, "error": "Sample not found."}, status=404)
                return
            self._json({"ok": True, "name": name, "body": body})
            return
        self._json({"ok": False, "error": "Not found."}, status=404)

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/ask":
            payload = self._read_json()
            detail = self.agent.ask_detailed(
                payload.get("question", ""), payload.get("language", "en")
            )
            self._json({
                "ok": detail.ok,
                "answer": detail.answer,
                "error": detail.error,
                "citations": [
                    {
                        "title": p.title,
                        "rel": p.rel,
                        "act": p.act,
                        "section": p.section,
                        "citation": p.citation,
                    }
                    for p in detail.citations
                ],
                "mode": detail.mode,
                "language": detail.language,
                "model": detail.model,
                "reason": detail.reason,
                "attempted": detail.attempted,
                "fallback_used": detail.fallback_used,
            })
            return
        if parsed.path == "/api/brief":
            payload = self._read_json()
            question = payload.get("question", "")
            if not question.strip():
                self._json({"ok": False, "error": "Ask a question first."})
                return
            brief = self.agent.research_brief(question, payload.get("language", "en"))
            self._json({"ok": True, "brief": brief})
            return
        if parsed.path == "/api/reset-budget":
            self.agent.ledger.calls_used = 0
            self.agent.ledger.exhausted = False
            self._json({"ok": True, "budget": {"used": 0, "limit": self.agent.ledger.cap}})
            return
        self._json({"ok": False, "error": "Not found."}, status=404)


def _status_payload(agent: LegalAgent, config: NyayaVaultConfig) -> dict:
    ledger = agent.ledger
    mode = "real" if not config.mock_mode else "mock"
    return {
        "ok": True,
        "notes_count": len(agent.provisions),
        "mode": mode,
        "mode_label": (
            "real BharatCode API" if mode == "real" else "[mock] offline stand-in — no live model call"
        ),
        "gateway": config.base_url,
        "model": config.model if mode == "real" else "mock-extractive",
        "fallback": config.fallback_model,
        "reason": (
            "No BHARATCODE_API_KEY set — mock extractive provider."
            if mode == "mock"
            else "Primary BharatCode model configured."
        ),
        "budget": {
            "used": ledger.calls_used,
            "limit": ledger.cap,
            "exhausted": ledger.exhausted,
        },
        "attempted_models": ledger.attempted_models,
        "fallback_used": ledger.fallback_used,
        "acts": sorted({p.act for p in agent.provisions}),
    }


def make_handler(agent: LegalAgent, config: NyayaVaultConfig, samples_root: str):
    """Build a handler class bound to one agent/config (for testing)."""

    class BoundHandler(NyayaVaultHandler):
        pass

    BoundHandler.agent = agent
    BoundHandler.config = config
    BoundHandler.samples_root = samples_root
    return BoundHandler


def serve(agent: LegalAgent, config: NyayaVaultConfig, samples_root: str) -> None:
    handler = make_handler(agent, config, samples_root)
    server = ThreadingHTTPServer((config.host, config.port), handler)
    print(f"NyayaVault listening on http://{config.host}:{config.port}")
    server.serve_forever()
