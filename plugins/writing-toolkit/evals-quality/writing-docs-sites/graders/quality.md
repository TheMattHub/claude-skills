---
type: llm
---

Judge the final answer against these observable criteria.

1. The landing page change includes a short runnable code example shown together with its output, and an install line, near the top.
2. The pages are regrouped into a small number of named kinds by purpose (for example tutorials, how-to guides, reference, background), not left as one flat list.
3. A ticket makes sure the code and numbers shown on the site are produced or tested automatically (run in CI, generated from a seeded run) so that they cannot drift from the code.
4. The landing page is split by reader type (for example "I am a new user / analyst / integrator") routing each to a first page.
5. The list includes at least one item about machine-readable access for AI tools (llms.txt or a Markdown copy of pages) or about trust pages (release notes, stability policy, how to cite).

PASS if at least 4 of the 5 criteria hold. FAIL otherwise. Name the criteria that failed.
