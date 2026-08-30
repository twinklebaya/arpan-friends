# Kailash Journeys Crisis Response Site

A crisis-response web app tracking the Kailash Journeys tour group missing after the Nepal flash
floods near the Gyirong / Rasuwagadhi border crossing. Public hero + map + live feeds + status
tables + a reviewed tip-submission portal, plus an admin review queue that gates everything
before it goes live.

**Stack:** Vue 3 + Vite + Tailwind (frontend) · FastAPI + SQLite (backend) · OpenRouter (LLM
triage/classification) · deploy target: Vercel (frontend) + any persistent host for the backend
(Render/Railway/Fly — see below, not Vercel serverless).

## ⚠️ Before this goes live — read this

- **All content is placeholder.** Names for 3 of the 6 primary missing individuals, all photos,
  all "distinct physical markers", the last-known coordinates, and the emergency contact numbers
  are marked `PLACEHOLDER` in [`backend/app/seed.py`](backend/app/seed.py),
  [`frontend/src/lib/constants.js`](frontend/src/lib/constants.js), and
  [`frontend/src/components/EmergencyContacts.vue`](frontend/src/components/EmergencyContacts.vue).
  Replace every one with verified information before publishing.
- **No photos of deceased individuals, anywhere.** This is enforced in code, not just by
  convention: the `/api/persons` endpoint strips `photo_url` server-side for any record whose
  status is `deceased` ([`backend/app/routers/persons.py`](backend/app/routers/persons.py)), and
  the field is force-nulled the moment a person's status flips to deceased
  ([`backend/app/routers/admin.py`](backend/app/routers/admin.py)). The Confirmed Deceased table
  component has no photo column at all.
- **Deceased status is never automatic.** It can only be set through an admin-approved
  "source update" — raw text pasted from a real source, classified by OpenRouter, and approved by
  a human. A social-media source can never trigger a deceased determination even if it claims one
  (guarded twice: in the LLM prompt and again in the backend); it can still feed the general/target
  update feeds, just tagged "unverified — social media."
- **Public tips never auto-publish.** Every tip goes to `pending` and needs an admin approve/reject
  in `/admin` before it becomes a feed item.

## Project layout

```
backend/    FastAPI app, SQLite DB, OpenRouter integration, admin review-queue API
frontend/   Vue 3 + Vite + Tailwind SPA
```

## Running the backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit ADMIN_TOKEN and OPENROUTER_API_KEY
uvicorn app.main:app --reload --port 8000
```

Health check: `curl http://localhost:8000/api/health`

Without `OPENROUTER_API_KEY` set, the app still runs — source-update classification and tip
moderation both fall back to a "manual review required" note instead of failing.

## Running the frontend

**This machine had no Node.js/npm installed**, so the frontend below was hand-written but not
locally run or visually tested here. Install Node 18+ first (e.g. via
[nodejs.org](https://nodejs.org) or Homebrew: `brew install node`), then:

```bash
cd frontend
npm install
cp .env.example .env   # set VITE_API_BASE_URL to your backend URL
npm run dev
```

Visit `http://localhost:5173`. The admin queue is at `http://localhost:5173/admin` — it prompts
for the same token as `ADMIN_TOKEN` in the backend `.env`.

Once you have Node installed, it's worth running this once before deploying to catch anything
that only shows up at build/runtime (a live browser check is genuinely more reliable than reading
the source).

## Continuous integration

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs on every push/PR:

- **frontend-build**: `npm install && npm run build` for the Vue app — this is the real
  verification that the hand-written frontend actually compiles, since this dev machine had no
  Node.js to run it locally. Watch this job on your first push; if it's red, that's a real bug to
  fix, not a false alarm.
- **backend-import-check**: installs the FastAPI deps and imports the app, catching import/syntax
  errors.
- **vercel-preview-deploy** (PRs only, skipped until configured): deploys a live Vercel preview per
  PR using the Vercel CLI. To enable it, add these in the GitHub repo's Settings → Secrets and
  variables → Actions:
  - Secret `VERCEL_TOKEN` — from Vercel → Account Settings → Tokens
  - Variables `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID` — from running `vercel link` once inside
    `frontend/` locally (writes `.vercel/project.json`, gitignored), or from the Vercel project's
    Settings page

Once you run `npm install` locally, commit the generated `frontend/package-lock.json` and you can
re-add `cache: "npm"` to the workflow's `setup-node` step for faster CI runs — it's omitted for now
since there's no lockfile yet.

## Deploying

**Frontend → Vercel:** point a new Vercel project at `frontend/` (root directory = `frontend`),
build command `npm run build`, output directory `dist`. Set `VITE_API_BASE_URL` in Vercel's
environment variables to your deployed backend URL. `frontend/vercel.json` already rewrites all
routes to `index.html` so `vue-router`'s history mode (the `/admin` route) works.

**Backend → NOT Vercel.** Vercel's serverless functions have an ephemeral, read-only-ish
filesystem, which breaks both the SQLite file and the tip-image uploads directory this app relies
on. Deploy `backend/` to a host with a persistent disk instead — Render, Railway, and Fly.io all
work with basically the same `uvicorn app.main:app --host 0.0.0.0 --port $PORT` start command.
Set `ADMIN_TOKEN`, `OPENROUTER_API_KEY`, and `CORS_ORIGINS` (your Vercel domain) as environment
variables there.

**GitHub:** this directory isn't a git repo yet. When you're ready:

```bash
git init
git add -A
git commit -m "Initial crisis response app"
```

Then create a repo on GitHub (via the web UI or `gh repo create`) and push — happy to walk through
that with you when you're ready, since creating the remote repo is something you'd want to
confirm directly.

## Extending to real-time / Supabase

The Pinia store (`frontend/src/stores/crisis.js`) currently polls the FastAPI backend every 30s.
Every fetch goes through one `fetchAll()` action, so swapping polling for a real subscription
(Supabase realtime, a WebSocket, SSE) later only means calling the same state setters from a
subscription callback — no component changes needed.

## Optional next step: automated source monitoring

You mentioned potentially using a scheduled Claude/ChatGPT task to watch for updates (official
sources + social/X) and feed them in automatically. The pipeline already supports this:
`POST /api/admin/source-updates` accepts raw text + a `source_type` tag and does the OpenRouter
classification — a scheduled job just needs to paste text in. Whatever posts it should still only
ever reach the *pending* queue, never bypass the human-approval step, especially for anything that
could suggest a deceased-status change. Ask when you want to wire this up.
