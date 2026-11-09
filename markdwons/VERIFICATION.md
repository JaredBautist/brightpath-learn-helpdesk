# Verification record

## Observed checks

| Check | Result | Evidence / boundary |
| --- | --- | --- |
| Python source syntax | PASS | All project Python files parse |
| Django system check | PASS | No issues reported |
| Backend suite | PASS | 16 tests: validator, endpoint and simulated NVIDIA HTTP behavior |
| Mock acceptance | PASS, 4/4 | TEST_RESULTS.mock.md; Django Client, not browser |
| Configured NVIDIA acceptance | PASS, 4/4 | Developer ran the script outside the sandbox; saved TEST_RESULTS.md inspected, including actual model answers and citations |
| Frontend dependency install | PASS from local cache | package-lock.json generated with registry URLs/integrities; network-based fresh install not verified here |
| TypeScript | PASS | npm run typecheck |
| Next production build | LOCAL CHECK BLOCKED; DEPLOYED UI OBSERVED | Agent-local TypeScript subprocess returned empty stdout; Vercel now serves the frontend. Build logs were not independently reviewed |
| Django development socket | BLOCKED | runserver reports Operation not permitted |
| Next development process | LIMITED | Reports Ready, but a separate HTTP probe could not connect; no served-page proof |
| Browser QA | PARTIAL | Later static Chromium screenshots inspected; hydrated application interaction remains unverified (see frontend refinement below) |
| Gunicorn startup | NOT VERIFIED | Pinned for deployment; unavailable in local package cache |
| Vercel / Render | DEPLOYED; PROXY CASES OBSERVED | Public frontend, sourced NVIDIA response on retry, abstention and simulated 503; see HOSTED_TEST_RESULTS.md |
| Secret scan | PASS for deliverable files | Private backend/.env excluded; only placeholders in examples/tests |

The agent sandbox blocks external DNS for PyPI and NVIDIA. The developer subsequently ran the NVIDIA evaluation successfully outside it. Cached packages were used locally (Python 3.14.9, Django 5.2.17, httpx 0.28.1, python-dotenv 1.2.4; Node 22.23.4). This establishes test-client behavior, not a fresh-clone network installation or a running hosted app.

## Review and correction

A separate read-only reviewer found one important issue: Django SecurityMiddleware was absent, so configured SSL redirect and nosniff settings were ineffective. `test_production_https_and_nosniff` first failed (HTTP returned 200 instead of 301); adding SecurityMiddleware made it pass. The complete 16-test suite then passed.

## Decisions and disclosed limits

- NVIDIA and the user-selected model replace the template's Groq/Gemini adapter; optional Ollama is omitted.
- JSON mode defaults off because the selected hosted model's official schema does not document response_format. The configurable option remains available and server parsing always runs.
- Canonical server-generated abstentions are English, a known gap for non-English questions. The mock supports English lexical matching only.
- Cited substrings establish provenance, not semantic entailment or complete prompt injection resistance.
- The developer published the GitHub repository and deployed Render/Vercel. Public code and frontend checks returned HTTP 200. The source archive excludes secrets and dependencies.

## Remaining acceptance work

On a normal networked machine: follow README setup, run npm run build, start both services, exercise the UI success/not-found/failure/backend-unreachable states on desktop and mobile, and retain the successful NVIDIA evaluation. Deploy backend first and then frontend if desired; verify the hosted cases separately. Replace the saved real results only with actual observed outputs.

## Approved frontend refinement

Implemented the approved `.kiro/specs/frontend-polish/` design using UI/UX Pro Max minimal-interface/form guidance and Emil Kowalski design-engineering principles. Updated English product copy, header, spacing, typography, form, provider badge and source cards; extracted HelpHeader and AnswerResult presentation components. Existing API transport, state transitions, failure simulation, mock disclosure and saved NVIDIA outputs were preserved.

Observed checks:

- `npm run typecheck`: PASS after the component extraction.
- Standalone TypeScript compilation and React server rendering: PASS for the initial page and all four saved NVIDIA response states (supported answer, abstention, outage and lesson completion). This does not exercise browser submission or hydration.
- Text color contrast: 18 measured foreground/background combinations passed 4.5:1 in light and dark themes, including secondary copy, primary-button normal/hover, mock notices and errors.
- Static screenshots: inspected Chromium output at 1200px light, 375px light and 768px dark with reduced-motion flags. The initial form fits the inspected widths and the mobile actions stack. Screenshots use actual component markup and CSS, without a Next server or live backend. Browser launches needed an explicit writable user-data directory; attempts involving DOM dump output were blocked by socket restrictions.
- `npm run build`: still blocked by Next's TypeScript subprocess returning empty stdout. The production build is not established by these checks.
- Remaining: hydrated application success/abstention/failure, real keyboard/touch interaction, 1440px/zoom inspection and a production build outside the agent sandbox. See the refinement regression checklist in MANUAL_TESTS.md.

A separate read-only review of the frontend refinement found no important actionable findings. It confirmed preservation of transport/state, honest provider/mock identification, source content and basic accessibility structure.

## Developer-reported manual review and time

The developer reports approximately 90 minutes of active work, including development, substantial debugging/corrections, review of AI-assisted code against the SDD specifications and manual testing. This is a developer-reported total, not an elapsed-time measurement by the agent. Individual manual case outcomes were not provided, so MANUAL_TESTS.md has not been automatically marked PASS. No new production-build or hosted-deployment result was supplied.

NVIDIA remains the only live adapter; the exact account quota and remaining allowance have not been checked. The mock is an explicit alternative for local demonstration, not automatic live-provider failover.

## Hosted deployment verification

See [HOSTED_TEST_RESULTS.md](HOSTED_TEST_RESULTS.md) for observed responses through the public Vercel proxy. The frontend and GitHub repository returned HTTP 200 without credentials. The developer supplied a screenshot showing the hosted coaching answer and NVIDIA badge. The agent observed a first coaching TIMEOUT (504), then a successful retry (200, nvidia, DOC2), correct unknown-information abstention (200, nvidia), and simulated MODEL_UNAVAILABLE (503, no answer). Earlier agent-local limitations above describe historical attempts; hosted operation is now established for these cases. The exhaustive manual/browser checklist and clean-install reproduction remain outstanding.

The repository Blueprint now declares LLM_PROVIDER=nvidia, matching the working Render configuration, instead of its original mock default. NVIDIA_API_KEY remains sync:false and private to the platform; no credential was added to the manifest.

## Approved configurable timeout adjustment

After repeated local 504 reports, the developer approved retaining MiniMax with a configurable read budget. The adapter fallback remains 15 seconds; the local private environment, environment example and current Blueprint specify NVIDIA_TIMEOUT_SECONDS=45. Connection/write/pool budgets are five seconds. Invalid, infinite and out-of-range settings fail before a provider call. Timeout responses retain HTTP 504/TIMEOUT without an answer; the message no longer claims an invariant 15-second total. Logs contain phase, elapsed time and model identifier, not request content or credentials.

Observed verification: new tests first failed against the old adapter; the complete suite then passed 21/21 after implementation. Mock acceptance passed 4/4 with output written to a temporary file, preserving the developer's existing saved results. A separate read-only review found no important actionable findings. These checks establish configuration and error behavior, not improved real-provider latency. Existing hosted evidence predates this adjustment. A fresh probe of the original Render origin received no bytes within its 35-second client limit; that cannot establish a specific NVIDIA timeout phase. Restart/redeploy and repeat real questions before claiming the latency issue resolved.

## Local proxy cutoff diagnosis

Django and the Next.js local proxy returned JSON 405; local simulated POST returned JSON 503. A real local proxy POST then returned HTTP 500 with plain Internal Server Error at 30.013238 seconds. Installed Next.js 16.4 code confirms a 30-second development proxy default. The local proxy budget was aligned to 65 seconds through its supported experimental.proxyTimeout setting, retaining the browser 75-second and configured model read 45-second budgets. This addresses premature proxy failure; genuine provider timeouts remain explicit.

## Direct NVIDIA diagnostic (2026-11-09T06:02:43.502949+00:00)

One direct hosted chat-completions request used the current private local credential, existing model, full document prompt, temperature 0, non-streaming output and 2048-token ceiling. HTTP 200 arrived after 26.444455 seconds to first byte (26.444849 seconds total). The response reported minimaxai/minimax-m3.1-flash, finish_reason=stop, 180 completion tokens including 128 reasoning tokens. Server answer validation passed with a verified quote. This proves that credential/model access worked for this request; it does not rule out intermittent timeouts or establish the phase of the developer’s failing request. No application behavior was changed in this diagnostic. The temporary credential header was deleted; no credential or raw prompt was recorded here.

## Latest timeout setting: 10 seconds

The developer explicitly requested reducing the configured read budget from 45 to 10 seconds. Private local environment, environment example and current Blueprint now specify NVIDIA_TIMEOUT_SECONDS=10. The adapter fallback remains 15 seconds when absent, connection/write/pool remain five seconds, and local proxy/browser budgets are unchanged. Earlier 45-second entries are historical. This change cancels slow operations sooner; the measured direct NVIDIA response took 26.4 seconds, so the new budget may increase timeout frequency. The application still returns TIMEOUT rather than inventing a result.
