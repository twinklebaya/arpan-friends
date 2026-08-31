# Kailash Journeys Crisis Response Site

A crisis-response hub tracking the Kailash Journeys tour group missing after the Aug 26, 2026
Nepal-Tibet flash floods, open to families and friends of anyone affected by the disaster. Hero +
map + dual live feeds (general disaster news / Kailash Journeys-specific) + status tables + a
reviewed tip-submission portal, plus an admin review queue that gates everything before it goes
live.

**Stack:** Vue 3 + Vite + Tailwind (frontend) · FastAPI + Supabase Postgres (backend) · Supabase
Storage (tip-image uploads) · OpenRouter (LLM triage/classification, free tier) · deployed
entirely on Vercel (frontend as a static SPA, backend as a Vercel Function via FastAPI's
zero-config support).

## Safety rules enforced in code

- **No photo of a deceased person, ever.** `/api/persons` strips `photo_url`/`photo_urls`
  server-side for any record with `status: deceased`
  ([`backend/app/routers/persons.py`](backend/app/routers/persons.py)), and both fields are
  force-nulled the moment a person's status flips to deceased
  ([`backend/app/routers/admin.py`](backend/app/routers/admin.py)).
- **Deceased status is never automatic.** It's only set through an admin-approved "source
  update" — raw text pasted from a real source, classified by OpenRouter, approved by a human. A
  social-media source can never trigger a deceased determination even if it claims one (guarded in
  both the LLM prompt and the backend) — it can still feed the general/target update feeds, tagged
  "unverified — social media."
- **Public tips and person registrations never auto-publish.** Both go to `pending` and need an
  admin approve/reject in `/admin` before appearing anywhere public.
- Every piece of real content on the site (names, ages, physical markers, coordinates, emergency
  contacts, feed items) is sourced and cited — see conversation/commit history for provenance on
  any specific fact.

## Project layout

```
backend/    FastAPI app (Supabase Postgres + Storage, OpenRouter integration, admin review-queue API)
frontend/   Vue 3 + Vite + Tailwind SPA
```

## Running the backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in DATABASE_URL, ADMIN_TOKEN, OPENROUTER_API_KEY, SUPABASE_*
uvicorn app.main:app --reload --port 8000
```

Health check: `curl http://localhost:8000/api/health`

Without `OPENROUTER_API_KEY` set, the app still runs — source-update classification and tip
moderation both fall back to a "manual review required" note instead of failing. Without
`SUPABASE_URL`/`SUPABASE_SERVICE_ROLE_KEY`, tip image uploads will fail (everything else works).

## Running the frontend

```bash
cd frontend
npm install
cp .env.example .env   # set VITE_API_BASE_URL to your backend URL
npm run dev
```

Visit `http://localhost:5173`. The admin queue is at `http://localhost:5173/admin` — it prompts
for the same token as `ADMIN_TOKEN` in the backend `.env`.

## Continuous integration

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs on every push/PR:

- **frontend-build**: `npm install && npm run build` for the Vue app.
- **backend-import-check**: installs the FastAPI deps and imports the app, catching import/syntax
  errors.
- **vercel-preview-deploy** (PRs only): deploys a live Vercel preview per PR using the Vercel CLI,
  gated on `VERCEL_TOKEN` secret + `VERCEL_ORG_ID`/`VERCEL_PROJECT_ID` variables being set in the
  GitHub repo's Settings → Secrets and variables → Actions.

## Deploying

Both frontend and backend deploy on Vercel, as **two separate Vercel projects** pointed at the
same GitHub repo with different root directories.

**Frontend project** — Root Directory `frontend`, framework preset Vite, build command
`npm run build`, output directory `dist`. Env var: `VITE_API_BASE_URL` set to the backend
project's URL. `frontend/vercel.json` rewrites all routes to `index.html` so `vue-router`'s
history mode (the `/admin` route) works.

**Backend project** — Root Directory `backend`. Vercel's FastAPI zero-config support
auto-detects `app/main.py` (a supported entrypoint name) as the ASGI app — no wrapper file
needed. `backend/vercel.json` just bumps the function's `maxDuration` to 30s, since OpenRouter
calls in the tip-moderation and source-update-classification paths can take a few seconds. Env
vars needed: `DATABASE_URL` (Supabase **pooled** connection, port 6543 — see the comment in
`.env.example` for why direct/port-5432 is wrong for serverless), `ADMIN_TOKEN`,
`OPENROUTER_API_KEY`, `OPENROUTER_MODEL`, `CORS_ORIGINS` (the frontend's domain),
`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`.

**Database & storage**: Supabase Postgres (provisioned via Vercel Storage integration) holds all
app data; a public `tip-uploads` Storage bucket holds tip-submission images. Row Level Security
is enabled on every app table — the backend connects as the `postgres` role which bypasses RLS,
but this blocks the Supabase anon key (used by e.g. its auto-generated REST API) from reading or
writing rows directly, which would otherwise let anyone bypass every review-queue guard above.

## Extending to real-time

The Pinia store (`frontend/src/stores/crisis.js`) currently polls the FastAPI backend every 30s.
Every fetch goes through one `fetchAll()` action, so swapping polling for a real subscription
(Supabase realtime, a WebSocket, SSE) later only means calling the same state setters from a
subscription callback — no component changes needed.

## Optional next step: automated source monitoring

A scheduled job (Claude, ChatGPT, or otherwise) watching for updates from official sources and
social/X could feed them in automatically: `POST /api/admin/source-updates` accepts raw text + a
`source_type` tag and runs the OpenRouter classification — a scheduled job just needs to paste
text in. Whatever posts it should still only ever reach the *pending* queue, never bypass the
human-approval step, especially for anything that could suggest a deceased-status change.
