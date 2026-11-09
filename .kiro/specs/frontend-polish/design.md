# Frontend polish — Design

Status: approved by user and implemented; verification limits recorded in VERIFICATION.md.

## Visual direction

A restrained learning help center: warm ivory canvas, white surfaces, deep evergreen text and primary action, muted sage accents. Retain the existing green identity and improve its hierarchy rather than introducing a new brand. Use a system sans-serif stack without network font downloads, a 4/8px spacing rhythm, 16px body text, generous form padding, fine borders and restrained surface depth.

Desktop: compact brand masthead and Help Center label; short editorial heading and supporting line; a distinct question workspace; response and document citations below. Keep a readable single column around 800px instead of adding a sidebar for a three-document corpus. Mobile stacks actions naturally without horizontal overflow.

Proposed copy: header label `Help Center`, heading `How can we help?`, description `Ask about your lessons, coaching, or account. Get answers with supporting sources.` The footer contains `A fictional BrightPath Learn project.` Technical limitations remain documented in README; the form and loading text use concise product language. The failure checkbox remains visible with its existing label for reviewer testing.

## Review using Emil Kowalski's format

| Before | After | Why |
| --- | --- | --- |
| FICTIONAL DEMO in the main brand line | Help Center; fictional disclosure in footer | Focus the hierarchy on the member's task while retaining transparency |
| Large explanatory heading and several technical statements | Short heading, concise context and quieter metadata | Make the question form the primary action |
| Plain card with little visual hierarchy | Deliberate spacing, consistent border/radius tokens and stronger action contrast | Improve readability without adding screens |
| Button has no press feedback | Pointer-only 120–160ms scale feedback | Acknowledge clicks without delaying keyboard actions |
| Result and sources have similar visual weight | Clear answer heading and structured citation rows | Make supporting evidence easy to inspect |

## Architecture and contracts

`frontend/app/page.tsx` remains the state-owning container. Extract presentational `HelpHeader` and `AnswerResult` into `frontend/components/help/` only where this makes the existing JSX easier to read; consume existing `AskResult` types from `lib/api.ts`. The form stays with its current local state; no new store or provider. Keep the transport module unchanged.

`globals.css` defines semantic color, space, radius and timing tokens. Use ordinary CSS and small inline decorative SVGs with aria-hidden where useful. Never use icons as substitutes for visible field labels. Loading announces actual work without percentage progress or connection-success claims. Provider metadata is unknown until a successful response, as before.

## ADR-004: Restrained help-center refinement

Context: the user wants less of a mockup appearance and explicitly requests UI/UX Pro Max and Emil Kowalski guidance.

Decision: polish the current single-column help-center layout with plain CSS and small presentational boundaries. Apply UI/UX Pro Max's verified Minimalism & Swiss Style result (spacing, hierarchy, contrast, responsive layout) and form-feedback guidance. Apply Emil's fast, interruptible pointer feedback and reduced-motion principles.

Considered and rejected: a two-column support portal adds empty structure for this small corpus; a marketing landing page adds irrelevant sections. The initial skill design-system search returned testimonials and neumorphism, which do not fit this task and were rejected. Narrower style and UX searches returned relevant guidance. Next.js search suggestions about Server Actions concern a different architecture; retain the approved Django API and local request state.

Consequences: no animation library or new dependencies. No entrance choreography, animated layout sizes or fake product status. Disclosure is quieter; actual mock status remains prominent when applicable. Visual verification requires a working browser and will be reported separately from TypeScript/build checks.
