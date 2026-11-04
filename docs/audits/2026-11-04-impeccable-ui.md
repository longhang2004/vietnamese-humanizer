# Impeccable UI audit and refactor — 04 November 2026

Workflow: technical audit, then extraction and polish using the installed Impeccable plugin 4.3.1. This is a scoped manual audit, not a WCAG certification or a Lighthouse result.

Baseline: commit `6958a47`. Preserve the approved graphite/lime identity, Vietnamese copy, six verbatim AI comparison pairs and fail-closed optional capabilities.

## Evidence

One batched baseline inspection covered the landing, checker, examples, guide and chatbot onboarding at desktop and 375px mobile. The mobile content viewport measured 360px after the scrollbar. Screenshots and the detector record are in ignored `build/impeccable-refactor/`.

The bundled detector returned `[]`. Read-only browser automation supports DOM, screenshots, computed styles and keyboard input; mutable detector overlays were not injected.

## Findings

| Priority | Finding | Evidence | Planned correction |
| --- | --- | --- | --- |
| P1 | Onboarding field boundaries have insufficient contrast | Existing border `#2b3846` against `#0b0f14`: 1.61:1; shared control border: 3.26:1 | Reuse the shared field and action classes |
| P2 | Primary checker action is buried on mobile | Submit top measured 1,489px, including expanded defaults and a metadata notice | Disclose optional checks; retain all four defaults; move metadata context below results |
| P2 | Checker panels do not align | A screen-reader-only live region participates in the results stack spacing | Move its announcement outside the two-column layout |
| P2 | Menu cannot close with Escape | Menu remains open after Escape from its toggle | Close and restore toggle focus |
| P2 | Standalone examples skip heading levels | Main outline begins H1 → H3 → H4 | Give the explorer a context-aware heading level |
| P2 | Topic selection announces two full outputs | Both outputs sit inside an atomic live region | Announce the selected topic in a short status |
| P2 | Standalone links and disclosure have small targets | Landing links measured 20–22px high; methodology summary 28px | Apply the existing 44px interaction floor |
| P2 | Install command is difficult to read on mobile | Computed monospace size is 10px | Use 13px text that wraps within the control |
| P3 | Shared UI source is compressed and variants drift | Large JSX/CSS blocks are single lines; onboarding reimplements fields/buttons | Separate formatting commit; reuse current primitives |

The known production backend startup failure is an infrastructure blocker from before this pass. It is not repaired or represented as a successful checker response by these UI changes.

## Audit health

Scores are a bounded code/browser assessment, not an automated certification.

| Dimension | Baseline / 4 | After / 4 | Verification |
| --- | --- | --- | --- |
| Accessibility | 2 | 3 | Headings, short announcements, Escape focus and field boundaries verified; no full assistive-technology certification |
| Performance | 3 | 3 | No new frontend runtime dependency; lab metrics not measured |
| Theming | 3 | 4 | Onboarding reuses shared field/button primitives |
| Responsive design | 2 | 3 | Action depth, touch areas and command readability improved; long forms still scroll |
| Implementation integrity | 3 | 4 | Actual examples preserved; source formatting separated from behavior changes |
| Total | 13 / 20 | 17 / 20 | Scoped manual assessment |

## Verification

- Four regression checks reproduced the original failures before implementation. The full frontend suite now has 45 passing tests, including existing stale-result and capability guards.
- Frontend lint, TypeScript and production build pass. Seven targeted repository tests pass; all six AI pairs and 13 download artifacts remain unchanged.
- An independent code review found no material regression.
- One combined confirmation round covered desktop, 375px mobile and 768px tablet. The checker panels both start at y=233px on desktop. At 375px, the initial submit button moved from y=1,489px to y=812px, a reduction of 677px.
- No horizontal document overflow at the inspected sizes. Standalone landing links and methodology disclosure measure 44px high. Commands render at 13px; onboarding fields render at 16px with the shared control border.
- Escape closes navigation and restores focus. Topic selection announces a short status, with H2 output headings on the standalone examples page. The local checker returns the real sample finding; changing selected checks clears that result.
- Claude onboarding retains its real ZIP link, and the copy action displays confirmation. Screenshots are stored alongside the baseline artifacts. No mutable overlay or detector live server was used.
