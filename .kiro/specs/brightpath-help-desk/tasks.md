# BrightPath Help Desk — Tasks

Status: approved and implemented. See VERIFICATION.md for completed checks and environment-blocked verification.

1. [x] Documents, prompt and validation (20 minutes): create the verbatim corpus, typed contracts, errors and prompt; write parser and quote-verification tests, implement helpers, run the tests.
2. [x] Mock and Django API (25 minutes): add minimal settings, provider Protocol, mock, ask use case, JSON middleware and endpoint. Test answerable/unanswerable requests, input limits, 404/405/500 JSON and both failure switches. Verify with the Django client before continuing.
3. [x] NVIDIA adapter (15 minutes): confirm official endpoint/model capabilities, add environment configuration and HTTP mapping. Test timeout/429/network/malformed responses and explicit missing credentials; never silently fall back after failure. Run a real smoke test only when a local key is available.
4. [x] Next.js UI (25 minutes): add typed API module, page, plain CSS, badge, disclaimer, counter, citations and distinct response/error states. Add the rewrite, dependency lockfile and environment example. Run TypeScript/build and browser checks of the critical states where tooling permits.
5. [x] Evaluation and evidence (20 minutes): implement `scripts/run_cases.py` with Django setup and assertions for actual content/citations. Run mock cases into TEST_RESULTS.mock.md and real NVIDIA cases into TEST_RESULTS.md when credentials are available. Never label mock evidence as real results.
6. [x] Handoff (15 minutes): write README and the submission walkthrough, document tradeoffs and limitations, include the AI-tool disclosure, scan for secrets and run final relevant checks. Provide exact startup/test commands, local credential instructions and ten interview discussion points.

## Proposed files

```text
.kiro/specs/brightpath-help-desk/{requirements,design,tasks}.md
backend/
  manage.py, requirements.txt, .env.example
  config/{__init__,settings,urls,wsgi}.py
  qa/
    {__init__,views,service,docs,prompt,validate,errors,middleware}.py
    llm/{__init__,base,nvidia,mock}.py
    tests/{__init__,test_validate,test_api,test_providers}.py
  docs/{01-getting-started,02-coaching-and-feedback,03-account-help}.md
  scripts/run_cases.py
frontend/
  package.json, package-lock.json, next.config.js, .env.example
  tsconfig.json, next-env.d.ts
  app/{page.tsx,layout.tsx,globals.css}
  lib/api.ts
README.md, SUBMISSION.md, TEST_RESULTS.md, TEST_RESULTS.mock.md, .gitignore
```

The structure keeps the requested monorepo and small `qa` feature intact. The extra service and middleware separate orchestration and JSON error handling from the Django view; the frontend API module isolates transport from rendering. No additional architectural framework is needed. Add repository-root `render.yaml`; pin Gunicorn in backend requirements.

## Deployment additions to tasks 4 and 6

- [ ] Verify the frontend production build with an HTTPS BACKEND_URL and document Vercel root/build/environment settings.
- [ ] Add Render blueprint, Gunicorn command and production environment settings; check Django production configuration and server startup locally where supported.
- [ ] Document backend-first deployment, private NVIDIA configuration, Vercel redeploy requirements, cold starts and any unverified hosted behavior. Actual publication is outside this preparation step.

Implementation checkboxes indicate code/artifacts delivered, not that environment-blocked acceptance checks passed. NVIDIA required cases now pass outside the sandbox (TEST_RESULTS.md). Broader model quality, full Next build, browser QA and hosted verification remain pending.

Hosted update: Vercel frontend and Render backend are now live. See HOSTED_TEST_RESULTS.md for public proxy checks, the timeout/retry observation and remaining verification limits. The Render blueprint provider was aligned with the activated NVIDIA deployment.
