# BrightPath Help Desk — Requirements

Status: approved by user; implementation delivered with verification limitations recorded in VERIFICATION.md.

## Scope

A local take-home exercise limited to two hours of work. Next.js App Router, React and TypeScript frontend; Python 3.11+ and Django 5.x backend. All product text, code comments and documentation are English. No database, authentication, streaming, history, Docker, CI or video. Deployment preparation for Vercel and Render is included; actual publication is a separate manual step.

The supplied user prompt is the implementation specification. `context.md` confirms the reviewer's five requirements and submission constraints. Use the three fictional documents verbatim from the prompt, with their specified filenames and titles.

## Acceptance criteria

1. WHEN a JSON question contains 1–500 non-whitespace characters, the system SHALL accept `POST /api/ask` and display the validated result with provider identification and document citations.
2. WHEN a question is supported, the system SHALL use only supplied documents, preserve caveats, answer in the question's language and attach short verbatim supporting quotes.
3. WHEN information is absent or all citations fail validation, the system SHALL return `answerable: false`, no sources and the standard unavailable-information message. Pricing, refunds and job placement questions SHALL also refer to support@brightpath.example.
4. WHEN the model fails, times out, is rate limited or returns invalid output, the system SHALL return the specified JSON error envelope and SHALL NOT return an answer. Missing credentials for an explicitly selected NVIDIA provider SHALL produce MISSING_API_KEY.
5. WHEN `SIMULATE_FAILURE=true` or `?simulate=failure` is supplied, the system SHALL produce MODEL_UNAVAILABLE. The UI SHALL expose a simulation checkbox.
6. WHEN no provider or key is configured, the system SHALL use a clearly labelled mock, including a visible UI disclaimer. A configured provider failure SHALL NOT silently fall back to mock.
7. WHEN input, method or route is invalid, the Django API SHALL return JSON with an appropriate status, including 400/404/405/500. Frontend connection failures SHALL show the specified backend-unreachable message.
8. WHEN evaluation runs, it SHALL save observed results for coaching, pricing/refunds and simulated failure, plus lesson completion if time allows. Mock and real results SHALL remain separate; unexecuted real tests SHALL be labelled unverified.
9. WHEN preparing submission, the project SHALL include reproducible setup, pinned dependencies and lockfile, both environment examples, ignored secrets, test results and an honest walkthrough and AI-tool disclosure, consolidated in `SUBMISSION.md` by the user’s final instruction.

## Required verification

Parser tests: fenced/invalid JSON, incorrect schema, unknown document IDs, fabricated and blank quotes, normalized quote matching, unsupported-answer downgrade. Endpoint tests: input boundaries, failures and JSON errors. Provider tests: timeout, 429, missing key and malformed upstream output using simulated HTTP responses. UI checks: success, not found, simulation, loading, mock warning and unreachable backend. Real model quality is verified only through actual NVIDIA calls.

## Limits

Matching quotations establishes provenance, not semantic entailment. Prompt injection resistance and answer correctness are best-effort model behavior and require evaluation. The English keyword mock demonstrates plumbing only; multilingual answer quality belongs to real-provider evaluation. The two-hour budget includes verification and documentation; unfinished work must be disclosed.

## Deployment readiness

WHEN the reviewer deploys the monorepo, the frontend SHALL support Vercel with root directory `frontend` and server-only `BACKEND_URL` pointing to the Render HTTPS origin. The backend SHALL support a Render Python web service rooted at `backend`, with pinned Gunicorn, environment-based production settings and a repository-root `render.yaml`. No database or migrations are required. Production SHALL use DEBUG=false, an externally supplied SECRET_KEY, explicit ALLOWED_HOSTS and correct trusted-proxy HTTPS handling. README SHALL document configuration, deployment order, redeployment after changing BACKEND_URL, free-service cold starts and the distinction between local verification and hosted verification.
