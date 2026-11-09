# Configurable NVIDIA timeout — Design

Status: approved; implemented with live-latency verification pending.

## Decision

Read NVIDIA_TIMEOUT_SECONDS in the NVIDIA adapter at construction, validate its finite numeric range and create an explicit httpx.Timeout with configurable read budget and 5-second connection/write/pool budgets. Preserve a 15-second default for original-contract compatibility; recommend 10 seconds in the private local environment and deployment configuration after approval. Keep the 75-second frontend request limit and the existing Gunicorn command initially; document that cold starts and per-operation timeouts do not establish an overall wall-clock deadline. A later frontend-budget change requires its own evidence.

Use a generic TIMEOUT message such as `The model request timed out. Please try again.` Safe provider logs distinguish ConnectTimeout, ReadTimeout, WriteTimeout and PoolTimeout and record elapsed duration without request content. Invalid timeout configuration maps to the existing public MODEL_UNAVAILABLE error contract.

## Alternatives

- Unlimited waits: rejected because failed requests must terminate visibly.
- Automatic retries: rejected because they increase quota usage and can hide persistent latency.
- Change the selected model: deferred; the user explicitly selected MiniMax M3.1 Flash.
- Immediately attribute the issue to NVIDIA quota: rejected because no 429 or account evidence was supplied.

## Boundaries and risk

Only provider configuration, timeout wording, environment documentation and tests change. Waiting longer can accommodate responses that exceed 15 seconds; it does not repair an outage or guarantee reliability. If verified responses still fail at 10 seconds, use the phase/timing evidence before changing additional budgets or considering another live provider.

The developer moved documentation and render.yaml into `markdwons/`; preserve that work. Do not silently restore or relocate files while implementing this fix. Render Blueprint path consistency is a separate deployment concern.

## References

- HTTPX timeout phases: https://www.python-httpx.org/advanced/timeouts/
- Vercel external-origin timeout: https://vercel.com/docs/errors/router_external_target_error

## Follow-up: local proxy budget alignment

A real POST through the running localhost Next.js proxy returned HTTP 500 and plain `Internal Server Error` after 30.013 seconds, while both Django and the proxy answered GET with JSON 405 and simulated failure with JSON 503. Installed Next.js source (`server/lib/router-utils/proxy-request.js`) confirms a 30,000ms default for development and `experimental.proxyTimeout` configuration. This explains the misleading BACKEND_UNREACHABLE presentation after the approved backend read budget increased to 10 seconds.

Correction within the approved timeout change: configure the local Next.js proxy for 65,000ms, retain browser abort at 75,000ms, and retain the model's configured 10-second read budget. This permits the backend's JSON timeout or answer to arrive after the old 30-second proxy cutoff. It does not change Vercel's external-origin platform limit or guarantee an overall provider deadline.

Latest developer instruction: reduce the configured read timeout from 45 to 10 seconds. This supersedes the earlier 45-second recommendation; the absent-variable fallback remains 15 seconds and other phase budgets remain five seconds.

## Publishing compatibility

The developer requested pushing changes to the connected deployments. Preserve the relocated documentation in markdwons, add a root README entry point, and retain a root render.yaml matching the relocated copy so the existing root-path Blueprint remains usable. Exclude the relocated personal context file. No provider or timeout choice changes during publishing.
