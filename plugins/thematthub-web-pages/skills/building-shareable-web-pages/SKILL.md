---
name: building-shareable-web-pages
description: "Use when building or reviewing an HTML page that is shared, emailed, opened from disk or served on localhost - a run player or replay, a model viewer, a live monitor, a control room or control panel, a client dashboard or console, a report page, an MCP App page - including its CSP and escaping, sandboxed frames, local-server protection, phone-width layout, layout shift, light/dark theme, KPI and verdict display, clutter, and browser tests. Also when a page \"looks flat\", \"jumps around\", \"is cluttered\", blanks out, or a local page's server must be locked down. Not for docs sites (writing-docs-sites), colour choice itself (choosing-ui-colours) or desktop Qt UI."
---

# Building shareable web pages

## Overview

A shared page is read by people you never meet, in browsers you never test, next to websites that attack
localhost. It fails in three ways: it leaks or runs what it should not, it breaks or jumps on a real screen,
or it shows numbers nobody can act on. Every rule below came from a bug or a review finding that happened,
most of them more than once.

Load alongside: `choosing-ui-colours` (palette, status colours, dark mode; same plugin). If installed, also
`dataviz` (charts), `ui-ux-pro-max` (UX rules, layout shift, touch sizes) and `frontend-design` (visual direction).

## Before building

1. Spec with Done-when, Anti-goals and a **Review Focus** list naming the inputs that break pages: no data /
   no optional fields, a hostile name, phone width (360 px), dark mode, storage that throws, a long label,
   a failed extra step. Each gets a test in the task that owns it.
2. Show the look as rendered mock-ups (several variants, a tone strip) and let the user pick; style waits for
   them.
3. Plan a feedback round after the first build: users react to the built page, not the spec (in one project the console
   look got "flat", then "jumps around", "cluttered", "boxes overlap" only once it was real).

## Security of a self-contained page (`references/csp-and-escaping.md`)

- **Template + one data block.** The page is a constant template; everything that varies is one JSON block
  escaped for `< > & /`. Model text reaches the DOM only via `textContent` or canvas `fillText`.
- **CSP:** `default-src 'none'`, a sha256 hash per inline script and style, `base-uri 'none'`,
  `form-action 'none'`, `img-src data:` only if needed. Never `'unsafe-inline'`. A test asserts every inline
  script/style hash is in the policy, and the script holds no `innerHTML`, `eval`, `document.write`,
  `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`.
- **Names are hostile.** A block named `constructor` or `__proto__` blanked a page: every lookup by name uses
  an own-property check (`Object.prototype.hasOwnProperty.call`) or a `Map`.
- **Embedded author content** goes in `<iframe sandbox="allow-scripts" srcdoc>`; the parent policy lists the
  frame's hashes.
- **"No network" is measured,** with a canary server and the browser driver attached to every worker, not
  claimed from the CSP (browsers still pre-connect on navigation; WebRTC ignores CSP).
- **Secrets never reach the page, the folder, logs or an assistant's tool results.** A token was written
  beside the page, printed in it and pasted into chat: three leaks in two days.
- **Local servers** (anything a page talks to on 127.0.0.1): `references/local-server-checklist.md`.

## Layout

- **Phone and wide screen in a real browser:** assert `scrollWidth <= innerWidth` at 360 and 1920 px and
  the grid's column count. A headless screenshot window cannot shrink to 360 px: measure, do not eyeball.
- **No layout shift on live values:** tabular digits (`font-variant-numeric: tabular-nums`), fixed slots
  sized in `ch` for the longest value (clocks "1008 / 2400"), reserved heights for status and answer
  lines, a selected tab that does not change width (no bold-only active state). Test: element boxes do not
  move across play, seek and a status change.
- **Never draw one item over another.** Labels get a width cap from the real spacing and an ellipsis (not
  squeezed glyphs); dependent items (a buffer of a station) attach as compact shapes on the link, shrinking
  before overlapping. Render every bundled example and look.
- **A refresh must not destroy state:** a poll that reloads wiped an inserted picture; bump the change signal
  only when data changed, keep open panels and scroll across reloads.
- A hidden element still takes a grid row: place grid children explicitly. An embedded frame needs its own
  height rule when its content stacks on a phone.
- One screen first: fold secondary panels; open a section only when it has something to say (a failure).

## What a dashboard shows

- **Labels, not internals:** the author's label and unit, never `system/Avg Queue Length` or `station_1/Mfg
  Machine` (full name on hover).
- **The question and a plain answer** on top, computed by one function from the numbers: "Yes, very likely"
  only when the whole interval clears the target, "No" when wholly on the wrong side, else "Not clear yet";
  a run repeats until clear, capped; within a practical-equivalence band the answer is "No change you would
  notice". A verdict never comes from colour.
- **Intervals, targets, words:** each KPI as an interval bar (yours vs baseline), the target as a line, the
  delta with an arrow and a word ("better", "worse", "no clear change").
- **Where it hurts:** one callout naming the cause (the bottleneck and why), only when there is one; it may
  not name a passive container (a buffer) instead of the process behind it.
- **Can I trust this?** The checks passed, warm-up removed, replications and precision; state what a
  deliverable is a version of ("made for v002"); show limits in the page (unsupported browsers, data date)
  instead of a blank screen.
- **Live data is labelled:** stale judged by the viewer's own clock with the age shown, approximations
  marked, a missing forecast with its reason; lead a recommendation with the action, fold the rest.
- **Counts are never typed** into pages (tool numbers, schema versions): read them from the source of truth
  and test it.
- **Clutter pass:** one idea per line; nothing that repeats what the layout says; explanations into a tooltip
  or the trust card; secondary tables folded.
- Failures are visible where the user looks ("(E_CODE)" in the panel), never only a spinner.

## Interaction

- Browser storage is a convenience: every read and write in try/catch, a test where it throws, stored values
  read back as data (known keys, primitive values, a cap).
- Theme: two token sets, `prefers-color-scheme` plus a stored override applied by a pinned head script
  before paint (no flash).
- Long actions: an estimate before (counting every extra step), a Cancel that kills the worker, a status line
  per stage, and a failed extra step (recording, picture) never discards a finished result.
- Controls state what changed: "N changed", "Reset to defaults" (neutral wording), defaults marked.
- A playback page stops advancing at its end; two players share one clock.

## Testing (`references/browser-testing.md`)

Three layers per page script: the pure half under `node` with a stub DOM, against the same script constant
the file embeds; the written file in headless Chrome/Edge over the DevTools protocol (no package); the
hostile-input version of each. Then drive it yourself in both themes and at 360 px, and open it in the
user's real browser before calling it done.

## Common mistakes

| Mistake | Fix |
|---|---|
| `'unsafe-inline'` "for now" | Hash every inline style and script; test the hashes |
| Model text via `innerHTML` | `textContent` / `fillText`; static test forbids `innerHTML` |
| "Works on my monitor" | 360 and 1920 px, both themes, measured in a real browser |
| Numbers that change width | Tabular digits and fixed slots |
| Engine names on screen | Author labels and units |
| Answer by colour | One function, words, interval vs target |
| Random debugging ports for parallel browsers | `--remote-debugging-port=0` and read `DevToolsActivePort` |
| Trusting task agents' "no bugs found" | A whole-branch review and a real-browser drive find them |
