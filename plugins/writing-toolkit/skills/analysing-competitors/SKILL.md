---
name: analysing-competitors
description: Use when competitors, incumbents or alternative tools should inform a roadmap, a product or feature decision, a parity check, a bid or positioning, including when the user asks how to find out or compare what other products do - "competitor analysis", "market scan", "what do X and Y offer", "how do others handle this", "parity with".
---

# Analysing competitors

## Overview

A competitor analysis is worth what its two comparisons are worth: theirs against ours as checked in our code, and today's against the last analysis. Every claim says how it was known.

## Pick the scope first

| Scope | Example | Depth |
|---|---|---|
| Landscape | next roadmap, positioning | parallel passes, full deliverable, archived report |
| Domain | a new vertical, module or library | two passes, short report or a spec section |
| Feature | "add a debug mode (X has one)" | a short section inside the feature's spec (recipe below) |

## The three passes

1. **Our side, from the code.** Inventory what exists from source, tests and what actually runs. Docs, READMEs and roadmaps are claims to check, not evidence; note where they disagree with the code.
2. **Their side, from live sources.** Group by segment, not one agent per product: direct incumbents; open-source and newcomers; adjacent tools and substitutes users pick instead (spreadsheets, consultancies, in-house scripts, a neighbouring product category). At landscape scope run the passes as parallel read-only agents that share one output template; the coordinator merges their outputs into the matrix.
3. **The previous analysis.** Search the repo's history, plans and decisions for it, and diff against it. Its claims carry over as [m] until re-fetched.

## Evidence legend (on every claim)

- **verified**: page fetched, with the date
- **snip**: search-result summary only, page not fetched
- **[m]**: from memory, unverified
- **n/f**: looked for, not found

Prices count only from the vendor's own page; aggregator and reseller prices contradict each other, so mark them snip at best. A page behind a login or paywall is n/f with the reason. A snip or [m] claim that would drive a decision goes to Open checks, with how to settle it (a trial, a screenshot from the user, a sales question).

## Deliverable

1. **Summary**: findings and the decisions they call for.
2. **Scope**: date, products, sources, legend.
3. **Since last time**: closed, still open, new.
4. **Matrix**: us and each product, Y / P (partial) / N / ?.
5. **Copy, improve, avoid**: what to adopt, what to do better, what to refuse. Refusals that should outlast this analysis become standing decisions in the project's decision log.
6. **White space**: needs nobody covers well, and our edges.
7. **Open checks**: unverified claims that matter, and how to settle them.

**Feature scope** replaces all of the above with one section in the feature's spec, "How others do it": one or two tagged lines per product, our current state from the code, then copy / improve / avoid in a line each. No matrix and no archived report.

## Handing off

- **Inside a design or planning discussion:** sections 5 and 6 are the candidate options; ranking and choosing belong to that discussion.
- **Standalone:** the report is the result.
- **Storage:** save the full report dated in the project's archive or history folder (follow its conventions) and link it from the plan; the plan carries the conclusions, not the research.

## Common mistakes

| Mistake | Effect |
|---|---|
| Our docs used as our inventory | parity claims we cannot back |
| Only direct competitors | miss what users actually use instead |
| No "avoid" list | drift toward copying the incumbents' weaknesses |
| Memory and fetched facts in one unmarked table | confident errors in the roadmap |
| Landscape depth for a one-feature question | hours spent where a paragraph would do |
