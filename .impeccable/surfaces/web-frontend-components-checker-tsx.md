---
version: 2
slug: "web-frontend-components-checker-tsx"
primary_target: "web/frontend/components/Checker.tsx"
related_targets: ["web/frontend/app/check/page.tsx","web/frontend/app/contribute/page.tsx","web/frontend/components/ContributeForm.tsx","web/frontend/components/Editor.tsx","web/frontend/components/RewritePanel.tsx","web/frontend/components/workspace.module.css"]
---

# Editorial workspace layout

Mode: Operate. Scope: checker, findings, multi-skill rewriting, inline word diff and contribution.

## Direction contract

THESIS: Source drafting belongs on archival paper while rule diagnostics belong on the dark lacquer inspector column; keep source first and findings aligned cleanly beside it.

OWN-WORLD: Archival calico ivory drafting surface (`#f3efe4`) on `.source` paired with deep forest cabinet `.review` (`#11211e`), CSS `:has(:checked)` check indicators, sharp 4px–6px corners, 44px controls, chrome-brass submit CTA, and paper/vermilion `<del>`/`<ins>` word diff marks in `.rewriteOutput`.

STORY: Paste or sample Vietnamese prose on paper, toggle any of the four checks, inspect location-pinned findings on the cabinet column, unlock any of the four skills or spoken/satire presets for capability-gated rewriting, verify word changes with inline diff, and re-apply to the draft loop.

FIRST VIEWPORT: Compact page heading precedes the paired ivory-source / forest-findings workbench. Mobile stacks in task order without burying submission. Contributions keep original and proposed drafts together on dual ivory sheets.

FORM: Dual-ground proofreading desk harmonized with the v2 Archival Specimen Cabinet system (`seed:b3b4e67a046e1d61`), preserving facts, character limits, consent and stale-result guards.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
