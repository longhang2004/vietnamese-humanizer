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
  guided-surface: "#141e1b"
typography:
  display:
    fontFamily: "Be Vietnam Pro, Segoe UI, sans-serif"
    fontSize: "clamp(48px, 6.2vw, 88px)"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "Be Vietnam Pro, Segoe UI, sans-serif"
    fontSize: "40px"
    fontWeight: 600
    lineHeight: 1.25
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
  field: "8px"
  button: "9px"
  panel: "14px"
spacing:
  inline-gap: "12px"
  field-block: "11px"
  control-inline: "20px"
  panel-padding: "24px"
  desktop-gutter: "32px"
  mobile-gutter: "18px"
  reading-gap: "64px"
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

# Design System: Vietnamese Writing Skills

## Overview

**Creative North Star: "A dark workspace for Vietnamese writing"**

The user selected a dark interface aimed at technical users on 04 November 2026 and retained that identity for the layout refactor. Readable Vietnamese, actual output examples and a clear path into the editor remain the focus. Graphite surfaces and a pale lime accent establish the visual identity.

The shared system supports wide working regions and controlled reading measures. Rules, aligned rows and restrained tonal changes organize the content; native controls and direct labels keep the same interface usable for nontechnical readers. Surface-specific composition is recorded in the briefs under `.impeccable/surfaces/`.

**Key Characteristics:**

- Dark canvas, flat surfaces and visible borders.
- Vietnamese typography with commands in monospace.
- Direct labels and progressive disclosure.
- Native controls, visible focus and generous touch targets.

## Colors

The frontmatter records the canonical colors from `web/frontend/app/globals.css`. The palette combines graphite layers with pale lime task emphasis.

### Primary

- **Pale lime** (`accent`): primary actions, focused controls, selected checks and links; the lighter hover variant provides state feedback.
- **Lime ink** (`accent-ink`): dark lettering on lime fills and selection highlights.

### Neutral

- **Graphite canvas** (`background`): the page and text-entry background.
- **Graphite surface** (`surface`) and **raised graphite** (`surface-raised`): working regions and hover or active surfaces.
- **Quiet border** (`border`) and **control border** (`control-border`): content separators and clearly identifiable interactive boundaries.
- **Reading white** (`foreground`) and **muted slate** (`muted`): primary text and supporting copy.
- **Guided graphite** (`guided-surface`): the subtle green-tinted background of the skill-loaded comparison output. It identifies the condition without declaring a winner.

Warning and danger colors accompany explicit text labels; color does not carry the finding type alone.

**The Evidence Rule.** Comparison emphasis distinguishes the two recorded conditions; it must not imply a measured quality advantage.

## Typography

**Display and Body Font:** self-hosted Be Vietnam Pro, with Segoe UI and sans-serif fallbacks. The shipped weights are 400, 600 and 700, including Vietnamese glyphs; licenses sit beside the font files.
**Label/Mono Font:** Be Vietnam Pro for labels; self-hosted JetBrains Mono for commands, identifiers and measurements.

### Hierarchy

- **Display:** the landing heading uses the frontmatter clamp, with a compact-tablet override (64px at and below 960px) and mobile override (48px at and below 600px).
- **Headline:** reading and onboarding route headings use the headline token, reducing to 32px at and below 600px. Checker and contribution headings use the workspace-heading token, reducing to 1.75rem at that breakpoint.
- **Section heading:** landing sections scale between 28px and 36px; reading sections use 26px, reducing to 23px on mobile. Workspace region titles use 1.25rem, reducing to 1.125rem on mobile.
- **Body:** the body token establishes the base rhythm. Reading copy and comparison outputs use the reading token; editor text uses a 1.75 line height. Reading articles are limited to 73ch.
- **Label:** the label token defines shared action text. Supporting labels and metadata commonly use 14px; commands remain 13px and wrap within their control.

**The Vietnamese Reading Rule.** Preserve Vietnamese glyph coverage, comfortable line height and the original line breaks of published output examples.

## Layout

The shared container is at most 1280px wide. Main content, header and footer use the desktop-gutter token on each side, switching to the mobile-gutter token at and below 600px. Grid children and command controls can shrink; long commands wrap instead of widening the page.

The landing page uses a two-column heading and summary, then a full-width real comparison, followed by rule-separated capability, use and FAQ rows. The hero has 64px top and 52px bottom padding on desktop; later editorial sections use 56px top and 64px bottom padding. At and below 960px, the hero, capability and FAQ regions become one column. At and below 600px, the hero uses 36px/32px padding and later sections use 36px/40px.

Checker source and findings occupy one bordered workbench with equal columns and a shared divider. The optional rewrite region follows beneath that pair. Contribution forms pair original and proposed text, then supporting fields and consent. Working regions use the panel-padding token, reducing to 20px on mobile. Feedback stays beside its action or in the result region.

Onboarding uses a sticky selection rail (304px) beside setup and prompt content, with a 48px gap. Reading routes use a sticky index (220px) beside a 73ch article, with the reading-gap token. These are module layouts with their own responsive behavior.

| Source and scope | Breakpoint | Implemented change |
| --- | --- | --- |
| Shared styles | 1100px | Compact navigation spacing, landing gaps and capability-row detail columns. |
| Shared navigation and landing | 960px | Navigation becomes a disclosure; hero, capability and FAQ regions stack; use rows become two columns. |
| Shared legacy reading primitives | 960px | The shared prose layout becomes one column; the route reading module below defines its current index behavior. |
| Comparison explorer | 780px | Toolbar reflows, paired outputs stack, and provenance becomes vertical. |
| Shared styles | 600px | Mobile gutters, 48px hero, full-width hero actions, single-column use rows and compact footer. |
| Workspace module | 1100px | Check choices use one column inside the side-by-side workbench; rewrite options retain two columns. |
| Workspace module | 850px | Source and findings stack; the check-choice grid returns to two columns in the wider stacked source region. |
| Workspace module | 600px | Text pairs, checks and supplemental fields stack; padding reduces and applicable submit actions fill the width. |
| Onboarding module | 1100px | Selection rail narrows to 280px with a 32px gap; heading and supporting link stack. |
| Onboarding module | 850px | Rail becomes a static two-column choice region above setup. |
| Onboarding module | 600px | Choices and support stack; task selection uses 16px text. |
| Reading module | 1100px | Header stacks; index narrows to 192px and gap to 40px. |
| Reading module | 850px | Index becomes a compact wrapping list above the article; next actions stack. |
| Reading module | 600px | Header and section spacing compact; recovery heading reduces to 32px. |

## Elevation & Depth

The interface is flat: borders and tonal layers provide separation, with no box-shadow vocabulary. The sticky header is opaque. Shared controls use 160ms ease transitions for text, background and border colors. Reduced-motion preferences disable animations and transitions; the current landing page has no entrance animation.

**The Flat Workbench Rule.** Use shared boundaries and tonal changes to organize working regions; avoid stacking decorative cards inside them.

## Shapes

Fields, filter chips and navigation states use the field radius; buttons use the button radius, and enclosing workbenches, comparison and onboarding panels use the panel radius. Borders are 1px. Text highlights use a small 2px radius; the system does not apply large pill shapes to controls.

Actions and disclosures provide at least 44px touch targets; primary and secondary buttons are at least 46px high. Prose links remain text links.

## Components

### Buttons

Primary actions have a pale lime fill and dark text, with a lighter hover fill. Secondary actions have a control border and transparent fill, changing to raised graphite on hover. Icon buttons are 44px square. All share visible focus (2px lime outline, 4px offset). Disabled buttons use 0.5 opacity and a disabled cursor.

### Inputs / Fields

Shared fields have a graphite canvas, control border, field radius and 16px type. The checker textarea uses 16px internal padding and a 1.75 line height. Placeholders remain readable; carets and native checkbox/radio accents use lime. Onboarding uses the same field primitive, with its task selector adapting to the compact rail.

### Navigation

The sticky header uses opaque graphite. Hover and active links use foreground text on raised graphite. At the navigation breakpoint the menu is a disclosure; Escape closes it and returns focus to its toggle. GitHub stars are loaded from the public API and omitted when unavailable.

### Chips / Findings

Finding filters are compact rectangular buttons with a 44px minimum height; selected filters use a lime border and text on the canvas background. Findings are separated by rules, with type labels, counts, location metadata, excerpts and optional native explanations.

### Cards / Containers

The panel primitive is a single flat, bordered enclosing surface. The comparison explorer uses it around a toolbar, paired outputs, prompt disclosure and provenance. A topic change updates both outputs and prompt together, and announces the topic. Heading levels follow the embedding page.

### Editorial Workbench

The checker keeps source and findings in one continuous working region, followed by capability-gated rewriting. All four checks start enabled and live in a native disclosure above the submit action. Text edits and changed checks invalidate old results and pending responses. Contributions keep original and proposed text together, with explicit consent; optional features remain gated by backend capabilities.

### Selection and Reading

Onboarding separates platform/task choice from setup and the copyable request. The reading index links to sections within the controlled article measure. Install commands wrap in monospace and place their copy button and announced confirmation beside the command. Copy and submission feedback remain adjacent to the relevant action.

## Do's and Don'ts

### Do:

- **Do** keep the user's text and current task prominent.
- **Do** keep outputs verbatim and link their prompts and skill snapshot.
- **Do** use existing semantic colors, self-hosted fonts and native controls.
- **Do** preserve visible focus, reduced-motion behavior and minimum action targets.
- **Do** use the documented breakpoint for the affected module rather than assuming one global stacking threshold.
- **Do** review desktop, tablet and 375px mobile layouts, including loading, error and empty states.

### Don't:

- **Don't** invent scores, stars or claims that a skill always improves output.
- **Don't** put persistent supporting notices above the main task.
- **Don't** add decorative metrics, gradient lettering or translucent panels to this design.
- **Don't** promote surface-specific composition into a rule for every page.

Design references: [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/dd9a1b4cf9f67ca2e326f646d93e101b2778db30), [Impeccable 4.8.0](https://github.com/pbakaus/impeccable/tree/c8891a9ae865d6ee311836ae5199bfce0fe115b1). See [PRODUCT.md](PRODUCT.md), the [surface briefs](.impeccable/surfaces/) and the [frontend README](web/frontend/README.md).
