---
name: choosing-ui-colours
description: "Use when choosing or reviewing the colours of an interface - a palette, theme, light/dark mode, brand or accent colour, status colours (running, idle, down, warning), chart or series colours, scenario A vs B colours - or when a UI \"needs more depth\", \"pick better colours\", \"make a dark mode\", \"more blue\", or mock-ups are being drawn for a visual direction. Uses the ui-ux-pro-max and dataviz skills when installed and adds the rules they miss. Not for layout-only or copy changes."
---

# Choosing UI colours

## Overview

Colour is picked by job, then validated by script, never by eye. Mock-ups that "look fine" hid a
blue/violet pair that red-blind readers see as one colour (Delta E 0.9). Load the helper skills below if installed.

## Workflow

1. **Load the helpers, if installed.** `ui-ux-pro-max` (run `--design-system` with `--density` for dashboards; use its
   UX rules, not its palettes: they are generic Tailwind slate) and `dataviz` (its validator is the gate).
   Neither installed: follow the rules in this skill and check every colour pair with any WCAG contrast
   calculator (step 8), plus a colour-blindness simulator for series colours (step 4).
2. **Name the roles before any hex.** Surfaces (bg, panel, raised, line), text (text, muted, dim),
   one accent for everything clickable, series colours (identity), status colours (state), deltas.
3. **60-30-10.** About 60% background, 30% panels and cards, 10% accent. Two to four core colours plus
   neutrals; more feels chaotic. Every colour has one role; drop any colour without one.
4. **Series colours: validate.** With `dataviz`:
   `node <dataviz>/scripts/validate_palette.js "<hex,...>" --mode dark --surface <panel>` and again
   `--mode light`; add `--pairs all` when any two series can sit side by side (scenarios, scatter).
   All checks must PASS. Without it, simulate protanopia/deuteranopia and confirm series stay distinguishable. Blue + orange (+ teal third) is a safe start; blue + violet and red + green fail.
5. **Status colours: quiet when normal, loud when not** (industrial HMI practice, ISA-101 style).
   Normal running is a calm low-glow colour; only abnormal states (down, blocked, alarm) get bright
   colour or glow. Status always carries a word or icon ("DOWN", a warning sign), never colour alone,
   and never reuses a series hue.
6. **Deltas:** arrow + word ("better", "worse", "no clear change") beside the colour.
7. **Dark mode is designed, not inverted.** No pure black: a dark grey or blue-tinted base
   (e.g. slate `#151b26` / panel `#1c2331`), off-white text, depth by lighter surfaces per level
   (shadows barely read on dark). Re-validate every colour on the dark surface; buttons may need a
   different step so white text keeps 4.5:1.
7b. **Theme switch:** two token sets; follow `prefers-color-scheme`, with a stored override applied by a
   small head script before first paint (no flash; storage in try/catch). A host app's theme may give fonts
   and fills but never overrides a validated palette's surfaces or accent.
8. **Contrast:** body text 4.5:1, large text and marks 3:1 (`contrast()` exported by the dataviz
   validator, or any WCAG contrast calculator). Muted text is where palettes fail; check it on both bg and panel. Test contrast and a visible focus ring
   in every theme, not only the default one.
9. **Show options as rendered pages** (HTML mock-ups, pushed to Figma with `html_to_figma` when the user
   wants Figma), including a strip of candidate tones on the same elements, and recommend one.

## Example console palette (validated, 2026-10-22)

`references/console-palette.md`: an example slate-blue/light console palette, with
the validator results. Reuse it as a starting point for data-dense consoles.

## Common mistakes

| Mistake | Fix |
|---|---|
| Hand-picked scenario colours | Run the validator; blue/violet collapses under protanopia |
| Red/green for running/down | Quiet teal for running, bright red + word for down |
| Every state glowing | Glow only the abnormal ones |
| Pure black dark mode | Blue-tinted dark grey, lighter surfaces for elevation |
| Accent colour also used for status | One accent for interaction only |
| Palette from the design-system DB as is | Treat it as a hint; the roles and checks decide |
