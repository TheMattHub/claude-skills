---
name: multilingual-ui-rollout
description: Add language switching, a centralized translation helper, and page-by-page localization coverage to a web app. Use this whenever the user mentions multilingual support, i18n, localization, language selectors, translation audits, localized labels, or wants the app available in more than one language — even if they just say "translate the UI." Also triggers when sweeping hardcoded strings, adding a language switcher, or fixing partial translation coverage on admin pages and empty states.
---

# Multilingual UI Rollout

## Overview

Implement multilingual support without splitting the app into separate template sets or duplicating views per language.

## Workflow

1. **Audit the shared layout, shell, and navigation** for visible text — this is where partial translations hurt most.
2. **Add a centralized translation helper** for both templates and server-side messages (e.g., `t("key")` in templates, equivalent function in app code).
3. **Add a supported-language registry** and a language loader that respects the user's choice.
4. **Store the chosen language** in session or user preferences so it survives navigation.
5. **Sweep pages and replace hardcoded visible strings** with translation keys — one canonical English source string per key.
6. **Verify dynamic labels, statuses, and empty states** are translated at the source, not only in their final template.
7. **Add at least one regression test** for language switching and one for a translated page's content.

## Implementation checklist

- supported language registry
- current language loader
- translation helper for both templates and server-side code
- global shell/header translation coverage
- page-by-page audit for leftover untranslated text
- translated labels for feature-specific nouns and statuses
- tests for selector behavior and at least one key page's translated content
- a coverage test: scan the source for every `t('literal')` (and `data-i18n` labels) and fail on any missing from the target dictionary; dynamic values go through placeholders (`t('{n} of {total}', {n, total})`) so every key stays a literal the test can read

## Design notes

- Prefer **localized product terms** over literal translations when the domain has idiomatic equivalents.
- Keep the selector compact in the global header — language switching should never feel like a buried setting.
- Treat untranslated admin pages and empty states as **first-class cleanup work**, not optional polish.
- Use one canonical English source string per key — don't split a sentence across multiple keys, because translations rarely preserve the original word order.

## Common pitfalls

- Splitting sentences across template lines so keys do not match.
- Leaving dynamic labels hardcoded in server-side code.
- Translating most pages but missing secondary admin pages or empty states.
- Forgetting the mobile presentation of the language selector.
- Literal translation of domain terms that have a different idiomatic word in the target language.

## References

Read `references/playbook.md` for the full rollout checklist and rollout guidance.
