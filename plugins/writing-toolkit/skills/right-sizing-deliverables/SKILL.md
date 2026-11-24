---
name: right-sizing-deliverables
description: Use when a report, project or document must match a realistic effort level or reader rather than maximum completeness - course or certification projects, "too perfect", "looks AI-generated", "what would a student at 85% effort produce", "make a normal-effort version", "80/20 version", a deliverable far longer or more polished than its reader expects - and when tempted to add mistakes or imitate a writing style so work looks human.
---

# Right-sizing deliverables

## Overview

Match a deliverable to the scope, length and tools a competent person would produce for that reader. **Right-size, don't degrade:** correctness and honesty are fixed; completeness and polish are adjustable. Never plant errors, hide limitations, or tune style to disguise how the work was made.

## Recipe

1. **Profile the realistic author and reader.** Who would normally write this (Green Belt student at good effort, junior analyst, consultant) and for whom (grader, client)? Write down expected length, tools they would plausibly have, and depth of statistics or detail. Use the course rubric or brief if one exists.
2. **Inventory every element of every artifact** that is handed in, not only the main document: sections, tables, tests, figures, appendices, caveats, and each file in attachments, screenshot sets and code archives.
3. **Classify each element** and act:

| Class | Test | Action |
|---|---|---|
| Required by the brief or rubric | The brief names it | Keep |
| Requested by the user | The user asked for it in this work | Keep |
| Duplicate evidence | Another element already shows the same result (two tests for one question, the same chart from two tools) | Keep one |
| Changes a conclusion | Removing it would change or overstate a finding (non-significant result, key caveat, data-quality issue) | Keep, compressed |
| Reader takes for granted | A competent reader of this type would not miss it (why an I-MR chart, formula of sigma level, glossary) | Drop |
| Analyst extra | Adds rigour but no new conclusion (extra tests, tools-not-used appendix, second robustness check) | One line, an appendix, or drop |

4. **Use only what the data and source support.** Do not add a tool because templates usually have it (e.g. a Pareto chart needs counts of categories). When an extra becomes one line, the line restates a check that was actually run, with its real result; if you cannot name the run, drop the line.
5. **Tools: use what the author plausibly has, and say so.** No licence for the reference software → state it and name the substitutes (e.g. "Excel for descriptive statistics, Python for control charts and tests").
6. **Keep two versions.** The right-sized one is the deliverable; the full one stays as a reference (and as learning material).
7. **Remind the user about authorship rules.** If AI help was used, point them to the venue's AI-use policy, and tell them to rerun and be able to explain every result.

## Boundary

These requests are legitimate scope choices: shorter, fewer extras, the reader's tools and terms, plain prose (stop-slop). Prose target: the plain style of the user's own writing rules, the same for any reader; no persona or "student voice". These are not: planting errors, removing a non-significant result or a key caveat, inventing facts, or adjusting style ("less symmetry", "add typos", "sound like a student") so a grader cannot tell AI was used. If asked, say why in one sentence and offer the right-sized version instead.

## Quick reference: typical course-project profile

| Aspect | Full analyst version | Right-sized student version |
|---|---|---|
| Length | 15–25 pages | 8–12 pages |
| Tools | Scripts, many tests | Course software or stated substitutes |
| Statistics | CIs, robustness, multiple tests | Main test per question, CI for the main effect, the non-significant result |
| Caveats | Full limitations section | One paragraph with the caveats that change conclusions |
| Assumptions | Own section | Short paragraph or box |
| Screenshots or figure set | Every chart produced | The figures the document shows or cites |
| Source code | Analysis plus the tooling that builds the document | What produced the numbers (analysis script, workbook, data, README); document-building tooling stays local |

Rerun the pass whenever the brief changes: a new target (e.g. "+15% satisfaction") can turn an extra into a required element, or add a check to the conclusion.

## Common mistakes

| Mistake | Fix |
|---|---|
| Cutting by gut feel | Run the classification table on every element |
| Adding template tools the data cannot support | Step 4: check the data first |
| Dropping the inconvenient result to look clean | It changes a conclusion: keep it |
| Deleting the full version | Keep it as the reference |
| Claiming tools that were not used | State the real tools and why |
| Compressing an extra into a claim that was never tested ("results held under a log transform") | Quote only runs that exist |
| Writing in a "student voice" or "less symmetric" to read as human | Plain prose, same style as any other document |
| Trimming the report but uploading every chart and script produced | Right-size attachments with the same table |
| Shortening by dropping verbs, subjects or context ("Type, line, power?") | Cut whole elements, never the words that make a sentence readable alone (writing-self-contained-text) |

Related: writing-research-papers, writing-course-handbooks, anthropic-skills:stop-slop.
