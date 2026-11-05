# Vietnamese Writing Skills - Frontend UI

Next.js (App Router + TypeScript + Tailwind CSS) website and Vietnamese writing checker. Landing and documentation pages work independently of the checker API. Rewrite and contribution controls follow the backend's advertised capabilities.

## Routes

| Route | Purpose |
| --- | --- |
| `/` | Landing, actual GitHub stars and paired AI outputs |
| `/check` | Editor, selected checks, findings and optional rewrites |
| `/examples` | Six genuine comparison pairs and methodology |
| `/guide` | Web, chatbot and agent usage |
| `/start` | Platform-specific downloads and copyable requests |
| `/about` | Project scope, research and contribution links |
| `/contribute` | Capability-gated form and GitHub fallback |

Visual conventions and skill references are in [DESIGN.md](../../DESIGN.md). Font licenses live in `public/fonts/`.

Comparison inputs and raw outputs live in [the research record](../../docs/research/2026-11-04-web-comparisons/README.md). From the repository root, run `python scripts/export_web_comparisons.py` after changing those records, or add `--check` to verify the published JSON. Keep AI outputs verbatim.

## Quick Start (Local Development)

1. Install dependencies:
   ```bash
   npm install
   ```

2. Copy local environment settings:
   ```bash
   cp .env.local.example .env.local
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

   The web app will open at `http://localhost:3000`.

## Production Build

```bash
npm run build
```

## Checks

```bash
npm run format
npm run lint
npm test
npx tsc --noEmit
```

`npm run lint` checks formatting, ESLint and the pinned Impeccable source detector. `npm run ui:check` runs the detector alone. Generated comparison content and user downloads are kept outside the formatter's source scope.

## Project-local design skills

The complete Impeccable 4.8.0 skill and command references are installed in [`.agents/skills/impeccable`](../../.agents/skills/impeccable/UPSTREAM.md), pinned to upstream commit `c8891a9ae865d6ee311836ae5199bfce0fe115b1`. Its Apache-2.0 license and NOTICE are included. Codex discovers the local skill on the next turn; contributors should read [AGENTS.md](../../AGENTS.md) before UI work.

Route strategy is stored in `.impeccable/surfaces/`. The shared visual system remains in `DESIGN.md`. Impeccable and Prettier are development tools pinned in `package-lock.json`.
