# Configurable NVIDIA timeout — Tasks

Status: approved; tasks 1–3 complete, mock acceptance passed; live checks after restart/deployment remain pending.

1. [x] Add failing provider tests for preserved default, 10-second override, range validation, timeout phase logging and unchanged HTTP 504/no-answer behavior.
2. [x] Implement typed configuration and explicit timeout phases; adjust the error message and safe diagnostic logging. Run the focused tests and full backend suite.
3. [x] Update backend/.env.example and the current documentation/deployment manifest in markdwons/. Apply a private 10-second local override after approval, without exposing credentials or replacing other environment settings.
4. [ ] Check the three acceptance paths and timed live requests where connectivity permits. Save actual outcomes separately from existing test evidence; record residual timeouts rather than claiming the longer budget guarantees a fix.

Evidence: 21/21 backend tests passed after RED→GREEN, mock4/4 passed, independent review found no important findings. Existing source documents/results and user file moves were preserved.

Latest developer instruction: reduce the configured read timeout from 45 to 10 seconds. This supersedes the earlier 45-second recommendation; the absent-variable fallback remains 15 seconds and other phase budgets remain five seconds.
