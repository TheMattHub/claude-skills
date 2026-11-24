# Multilingual UI Rollout

## Goal

Add multi-language support to an app so all visible UI text can switch by language without forking templates.

## Use when

- the product serves users in multiple countries
- the UI is mostly server-rendered or template-driven, or has a shared shell across pages
- you want one codebase, not one template set per language

## Core pattern

1. Add a language selector in the shared layout.
2. Store the chosen language in session or user preferences.
3. Centralize translations in a single translation layer.
4. Make templates render via a translation helper like `t("...")`.
5. Sweep every page and replace hardcoded visible strings.
6. Add regression tests for language switching and at least one translated page.

## Implementation checklist

- supported language registry
- current language loader
- translation helper for both templates and server-side code
- global shell/header translation coverage
- page-by-page audit for leftover untranslated text
- translated labels for feature-specific nouns and statuses
- tests for selector behavior and key page content

## Good design choices

- Keep one canonical source string per key.
- Use localized terms, not literal translations, for domain concepts.
- Translate reusable messages at the source, not only in templates.
- Prefer a compact language switcher in the global header.
- Make the selector accessible on mobile, not just desktop.

## Common pitfalls

- Split sentences across template lines so keys do not match.
- Leave dynamic labels hardcoded in server-side code.
- Translate most pages but miss secondary admin pages or empty states.
- Forget mobile presentation of the language selector.
- Treat the rollout as "done" before sweeping admin and empty-state surfaces.
