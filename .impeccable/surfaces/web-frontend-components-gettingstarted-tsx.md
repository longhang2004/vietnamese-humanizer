---
version: 1
slug: "web-frontend-components-gettingstarted-tsx"
primary_target: "web/frontend/components/GettingStarted.tsx"
related_targets: ["web/frontend/app/start/page.tsx"]
---

# Chatbot onboarding layout

Mode: Operate. Scope: platform/task selection and real setup instructions.

## Direction contract

THESIS: Separate choosing a tool from carrying out its setup. Avoid one long box containing every stage.

OWN-WORLD: Reuse the approved dark palette, readable labels, native selection and shared field/button primitives.

STORY: Choose a platform and writing task, see the matching instructions or download, then copy a usable request. Keep the real platform URLs and package sizes.

FIRST VIEWPORT: A concise heading introduces a compact choice region beside the selected setup on desktop. On mobile, choices come first, then setup and prompt in the same DOM order. The launch/download action stays with its instructions.

FORM: A selection rail and task-focused instructions. Remove the duplicate decorative step strip. Advanced installation references remain a native disclosure.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
