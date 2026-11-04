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
npm test -- --run
npm run lint
npx tsc --noEmit
```
