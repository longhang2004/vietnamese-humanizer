---
name: Vietnamese Writing Skills
description: A dark workspace for editing Vietnamese with context.
colors:
  background: "#0b0f14"
  surface: "#11171f"
  surface-raised: "#18212b"
  border: "#2b3846"
  control-border: "#566678"
  foreground: "#eef2f5"
  muted: "#aab6c4"
  accent: "#c4ef91"
  accent-hover: "#d6f6b2"
  accent-ink: "#14220b"
  danger: "#ffb4b8"
  warning: "#f3cc83"
typography:
  body:
    fontFamily: "Be Vietnam Pro, Segoe UI, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.7
  label:
    fontFamily: "Be Vietnam Pro, Segoe UI, sans-serif"
    fontSize: "14px"
    fontWeight: 600
    lineHeight: 1.4
  command:
    fontFamily: "JetBrains Mono, monospace"
    fontSize: "11px"
rounded:
  field: "8px"
  button: "9px"
  panel: "14px"
spacing:
  inline-gap: "12px"
  panel-padding: "24px"
  section: "88px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.accent-ink}"
    rounded: "{rounded.button}"
    padding: "11px 20px"
  button-primary-hover:
    backgroundColor: "{colors.accent-hover}"
  button-secondary:
    textColor: "{colors.foreground}"
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

# Design System: Vietnamese Writing Skills

## Overview

The user selected a dark interface aimed at technical users on 04 November 2026. Readable Vietnamese, actual output examples and a clear path into the editor are the focus. Graphite surfaces and a pale lime accent establish the visual identity.

The landing page introduces the project through a real editing example. The checker uses a wide working surface; guides use a narrow reading column. They share navigation, typography and controls.

Key characteristics:

- Dark canvas, flat surfaces and visible borders.
- Vietnamese typography with commands in monospace.
- Direct labels and progressive disclosure.
- Native controls, visible focus and generous touch targets.

## Colors

The frontmatter records the colors in `web/frontend/app/globals.css`. Lime marks primary actions, focus and selection. Graphite layers separate the page, panels and controls. Errors and warnings also have explicit text labels.

Paired AI examples use neutral headings. A green tint identifies the skill-loaded output without declaring a winner.

## Typography

Be Vietnam Pro is self-hosted at weights 400, 600 and 700, including Vietnamese glyphs. JetBrains Mono is reserved for commands, identifiers and measurements. Licenses live beside the font files.

Body text is 16px with a 1.7 line height. The editor uses 16px and 1.75. The hero heading scales from 48px to 76px; route headings use 40px on desktop and 32px on mobile. Outputs retain their original line breaks.

## Layout

The main container is at most 1200px, with 24px side gutters on desktop and 18px at small widths. Sections use 88px vertical spacing, reducing to 64px below 850px and 48px below 600px.

The hero becomes one column below 850px. Paired outputs stack below 600px. Editor and results sit side by side on large screens and stack on mobile. Guides use a 220px table of contents and a reading column of at most 73ch.

Shared stylesheet breakpoints are 1100px, 850px and 600px; checker utilities follow the existing Tailwind configuration. Grid children containing commands must shrink within their columns. Commands scroll inside their own control.

## Elevation & Depth

Borders and tonal layers provide separation. The sticky header is opaque. Hero copy has one 600ms entrance animation; controls use 160ms color transitions. Reduced-motion preferences disable animation and transitions.

## Shapes

Fields use an 8px radius, buttons 9px and large panels 14px. Borders are 1px. Controls have touch targets of at least 44px. Prose links remain text links.

## Components

- **Primary button:** lime fill, dark text, lighter hover fill.
- **Secondary button:** control border, transparent fill, raised hover surface.
- **Field:** dark background, control border, readable placeholder. The editor is a larger 16px variant.
- **Navigation:** active and hover states; disclosure menu below 850px. GitHub stars come from the public API and are omitted when unavailable.
- **Comparison explorer:** native selector, previous/next buttons, paired outputs and prompt disclosure. A topic change updates both outputs and the prompt together.
- **Findings:** type labels, counts, filters and inline explanations. Editing invalidates old results and pending responses.
- **Install command:** internal horizontal scroll, copy button and announced confirmation.

## Do's and Don'ts

- Do keep the user's text and current task prominent.
- Do keep outputs verbatim and link their prompts and skill snapshot.
- Do use existing semantic colors and self-hosted fonts.
- Do review desktop and 375px mobile layouts, including loading, error and empty states.
- Don't invent scores, stars or claims that a skill always improves output.
- Don't put persistent supporting notices above the main task.
- Don't add decorative metrics, gradient lettering or translucent panels to this design.

Design references: [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/dd9a1b4cf9f67ca2e326f646d93e101b2778db30), [Impeccable](https://github.com/pbakaus/impeccable/tree/695cea5c6d1cbd420fc331375c7ef126a774e5f7). See [PRODUCT.md](PRODUCT.md) and [the frontend README](web/frontend/README.md).
