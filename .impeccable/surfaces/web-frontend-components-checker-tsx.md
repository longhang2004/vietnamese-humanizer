---
version: 1
slug: "web-frontend-components-checker-tsx"
primary_target: "web/frontend/components/Checker.tsx"
related_targets: ["web/frontend/app/check/page.tsx","web/frontend/app/contribute/page.tsx","web/frontend/components/ContributeForm.tsx","web/frontend/components/RewritePanel.tsx"]
---

# Editorial workspace layout

Mode: Operate. Scope: checker, findings, rewriting and contribution.

## Direction contract

THESIS: Source text and its review belong to one working region. Keep the source first and the result stable beside it.

OWN-WORLD: Use the existing neutral layers, lime primary action, 16px fields and 44px controls. Native disclosures hold optional choices; borders separate groups without nested cards.

STORY: Paste a draft, adjust checks if needed, submit, then read specific findings. Rewriting remains capability-gated. Contributions pair original and proposed text with explicit consent.

FIRST VIEWPORT: A compact page heading precedes aligned source/result regions. Mobile stacks them in task order; supporting options must not bury submission. Contribution begins with a real route heading and a shrinkable form.

FORM: A continuous editorial workbench inside the established visual system. Retain facts, input limits, consent and stale-result guards.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
