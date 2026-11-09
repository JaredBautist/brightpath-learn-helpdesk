# Configurable NVIDIA timeout

Status: approved by the developer; implemented with live-latency verification pending.

## Evidence

The current NVIDIA adapter uses a hardcoded `15.0` second httpx timeout and maps timeout exceptions to HTTP 504/TIMEOUT. The developer supplied four repeated local Django 504 logs. This is evidence of repeated request failure, not proof of an invalid key, exhausted quota or complete model outage. A subsequent agent probe of the Render origin received no bytes within a 35-second client limit; that observation cannot distinguish backend wake-up, transport delay or provider latency.

## Acceptance criteria

1. WHEN NVIDIA_TIMEOUT_SECONDS is absent, the backend SHALL preserve the original 15-second timeout default.
2. WHEN NVIDIA_TIMEOUT_SECONDS is a finite number from 5 through 60, the backend SHALL apply it to the model's read timeout; the recommended deployment override SHALL be 10 seconds. Connection, write and pool timeout budgets SHALL be 5 seconds.
3. WHEN configuration is invalid, the request SHALL fail explicitly with a safe configuration-error message using the existing MODEL_UNAVAILABLE envelope, without contacting NVIDIA or returning an answer.
4. WHEN an operation times out, the API SHALL retain HTTP 504/TIMEOUT, use wording that does not falsely claim a fixed 15-second total, and never silently switch to mock.
5. WHEN diagnosing provider failures, safe logs SHALL identify timeout phase, elapsed duration and model identifier; they SHALL NOT contain the API key, headers, full prompts, questions or answer content.
6. Existing API response shapes, provider identity, validation, simulation and citation behavior SHALL remain unchanged. No automatic retries or model switch SHALL be introduced.

7. WHEN a local backend request takes longer than 30 seconds but completes within the configured 65-second proxy budget, Next.js SHALL forward its JSON response rather than prematurely return a plain-text proxy failure. The browser budget remains 75 seconds.

Latest developer instruction: reduce the configured read timeout from 45 to 10 seconds. This supersedes the earlier 45-second recommendation; the absent-variable fallback remains 15 seconds and other phase budgets remain five seconds.
