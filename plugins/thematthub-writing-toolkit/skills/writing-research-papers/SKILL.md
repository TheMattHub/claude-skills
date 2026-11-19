---
name: writing-research-papers
description: "Use when drafting, structuring, checking, revising or preparing to submit a scholarly or professional paper - journal article, conference paper, preprint, JOSS software paper, white paper, technical report - or its journal cover letter, response to reviewers, camera-ready, LaTeX build, references.bib, AI-disclosure or data-availability statement; 'is it ready to submit', 'cite this'. Covers venue choice, number-to-evidence traceability, figures from scripts, reference verification, ethics and a pre-submission checklist; not slides or docs sites."
---

# Writing research papers

## Overview

A paper is a set of claims a stranger can check. Every number comes from a run, dataset or record you can
repeat, every reference from a source you opened, every claim from evidence that exists today. Drafts are
cheap and fine to prepare; sending anything out is the author's act (rule below).

## Rule: submit, post, publish only on the author's word

Prepare drafts, builds, cover letters, reviewer responses and checklists freely. Never submit to a journal
or conference, upload to a preprint server or Zenodo, open a review issue, make a repository public for the
paper, send a report to a client or editor, or email anyone on the paper's behalf without the author's
explicit word at that moment. An earlier "go ahead with the paper" is not that word. Say what is ready and
what is left, then stop.

## Choose the document type first

| Type | Reader and job | Shape |
|---|---|---|
| Research paper (journal, conference, preprint) | peers; add verified knowledge | abstract, introduction and gap, related work, method, results, discussion and limitations, conclusion |
| Short or software paper (JOSS) | reviewers and users; show the software exists, is needed, works | fixed short sections set by the venue |
| White paper | decision makers; argue a position or solution | executive summary first, evidence-backed argument, recommendation |
| Technical or industry report | project owner or client; record what was done and found | summary, scope, method, findings, limits, recommendations, appendices |

Then pick the venue and read its guidelines (`references/venues.md`). White papers and reports:
`references/white-papers.md`.

## Workflow

1. **Venue and rules.** Read the author guidelines or call for papers end to end, live, and date the check:
   length, template, anonymity, required statements, policies on data, preprints and AI.
2. **Structure before prose.** One file per section, one shared bibliography. Abstract = problem, gap, what
   was done, what was found (with numbers), why it matters. If the author has earlier papers, follow
   their structure and voice.
3. **Claims inventory.** List every number, count, version, date, comparison and "we show". Beside each:
   the run, dataset, test or source that supports it. No support: produce it or cut the claim. Numbers are
   generated or copied from a generated artefact, never typed from memory; a check fails if source and
   text differ.
4. **Figures and tables from scripts** in the project, reading the same data as the analysis, rerunnable.
   In Word/PDF: every table has a numbered title above, every figure a numbered caption below; figures
   centred and readable at print size (never shrunk to save pages). Details and pandoc traps:
   `references/figures-tables-word.md`.
5. **Method and results, stated generally.** Data (source, selection, cleaning), code or materials and
   how to obtain them, statistics (tests, intervals, effect sizes, multiplicity, seeds or randomisation),
   what was pre-specified, negative and null results reported. Use the field's reporting guideline
   (`references/checklists.md`).
6. **Ethics and integrity.** Ethics approval and consent where people, animals or personal data are
   involved; conflicts of interest; funding and role of funders; contributions of each author; data and
   code availability statements; AI-use disclosure as the venue requires, written from evidence.
7. **References: fetch, then cite.** Open each record (publisher, DOI, arXiv, database). Anything from
   memory is flagged `verify` until checked; none remain at submission. Unfetched sources are not cited.
8. **Hamburger paragraphs**: topic sentence, supporting detail, closing sentence; simple lists for parallel
   items. One idea per paragraph; wording no stronger than the evidence.
9. **Fair related work.** What others do well, why this work differs, what it does not do or costs.
10. **Limitations and threats to validity** in their own section: sample, setting, single site, model or
    machine, generalisability, conflicts, young project. Reviewers find them anyway.
11. **Build and check** (`references/build-and-checks.md`), **review** and **pre-submission checklist**
    (`references/checklists.md`).
12. **After submission: revisions.** Answer every reviewer point, numbered, quoting the comment, saying
    what changed and where (page, line) or why not, politely and with evidence. Change the manuscript
    for each accepted point; track changes; rerun affected numbers; never edit a claim without rerunning
    its source. Detail in `references/venues.md`.

## Version and evidence discipline

Describe what exists now: the released software version, the dataset version, the date of the run. A
feature on a branch but not in the release is out of the paper or marked "unreleased". If evidence is
older than the thing it supports (benchmarks on an old version), rerun or say so in the text.

## Confidentiality and ownership

No client, employer or confidential material in a paper without written permission and the required
internal approval. Never name a colleague's or employer's repository, dataset or client as the origin of
the work unless the author says so; ownership statements are the author's to make.

## Red flags

| Thought | Reality |
|---|---|
| "AI disclosure: one line is enough" | Venues treat an incomplete disclosure as misconduct. Tools, dates, role, checks. |
| "Report the significant result only" | State all pre-specified outcomes and null results. |
| "The white paper can round up the benefit" | Overclaim is marketing. Quote the evidence and its limits. |
| "Reviewer 2 is wrong, say so" | Respond with evidence and courtesy; if misread, the text was unclear: fix it. |

## References

- `references/venues.md`: venue table, how to read guidelines, journal cover letter, double-blind, camera-ready,
  revision rounds, archive step.
- `references/white-papers.md`: white papers and technical reports, confidentiality and approvals.
- `references/build-and-checks.md`: LaTeX route, bibliography, encoding, limits, preview commands.
- `references/figures-tables-word.md`: numbered table titles and figure captions, readable figure sizes,
  centring, column widths, pandoc-to-Word traps, checks before hand-off.
- `references/checklists.md`: review passes, reporting guidelines by field, pre-submission checklist.
