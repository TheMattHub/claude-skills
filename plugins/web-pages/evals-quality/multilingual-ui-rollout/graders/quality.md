---
type: llm
---

Judge the final answer against these observable criteria.

1. It proposes one central translation helper or message catalogue that every page uses, not translations scattered per page.
2. It includes a language switcher whose choice is remembered (cookie, profile or local storage) and a default or fallback language.
3. It plans page-by-page coverage, explicitly including admin pages and empty states or error messages.
4. It gives a way to check completeness, such as a script or test that finds hard-coded strings or missing keys.
5. It orders the work: the helper and switcher first, then pages in batches.

PASS if at least 4 of the 5 criteria hold. FAIL otherwise. Name the criteria that failed.
