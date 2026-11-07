# NyayaVault — Deployment Runbook (Vercel)

**Status:** NOT DEPLOYED. This runbook is the plan, written from the
proven Vercel recipe used for NoteVault Bharat and SchemeSathi.
Do not claim a deployment until the live URL is verified.

## Prerequisites

- Public GitHub repo with this code (create first — the HackIndia
  submission repo URL currently 404s; verify whether the organisers
  create it or the team does).
- Vercel account (already exists; account email is
  msabhishekanni10@gmail.com — codes sent there cannot be fetched
  by Muse; the user reads them from his own mailbox).
- No card. **Stop immediately if any step asks for a card or
  payment.** (Render is not a fallback — it card-gates new accounts.)

## Steps

1. **Push the repo** (snapshot-push via the GitHub connector, same
   procedure as the fleet: manifest outside the source dir,
   verify head with `list_commits` after the push).
2. **Vercel → Add New → Project → import the repo.**
   - Framework: Other (Python WSGI).
   - Entrypoint: `nyayavault.wsgi:application` (set in
     `pyproject.toml` `[tool.vercel]`).
   - `vercel.json` is `{}` (no rewrites needed — the WSGI app
     serves `/` and `/api/*`).
3. **Environment variables:** none required. `BHARATCODE_API_KEY`
   is optional — without it the app runs in `[mock]` mode, which is
   the honest state today. Do **not** set a key that does not exist.
4. **Deploy.** If Vercel puts a "Verify Your Identity" challenge on
   the deploy, the cancel-and-redeploy workaround may fail (it did
   on 7 Nov for NoteVault Bharat) — use a code the user supplies
   from his own mailbox; codes expire in ~30 minutes.
5. **Verify the live URL** (do not skip any step):
   - `GET /api/status` → `{"ok": true, "mode": "mock",
     "notes_count": 17, "budget": {"used": 0, "limit": 10}}`
   - Open the page in a browser: hero renders, constellation
     renders, shelves list 17 provisions.
   - Ask the three preset questions on the live app:
     identity theft → grounded answer citing s. 66C;
     free speech → answer citing Art 19;
     DPDP question → grounded refusal ("not in the NyayaVault corpus").
   - Generate a research brief on the live app; download it.
6. **Record the deployment** in `deployment/RELEASE_MANIFEST.json`
   (live URL, commit SHA, date, verification results).
7. **Then** record the demo video from the live URL (never from
   localhost, never from screenshots).

## Rollback

- A bad deploy is rolled back from the Vercel dashboard
  (Deployments → previous deployment → Promote to Production).
  The app is stateless (in-memory ledger only), so a rollback
  loses nothing.

## Known Vercel quirks (from the fleet)

- The identity-verification challenge can appear on redeploys;
  the user's own codes are the only route (Muse cannot fetch
  msabhishekanni10@gmail.com).
- Cold starts ≥ 1 s are normal on the Hobby tier; the budget
  counter is per-instance and resets on cold start (by design,
  labelled in the UI).
