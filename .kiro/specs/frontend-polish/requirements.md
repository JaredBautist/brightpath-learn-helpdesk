# Frontend polish — Requirements

Status: approved by user and implemented; verification limits recorded in VERIFICATION.md.

## Intent

Give BrightPath Learn the appearance of a small, credible learning help center. Replace prominent technical-demo wording with product-oriented English copy while retaining truthful provider identification and mock disclosures. This is a modest visual refinement of the existing take-home app, not a new product scope.

## Acceptance criteria

1. WHEN the page opens, it SHALL show BrightPath Learn branding, a Help Center label, a concise question-focused heading and the existing question form. The prominent FICTIONAL DEMO label SHALL be removed; a discreet footer SHALL retain the fictional-project disclosure.
2. WHEN a provider has been identified, the page SHALL preserve its actual name. WHEN that provider is mock, its badge and explicit non-AI warning SHALL remain visible.
3. WHEN an answer is returned, the answer SHALL have clear visual priority and citations SHALL retain document titles, filenames and exact quotes. Abstentions and errors SHALL remain distinct and shall not imply successful answers.
4. WHEN using desktop, mobile, keyboard, light mode, dark mode or reduced motion, the page SHALL remain readable, navigable and usable. Text contrast SHALL target WCAG AA; controls SHALL have visible focus and at least 44px touch targets.
5. WHEN submitting questions or using the failure checkbox, the existing API contract, 500-character limit, disabled/loading states and stale-answer clearing SHALL remain unchanged.
6. WHEN pointer feedback animates, it SHALL use short transform/opacity transitions, gated hover and reduced-motion handling. Keyboard interactions SHALL not receive movement animations.

## Scope

No new dependencies, backend changes, extra routes, sample answers, chat history, decorative dashboard statistics, fake navigation or model claims. Existing source documents and saved NVIDIA results remain intact.
