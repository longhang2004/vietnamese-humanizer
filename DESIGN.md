---
name: Vietnamese Writing Skills
description: Dual-ground archival editorial cabinet for reviewing and editing Vietnamese with context.
colors:
  background: "#0b1614"
  surface: "#11211e"
  surface-raised: "#182e2a"
  border: "#25403b"
  control-border: "#486b64"
  foreground: "#f2efe6"
  muted: "#a3b8b1"
  paper: "#f3efe4"
  paper-subtle: "#e7e1d1"
  paper-border: "#c9bfaa"
  paper-control-border: "#7d7563"
  paper-ink: "#141c1a"
  paper-muted: "#44544f"
  paper-accent: "#184d3b"
  accent: "#e8c55a"
  accent-hover: "#f2d57c"
  accent-ink: "#141a10"
  vermilion: "#f06b54"
  danger: "#ffb4b8"
  danger-paper: "#a82419"
  warning: "#f0c265"
  guided-surface: "#f3efe4"
typography:
  display:
    fontFamily: "Be Vietnam Pro, Segoe UI, sans-serif"
    fontSize: "clamp(42px, 5vw, 72px)"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "Be Vietnam Pro, Segoe UI, sans-serif"
    fontSize: "38px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.03em"
  workspace-heading:
    fontFamily: "Be Vietnam Pro, Segoe UI, sans-serif"
    fontSize: "2rem"
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "-0.03em"
  body:
    fontFamily: "Be Vietnam Pro, Segoe UI, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.7
  reading:
    fontFamily: "Be Vietnam Pro, Segoe UI, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.85
  label:
    fontFamily: "Be Vietnam Pro, Segoe UI, sans-serif"
    fontSize: "14px"
    fontWeight: 600
    lineHeight: 1.4
  command:
    fontFamily: "JetBrains Mono, monospace"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.7
rounded:
  field: "4px"
  button: "4px"
  panel: "6px"
spacing:
  inline-gap: "12px"
  field-block: "11px"
  control-inline: "20px"
  panel-padding: "24px"
  desktop-gutter: "32px"
  mobile-gutter: "18px"
  reading-gap: "56px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.accent-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.button}"
    padding: "11px 20px"
  button-primary-hover:
    backgroundColor: "{colors.accent-hover}"
  button-secondary:
    textColor: "{colors.foreground}"
    typography: "{typography.label}"
    rounded: "{rounded.button}"
    padding: "11px 20px"
  field:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.field}"
    padding: "11px 13px"
  surface-panel:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.panel}"
---

# Design System: Vietnamese Writing Skills (v2 — Archival Specimen Cabinet)

## Overview

**Creative North Star: "Tủ Phiếu Biên Tập & Sơn Mài Kỹ Thuật"**

On 24 November 2026 the user selected a dual-ground archival editorial direction to give the product a distinct personality beyond standard SaaS dark-mode templates. Structural navigation, rule drawers, and inspector columns sit on **deep archival lacquer forest** (`background` / `surface`), while the Vietnamese writing sheets, skill-guided specimens, and blind A/B comparison plates sit on **warm archival calico paper** (`paper`) with crisp carbon ink (`paper-ink`). Chrome brass (`accent`) anchors primary actions and structural index lines; vermilion (`vermilion` / `danger-paper`) marks active editorial proof points and deletions.

**Key Characteristics:**

- **Dual-ground contrast:** dark archival forest framing vs. high-legibility ivory paper specimen sheets.
- **Sharp editorial joinery:** 4px/6px crisp architectural corners, 1px hairline rules, flat elevation (no shadows).
- **Asymmetric first viewport on landing:** editorial headline + actions alongside the interactive comparison specimen inside the opening desktop viewport.
- **Native ergonomics & progressive enhancement:** `@view-transition` cross-document fades, CSS `:has()` state styling, container-query comparison reflow, 44px interaction targets, and reduced-motion safeguards.

## Colors

Canonical tokens live in `web/frontend/app/globals.css`. Contrast stays >= 4.5:1 across both dark cabinet planes and light paper sheets:

### Cabinet Planes (Dark Archival Lacquer Forest)

- **Deep lacquer canvas** (`background`): `#0b1614` page frame and sunken input beds inside dark drawers.
- **Cabinet surface** (`surface`) and **raised drawer** (`surface-raised`): `#11211e` and `#182e2a` for inspection columns, navigation states, and unguided baseline specimens.
- **Cabinet borders** (`border`, `control-border`): `#25403b` and `#486b64` hairline rules.
- **Ivory reading white** (`foreground`) and **sage slate** (`muted`): `#f2efe6` and `#a3b8b1`.

### Specimen Planes (Archival Calico Paper)

- **Specimen paper** (`paper`) and **paper tray** (`paper-subtle`): `#f3efe4` and `#e7e1d1` for `/check` drafting sheet, `/start` copyable prompt card, guided output comparison specimen, and neutral `/review` Output A & B sheets.
- **Carbon ink** (`paper-ink`), **charcoal sage** (`paper-muted`), **forest link ink** (`paper-accent`), **paper rules** (`paper-border`, `paper-control-border`): `#141c1a`, `#44544f`, `#184d3b`, `#c9bfaa`, and `#7d7563`.

### Editorial Accents & Status

- **Chrome brass** (`accent`, `accent-hover`, `accent-ink`): `#e8c55a`, `#f2d57c`, `#141a10`.
- **Proofreader vermilion & semantic alerts**: `#f06b54` / `#ffb4b8` on dark; `#a82419` (`danger-paper`) on ivory paper; `#f0c265` (`warning`).

**The Evidence Rule.** On `/examples` and `/`, dual-ground contrast distinguishes the baseline run from the skill-loaded run without claiming a quality score. On `/review`, both blind outputs (`a` and `b`) share the exact same archival ivory paper treatment so visual weight remains strictly unbiased.

## Typography

- **Display and Body Font:** self-hosted Be Vietnam Pro (400, 600, 700) with full Vietnamese diacritic legibility.
- **Technical Identifiers & Commands:** self-hosted JetBrains Mono (`13px`) restricted strictly to skill IDs, CLI install commands, pattern codes, line/column locations, and numeric counts.
- **Measures & Hierarchy:** display headline scales `clamp(42px, 5vw, 72px)` (`fontWeight: 700`, `-0.035em`); route headings use `38px`; workspace headings use `2rem`; reading copy stays within `73ch` at `1.85` line height; textarea editing uses `1.75` line height.

## Layout & Breakpoints

- Shared container max-width: `1320px` with `32px` desktop gutters (`18px` at and below `600px`).
- **Home Opening Stage (`.home-stage`):** 12-column asymmetric split (`minmax(0, 5fr)` editorial column + `minmax(0, 7fr)` live `ComparisonExplorer` specimen) above `1100px`, stacking cleanly into single column below `1100px`. `.comparison-explorer` uses `container-type: inline-size` so its internal 2-column outputs stack automatically whenever container width drops below `640px`.
- **Capabilities & Use Ledger:** `.home-capabilities` uses ruled rows; `.use-section` places the highlighted ivory web-workspace sheet (`7fr`) beside stacked dark cabinet drawers (`5fr`) for chatbot packs and CLI agent installation.
- **Workspace (`/check` & `/contribute`):** dual-ground workbench putting the ivory drafting `Editor` (`#f3efe4`) directly alongside the dark lacquer findings column (`#11211e`), with optional capability-gated `RewritePanel` below comparing original draft (dark surface) with proposed rewrite (ivory paper + inline `<del>`/`<ins>` diff).
- **Onboarding (`/start`):** sticky dark cabinet rail beside setup instructions and ivory tear-off prompt sheet.
- **Reading (`/examples`, `/guide`, `/about`):** dual-column editorial index + `73ch` prose layout.
- **Blind Review (`/review`):** archival cabinet frame with balanced dual ivory specimen sheets for Output A and Output B.

## Elevation, Motion & Controls

- Strictly flat architecture: zero box-shadows, 1px hairline borders only, crisp `4px`/`6px` corners.
- Progressive cross-document `@view-transition { navigation: auto; }` gated inside `@media (prefers-reduced-motion: no-preference)`.
- Controls keep >= 44px touch height, native `<details>`/`<select>`/`<input>` semantics, CSS `:has(:checked)` selection states, and visible `2px` focus outlines (`4px` offset).

Design references: [GoogleChrome/modern-web-guidance](https://github.com/googlechrome/modern-web-guidance), [Impeccable 4.8.0](https://github.com/pbakaus/impeccable/tree/c8891a9ae865d6ee311836ae5199bfce0fe115b1), [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/dd9a1b4cf9f67ca2e326f646d93e101b2778db30). See [PRODUCT.md](PRODUCT.md) and [.impeccable/surfaces/](.impeccable/surfaces/).
