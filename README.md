# 🌿 BrightPath Learn · Help Desk

A document-grounded Q&A app built with **Next.js, React, TypeScript and Django**, using NVIDIA-hosted **MiniMax M3.1 Flash**. Answers include document citations; missing information and API failures are explicit.

[🌐 Live demo](https://brightpath-learn-helpdesk.vercel.app) · [📖 Full setup and architecture guide](markdwons/README.md) · [📝 Walkthrough and AI disclosure](markdwons/SUBMISSION.md)

## 🚀 Run locally

From the repository root, start the backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py runserver 127.0.0.1:8000
```

In another terminal:

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Open http://127.0.0.1:3000. Existing environment files should be edited rather than overwritten. Python 3.11+ and Node.js 20.9+ are required. Fresh setup defaults to the clearly labelled mock when no key/provider is configured; mock does not prove AI answer quality. See the full guide for NVIDIA setup.

## 🧪 Verification

```bash
cd backend
source .venv/bin/activate
python manage.py test qa.tests
```

Run frontend checks with `npm run typecheck` and `npm run build` from `frontend`.

- [Local NVIDIA results](markdwons/TEST_RESULTS.md) and [mock results](markdwons/TEST_RESULTS.mock.md).
- [Hosted results](markdwons/HOSTED_TEST_RESULTS.md), [manual checklist](markdwons/MANUAL_TESTS.md) and [verification limits](markdwons/VERIFICATION.md).
- Current read timeout configuration: **10 seconds**, as requested. This can produce TIMEOUT for otherwise valid slower responses; it does not accelerate generation. Earlier saved results predate this adjustment.

## 🗂️ Structure and deployment

`backend/` contains the stateless Django API and three fictional documents. `frontend/` contains the Next.js UI. SDD artifacts are under `.kiro/specs/`; detailed documentation is under `markdwons/`.

Render continues to use the root [render.yaml](render.yaml); its copy in `markdwons/` is kept in sync for documentation. Vercel uses `frontend` as its root and server-only `BACKEND_URL` pointing to Render. Private environment files and NVIDIA credentials are excluded from Git.

The developer directed and audited the work through SDD with OpenAI Codex assistance. Read the [full guide](markdwons/README.md) for environment variables, API contracts, tradeoffs, deployment instructions and troubleshooting.
