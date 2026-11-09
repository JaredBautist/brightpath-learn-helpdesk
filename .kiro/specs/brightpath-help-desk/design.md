# BrightPath Help Desk — Design

Status: approved by user; implementation delivered with verification limitations recorded in VERIFICATION.md.

## Boundaries and flow

`Next.js page → same-origin rewrite → Django view → ask use case → LLMProvider → parser/validator → JsonResponse`.

`qa/docs.py` loads immutable document records (ID, title, filename, text). `qa/prompt.py` builds the corpus-labelled system prompt. `qa/service.py` orchestrates generation and validation without HTTP concerns. `qa/views.py` validates requests and maps application errors to HTTP. The Provider Adapter pattern isolates NVIDIA HTTP from the use case; a Protocol defines `generate(system: str, user: str) -> str`. No Repository is justified for three static files.

The frontend uses local React state and a small typed API module. Components render transport results without implementing answer rules. A neutral, accessible single-page form uses plain CSS and supports keyboard interaction, responsive layout and system color preference.

## Contracts

Request: JSON object with `question: string`; trim outer whitespace, reject empty or over 500 characters. The question is untrusted data, never system instructions.

Model output: `{ "answerable": boolean, "answer": string, "sources": [{ "docId": string, "quote": string }] }`.

Success: `{ "ok": true, "provider": "nvidia" | "mock", "answerable": boolean, "answer": string, "sources": [{ "docId": string, "title": string, "file": string, "quote": string }] }`.

Failure: `{ "ok": false, "errorType": string, "message": string }` with no answer field.

| Error | HTTP |
| --- | --- |
| BAD_REQUEST | 400 |
| RATE_LIMIT | 429 |
| INVALID_MODEL_OUTPUT | 502 |
| MODEL_UNAVAILABLE, MISSING_API_KEY | 503 |
| TIMEOUT | 504 |

JSON route/method/internal errors additionally use NOT_FOUND (404), METHOD_NOT_ALLOWED (405), INTERNAL_ERROR (500). A minimal JSON error middleware prevents Django decorators and unexpected exceptions from returning HTML; debug settings must not bypass it.

## Validation and honest behavior

Strip enclosing markdown fences, parse JSON, validate exact field types and reject empty answers. Reject malformed source shapes; drop unknown IDs, empty quotes and quotes absent after case/whitespace normalization. If an affirmative answer has no valid source, replace it with an unavailable answer and empty sources. Negative answers always have empty sources. Apply the support referral requirement to negative pricing/refund/placement answers. Never expose upstream response bodies, credentials or prompts through errors or logs.

The mock tokenizes sentences, removes punctuation/stopwords and ranks overlap, returning up to two exact sentences. It explicitly abstains on pricing/refunds/job placement and below the overlap threshold. Language limitations are documented. It is never represented as an LLM.

## ADR-001: Model provider

Context: the original template mentions Groq/Gemini, but the user explicitly selected NVIDIA.

Decision: implement `nvidia.py` and `mock.py`; skip optional Ollama and other providers. NVIDIA uses plain httpx with the hosted chat-completions endpoint, temperature zero, non-streaming responses and a 15-second timeout. `NVIDIA_API_KEY`, `NVIDIA_MODEL` and model-dependent JSON-mode configuration live in the backend environment; the example supplies a model default to verify against the catalog during implementation. Explicit provider selection takes precedence over automatic selection.

Considered/rejected: additional cloud/local adapters increase verification time without serving the five requirements. A heavy SDK adds unnecessary dependency surface. JSON mode is enabled when supported by the selected model; server validation always runs.

Consequences: API provider union and docs intentionally replace `groq` with `nvidia`. Free-account access, quotas and available models must be checked; they are not guaranteed. Real-provider acceptance remains unverified without an actual credential and successful evaluation.

## ADR-002: Corpus and persistence

Decision: include all three documents in each system prompt, with DOC1–DOC3, titles and filenames. `DATABASES = {}`, minimal installed apps/middleware, no migrations, sessions, auth, admin or DRF.

Considered/rejected: embeddings/vector storage and a database add setup and code without retrieval value for this corpus. Full context stops scaling when token cost, latency or context limits grow. Future improvement: top-k chunk retrieval with chunk citations and an evaluation set.

## Security and runtime

Bind local development servers to loopback. No auth or multi-tenancy is needed for this local exercise; production hardening beyond this public take-home demo, including rate limiting, remains a documented limitation. Keep the API key only in ignored backend `.env`. No NEXT_PUBLIC secrets. The stateless API is CSRF exempt; Next.js rewrites `/api/:path*` to server-only BACKEND_URL. Environment examples contain placeholders only. No paid hosting or publication is implied.

## ADR-003: Vercel frontend and Render backend

Context: the user requests readiness for these deployment platforms.

Decision: retain the monorepo; Vercel builds `frontend` and proxies `/api/*` to the HTTPS Render origin using the existing Next.js rewrite. Set BACKEND_URL before the Vercel build and redeploy after changes. Render runs `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` from `backend`; install pinned requirements without migrations. Add a repository-root render.yaml with a free web-service plan, generated SECRET_KEY, DEBUG=false, configurable ALLOWED_HOSTS and provider variables. The NVIDIA key is configured privately in Render. Trust the platform HTTPS proxy header only in the deployment configuration. No static-file server is required because Django serves only JSON.

Considered/rejected: a static frontend export cannot supply the required Next.js rewrite; moving Django into Vercel changes the requested deployment topology.

Consequences: backend deployment precedes frontend configuration. Render free-service cold starts can delay the first response independently of the 15-second model timeout. A public unauthenticated API may consume provider quota; state this limitation in the README. Local build checks establish readiness only; hosted operation requires actual deployment verification.

References: [Render Django deployment](https://render.com/docs/deploy-django), [Render free services](https://render.com/docs/free), [Vercel rewrites](https://vercel.com/docs/routing/rewrites).

## Provider model selection

The user selected `minimaxai/minimax-m3.1-flash` on NVIDIA hosted `https://integrate.api.nvidia.com/v1/chat/completions`. The model remains environment-configured through NVIDIA_MODEL; no model identifier is hardcoded in application code. Verify JSON-mode support and actual response quality with the selected model.
