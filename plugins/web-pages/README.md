# web-pages

Three skills for HTML pages and web apps that other people will open.

- `building-shareable-web-pages`: safe, stable, phone-friendly pages (CSP, escaping, local-server protection, layout shift, light/dark, browser tests). Example: "Build a live monitor page for this simulation and make sure it is safe to share."
- `choosing-ui-colours`: picks and checks palettes, status colours and dark mode by role and contrast. Example: "Pick status colours and a dark mode for this control panel."
- `multilingual-ui-rollout`: language switching, a central translation helper and page-by-page localisation coverage for a web app. Example: "Make the admin pages available in Italian and English."

## Requirements

None. Each skill works on its own.

## Optional companions

If installed, the skills also use `dataviz` (charts), `ui-ux-pro-max` (UX rules, palettes) and `frontend-design` (visual direction). Without them, `choosing-ui-colours` falls back to its own rules plus its own `contrast.py`.

## What it reads, writes and runs

- Instructions only, plus one script, `skills/choosing-ui-colours/scripts/contrast.py`. It computes WCAG contrast ratios from the hex colours you pass on the command line and prints them; it reads no files, makes no network calls and writes nothing.
- The skills themselves do not run anything else. Claude may write or edit HTML in your project when you ask for a page, and may run a local browser or test you request; those actions follow your normal Claude Code permissions.
- Optional companions (`dataviz`, `ui-ux-pro-max`, `frontend-design`) are separate plugins with their own behaviour.

## Install

```text
/plugin install web-pages --marketplace TheMattHub/claude-skills
```
