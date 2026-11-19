---
name: writing-docs-sites
description: "Use when a project's documentation SITE is being planned, audited, restructured or compared with others - \"improve our docs\", \"docs like numpy/pandas\", \"landing page of the docs\", \"tutorials vs reference\", \"make the docs readable for AI agents\", \"llms.txt\", \"is our documentation good\". Covers site structure, landing page, learning path, reference, trust signals and AI readers; not README-only edits or single docstrings."
---

# Writing docs sites

## Overview

A docs site is judged in its first five minutes: can each kind of reader install, run something real, see
why the tool is different, and know where to go next. Leaders (NumPy, pandas, SciPy) win on routing and
trust; small projects lose on a dense landing page and a flat pile of pages. Every claim on the site must be
true now, so code and numbers come from runs, never from pasting.

## Audit first (recipe)

1. **Readers.** Name them (e.g. library user, analyst, integrator, AI agent) and write, for the main one,
   what they must have done after five minutes. That sentence is the success test of the landing page.
2. **Ours, from the files.** Nav tree, page count, generated vs hand-written, Diataxis type per page,
   which snippets run in tests, trust pages, AI files. Rendered pages are claims; the files are evidence.
3. **Theirs, live.** Two or three leaders in the same language plus two in the same domain. Tag every
   claim: verified (fetched, date), snip, [m], n/f. Use the analysing-competitors skill for the format.
4. **Copy / improve / avoid**, then a short written design before touching pages.

## Checklist

| Area | The bar |
|---|---|
| Landing page | pitch line, install line, a ten-line runnable example WITH its output, "why it is different" in three sentences, then "I am a..." cards per reader; one screen before the cards |
| Learning path | one example grown in steps (salabim's bank model), each step runnable alone; task-phrased titles (pandas "How do I...") |
| Structure | Diataxis, named plainly: Tutorials / How-to / Reference / Background; one job per page |
| Reference | generated from the code (numpydoc: Parameters, Returns, Examples, See Also), examples doctested; huge pages split per group |
| Trust | release notes in the nav, stability/deprecation policy, Citing page (CITATION.cff), validation against known answers, benchmarks with date and hardware |
| Comparisons | "Coming from X" pages for the tools readers already know, both sides runnable |
| AI readers | `llms.txt`, `llms-full.txt`, a Markdown copy per page (`rel="alternate" type="text/markdown"`), published schemas; no login walls or bot blocks |
| Sentences | each page readable alone: every sentence has its subject, verb and object, terms glossed at first use, no reference to internal material (also apply `writing-self-contained-text`, same plugin) |
| Truth | every snippet executed in CI; every printed number generated from a seeded run; counts generated or tested; no internal plan codes; the site follows the reader's system colour scheme (no flash between a dark browser and a light page) |

## Red flags

| Thought | Reality |
|---|---|
| "Paste the output, it is what it printed" | It drifts silently. Generate it from a seeded run and test the page against the generator. |
| "Add a version switcher" | Before 1.0 it adds cost and hides the version from crawlers; state the version and date in text. |
| "More pages = better docs" | A flat pile of 40 tutorials routes nobody. Fewer, typed pages with a path. |
| "The rendered site looks fine" | Audit the files: what is generated, what runs, what is guarded. |
| "Our README is the landing page" | The site's first screen is; mirror it, do not diverge. |

## Best practices with sources

`references/best-practices.md`: who does what (NumPy, pandas, SciPy, SimPy, salabim, Mesa,
Ciw, Anthropic/Pydantic/uv for llms.txt), evidence-tagged, surveyed October 2026. Re-check before relying on a
specific claim older than six months.
