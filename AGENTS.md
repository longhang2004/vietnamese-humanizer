# Project instructions

## Terminal

Run routine terminal commands in Ubuntu on WSL2 with Bash. On Windows, use PowerShell only as the launcher for `wsl.exe --distribution Ubuntu --cd <Linux-path> --exec bash -lc '<command>'`. Keep filesystem operations in that Bash session. Use native Windows tooling only for a Windows-specific operation and explain why.

## Frontend work

- Read `.agents/skills/impeccable/SKILL.md` for design, layout, UI copy and frontend changes. Use the repo-local version so every contributor applies the same rules.
- Read `PRODUCT.md`, `DESIGN.md` and the relevant `.impeccable/surfaces/` brief. The approved direction is a dark technical interface with readable Vietnamese.
- Preserve genuine comparison outputs in `web/frontend/content/comparisons.json`; update them only through their exporter and recorded source files.
- Keep optional features gated by backend capabilities. Text edits and changed checks must invalidate old results.
- Run `npm run format` after editing UI source. Before shipping, run `npm run lint`, `npm test` and `npm run build` from `web/frontend`. Lint includes formatting and the pinned Impeccable detector.
- Impeccable is project tooling under `.agents/skills`; the four user-facing Vietnamese writing skills remain under `skills/`.
