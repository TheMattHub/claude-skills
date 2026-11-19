---
name: writing-course-handbooks
description: "Use when writing, revising or reviewing a document that learners follow on their own - participant or student guide, course handbook, lab or exercise sheet, day-1 setup guide, week-by-week plan, onboarding guide - in any language; when a tester or colleague says a guide is hard to follow, too dense, uses terms before explaining them, or that they got stuck at a step; and before handing a course to its first tester. Not for documentation sites (writing-docs-sites) or for exporting to Word or PDF."
---

# Writing course handbooks

## Overview

A handbook is read alone, by someone who cannot ask the author mid-step and will not open
the other documents. It fails in two ways: the reader stalls on a step, or loses the thread.
Every rule below comes from a tester who did one or the other.

## The contract

A handbook that passes has all of these:

1. **Self-contained.** Every concept and step the reader needs is in it; links out are for
   depth only. Planning documents (budget, decisions, minutes, steering notes) are the
   author's sources, never the reader's homework. The same holds sentence by sentence:
   each one names its subject, verb and object (also apply `writing-self-contained-text`, same plugin).
2. **Learning path first.** It is about what the learner does and learns. Project, client
   or business context appears only where the learner acts on it.
3. **Nothing before it is introduced.** At first use each term gets a short gloss in
   parentheses and a link to the glossary or to the section that explains it. Every
   course-specific term is in the glossary. The link lands on the term itself, not on the
   top of the glossary: a glossary table gets one anchor per row
   (`| <a id="g-adapter"></a>Adapter | … |`), and term links point to `#g-adapter`.
4. **One fact per sentence.** Split any sentence that carries a second decision, date or name.
5. **The same shape for every unit** (week, day, module): the template below.
6. **Steps in the order most readers take them.** The default path first, alternatives after,
   labelled with who takes them. The command to type stands alone in its block, then its
   real output, then, optionally, what the file contains.
7. **A way out when stuck.** A troubleshooting table (what happens | likely cause | fix) built
   from real failures, and who to ask.
8. **Orientation.** One paragraph at the top on how the guide is organised, with linked
   sections; links work both in the rendered Markdown and in the PDF.

### Unit template

```markdown
## Week 2 · <topic>

> **In short**
> - **You hand in:** <deliverable, and where it goes>
> - **Decided on Friday:** <what the group decides with it, or "nothing">
> - **To start you need:** <accounts, files, setup, earlier unit>

<Two or three sentences: what you will be able to do by the end.>

### Step by step
1. <Do something real.> You should see <real output>.

### Check yourself
- Predict, then run: <a question the run answers>
- Explain it back: <one thing to explain at the demo>

### Done when
- [ ] <observable result>
```

In Italian: *In breve* (Che cosa consegni · Che cosa si decide venerdì · Che cosa ti serve per
iniziare), *Passo per passo*, *Verifica*, *Fatto quando*.

## Ground truth before release

- Run every step as a participant would: fresh clone, no admin rights, the folders and
  accounts the guide names. Paste real output. Never write an output, error or number you
  did not see; if you cannot run it, mark it unverified for the author.
- No placeholders (`<GIT_URL>`) in a released guide. List what must exist before the
  session: access, accounts, running services, credentials, data.
- Anything with a lead time (IT ticket, account, licence, hardware) is also asked for in the
  unit before, or in a checklist before day 1: readers open the current unit too late.
- Versions live in the lock file and a check script, not in prose.
- ML: seeds set, time-ordered splits, every metric from a run. Label stand-ins ("public
  dataset until the client's data arrives").
- An admin-only step a participant may hit is written as "check it is there; if not, do this".
- Code lines stay under about 85 characters, so the PDF does not wrap them: a wrapped
  command cannot be copied or found with Ctrl+F. Put comments on their own line and split
  long commands (PowerShell: a backtick at the end of the line). Before release, check the
  exported PDF can be searched.

## Tester round

Give the guide to one tester who works alone. Ask them to note every point where they asked
someone, guessed, or did something the guide does not say. Each note becomes a fixed step
or a troubleshooting row, and the revision is logged.

## Reviewing a handbook

Read `references/review.md` and follow it. It starts with the checker:
`python scripts/check_handbook.py GUIDE.md`.

## Pedagogy

- Do first, explain after, in two or three lines.
- One running example through the course (the learner's own dataset, site or machine); the
  final project ships it.
- Checks are predict-then-run, explain-it-back or a judgement on a scenario, not recall.

## Where other things go

- Course facts (people, hostnames, lanes, tool list): the course repo's `CLAUDE.md`.
- Italian prose: writing-italian. Export to Word or PDF: the `docs-export` plugin of this marketplace if installed, otherwise your usual tool (for example Pandoc). A docs site: writing-docs-sites.
- Figures and tables in the Word/PDF version (numbered titles and captions, readable sizes, no tables
  inside list items): the figures-and-tables reference of writing-research-papers (same plugin).

## Red flags

| Thought | Reality |
|---|---|
| "Everyone knows what a webhook / sprint / gate is" | Newcomers don't. Gloss it in parentheses and link it at first use. |
| "The special case needs warning first" | Readers follow the first block they see. Default path first; the special case goes in *To start you need*. |
