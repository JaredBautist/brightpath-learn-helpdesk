# Test submission answers

Copy the text under each field into the submission form. The checked public code and demo links are included below; the reported active work time is recorded below. Add a demo or video URL only if it exists and opens without reviewer credentials. The invitation deadline supplied in the form is November 9, 2026, at 9:38 p.m. COT; active work time must be reported separately from the invitation window.

## Links to your work

Public code first, then the deployed demo. Both responded to unauthenticated checks. The form accepts up to three links, one per line.

```text
https://github.com/JaredBautist/brightpath-learn-helpdesk
https://brightpath-learn-helpdesk.vercel.app
```

## Walk me through your work

I built a small document-grounded help desk for the fictional BrightPath Learn platform using a Next.js/React/TypeScript frontend and a Django JSON API. It uses NVIDIA's hosted `minimaxai/minimax-m3.1-flash` model with the three supplied fictional documents as its sole reference corpus. The interface displays answers with document titles, filenames and quoted evidence, distinguishes missing information from errors, and includes an API-failure simulation checkbox.

I kept the architecture small: all three documents are included in the model prompt, with no database, embeddings or vector store. Server-side validation checks the model's JSON structure, document IDs and quotations using case/whitespace-normalized matching against the document text. An affirmative response with no surviving verified quotation is downgraded to an unavailable-information response. This verifies quotation provenance, not whether the answer is semantically supported. Provider failures never silently fall back to a fabricated answer. A separate, clearly labelled keyword mock supports setup without a key.

I led the project using Spec-Driven Development (SDD): requirements and acceptance criteria came first, followed by design decisions and an ordered implementation plan, saved under `.kiro/specs/`. I selected the stack and NVIDIA model, approved the specifications before implementation, and audited the work against the agreed requirements. I reviewed the proposed behavior and results, questioned the provider configuration and execution environment during debugging, and ran the real-provider acceptance script locally. I also reviewed AI-generated code, worked through debugging and corrections, performed manual checks, and directed and approved the frontend refinement.

I used OpenAI Codex as a coding assistant to draft specification artifacts and generate implementation code, tests and documentation. My role included technical direction, audit, acceptance decisions and real-provider testing throughout the process; Codex assisted with implementation and automated checks.

The frontend was refined into a restrained Help Center with responsive layout, light/dark themes, accessible labels and reduced-motion handling. Provider identification and the mock disclaimer remain explicit.

The saved run configured for NVIDIA passed all three required cases and one bonus case:

| Case | Observed result |
| --- | --- |
| Supported question: “How often is the group coaching session and where do I find the link?” | Answered every Tuesday at 16:00 UTC, with the link on the Coaching page 30 minutes before the session. Cited DOC2 with the relevant quotations. |
| Unknown information: “How much does BrightPath Learn cost and can I get a refund?” | Returned `answerable: false`, stated that the information is not available in the supplied documents, referred to support@brightpath.example, and returned no sources or invented prices. |
| Simulated API failure: “When is coaching?” | Returned HTTP 503 with `MODEL_UNAVAILABLE`, a clear retry message and no answer field. The failure is deliberately raised before a provider call; it does not establish that NVIDIA itself was unavailable. |
| Bonus: “Does watching the video mark the lesson complete?” | Answered no and instructed the member to select Mark complete, citing DOC1. |

The observed outputs are saved in `TEST_RESULTS.md`; the separate mock run is saved in `TEST_RESULTS.mock.md`. Twenty-one backend tests cover parsing, quotation validation, endpoint behavior and simulated provider failures. TypeScript checks passed. Static React rendering covered the initial page and the four saved response states; static screenshots covered desktop, mobile and dark mode, and 18 text/background contrast checks passed. I also performed manual checks of the application. Their individual outcomes have not yet been recorded in the manual checklist, so I distinguish them from the saved automated results rather than claiming that every manual case passed.

The app is deployed with Next.js on Vercel and Django on Render. Hosted checks through the Vercel proxy observed the required sourced-answer, abstention and simulated-failure behaviors. The supported question timed out once and succeeded on retry; the developer also demonstrated the successful answer in the hosted UI. Outputs are recorded in `HOSTED_TEST_RESULTS.md`.

One improvement would be an evaluation set measuring answer correctness, citation relevance and abstention. As the corpus grows, I would introduce embeddings and top-k chunk retrieval with per-chunk citations, using that evaluation set to measure whether retrieval improves results.

## Video walkthrough (optional)

If recorded, paste a publicly accessible video URL of up to three minutes here:

```text
[OPTIONAL: REPLACE WITH VIDEO URL OR LEAVE THE FORM FIELD EMPTY]
```

A recording outline is kept locally and excluded from the repository. Written answers are sufficient; a video is not required.

## How much time did you spend?

Approximately 90 minutes (1 hour 30 minutes). This included development, with much of the time spent debugging and correcting errors, reviewing AI-assisted code against the SDD specifications, and performing manual tests to verify the application's behavior.

## What tools did you use?

- **OpenAI Codex:** Specification drafting, implementation, tests, debugging, automated review and documentation within my SDD workflow. I set requirements, approved the design, audited the work and ran the real NVIDIA evaluation locally.
- **NVIDIA hosted API / `minimaxai/minimax-m3.1-flash`:** the application's real language model, called from the backend over HTTP. The key is configured privately through environment variables and excluded from the submission.
- **Python, Django 5.2 and httpx:** the stateless JSON API, provider adapter and HTTP failure handling. **python-dotenv** loads local environment configuration; **Gunicorn** is configured as the Render startup server.
- **Next.js 16.4, React 19.3 and TypeScript 5.9:** the single-page frontend, typed API client and same-origin backend proxy. Styling is plain CSS with system fonts; no prebuilt UI kit or purchased template was used.
- **Django test Client and Python unittest:** backend tests and the acceptance script that saves real/mock results.
- **Chromium and React static rendering:** limited visual checks of the generated markup on desktop/mobile and in dark mode. They were not a full interactive browser acceptance run.
- **UI/UX Pro Max and Emil Kowalski design-engineering skills:** guidance for hierarchy, spacing, contrast, accessible states, responsive layout and restrained interaction feedback during the frontend refinement.

## What is unfinished or limited?

The main operational limitation is that NVIDIA is the only live model provider currently integrated. I have not verified the exact quota or remaining allowance for my account, so continued access depends on NVIDIA's availability and account limits. After observing repeated timeouts, I retained MiniMax and approved a configurable read timeout: 10 seconds in the current local/deployment configuration, with the original 15-second fallback and separate five-second connection/write/pool budgets. Safe logs identify timeout phase and duration without credentials or question content. The adjustment passes automated tests; its impact on live latency remains to be checked after deployment. The app handles rate limits, unavailable responses and timeouts explicitly; it does not silently replace a failed real call with a mock answer. A clearly labelled mock is available for local use, but it does not establish AI answer quality. The provider interface would allow another live adapter to be added later.

The app is deployed and publicly accessible on Vercel and Render. The required hosted API behaviors were observed, including a successful NVIDIA response through the frontend proxy. One supported request returned HTTP 504/TIMEOUT before succeeding on retry, so provider latency and free-host cold starts remain practical limits. A fresh-clone installation and a reproducible local production build have not been verified; the earlier agent-local build failed on empty TypeScript subprocess output. Hosted operation is now confirmed, but build logs and an exhaustive manual/browser checklist have not been independently audited.

Quotation matching establishes that a quote exists in the documents, not that every claim is supported. The evaluation is small; broad answer quality and prompt-injection resistance are not established. The mock and canonical server-generated abstentions are English. Authentication, application rate limiting and persistence were intentionally excluded from this small exercise.

Next I would verify the account's actual NVIDIA limits, reproduce the build from a fresh checkout and expand the answer-quality evaluation set before adding functionality.

## Before submitting — personal completion

- [x] Include code and demo URLs; unauthenticated HTTP checks returned 200.
- [x] Record active work time: approximately 90 minutes, reported by the developer.
- [ ] Confirm that the authorship description accurately reflects your work; add any personally implemented changes if applicable.
- [ ] Complete the remaining manual/browser checklist and fresh-checkout build verification.
- [x] Include the checked demo URL; leave the video field empty unless a recording is available.
- [ ] Submit source files without private `.env` files, credentials or dependency folders.
