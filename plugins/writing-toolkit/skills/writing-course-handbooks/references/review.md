# Reviewing a handbook

The reviewer is the newest participant: starts from zero, has only this file, reads it in
order and does what it says. Review what that reader meets. Staffing, schedules and the
project plan belong to the author's planning documents; a review of the handbook does not
rebalance them.

## Passes

1. **Run the checker.** `python scripts/check_handbook.py GUIDE.md` (`--glossary HEADING`
   if it cannot find the glossary table). It lists broken section links and missing
   images, placeholders, sentences over 30 words, units without the summary box, the
   *Check yourself* section or the *Done when* list, and glossary terms whose first use is
   not a link (bold at a definition counts). Its term list has false positives, mostly
   the same word in another sense ("tempo ciclo" for *Ciclo*) and irregular plurals: read
   each line before reporting it. Run it on the guide in place, since images resolve
   relative to it. Keep its counts as the before figures.
2. **First use, in reading order.** Read from the top. At each paragraph, list every term,
   acronym, person, team, project, client, event or decision a newcomer could not know at
   that point. For each: is it explained here or earlier? Is it in the glossary? The
   checker only knows terms already in the glossary; this pass finds the missing ones.
3. **Self-containment.** List every pointer outside the guide: another document, a
   meeting, "as agreed", a decision taken elsewhere, initials not yet introduced. Fix by
   bringing in the lines the reader needs, or by cutting.
4. **Focus.** Mark paragraphs about the project, client, budget or organisation that the
   learner does not act on. Fix by cutting or by moving to the project documents.
5. **Density.** Take the worst sentences from the checker. Rewrite one or two in the
   guide's language, one fact per sentence, to show the fix.
6. **Unit shape.** Every unit has the *In short* box with its three slots, steps, a check
   and *Done when*. Each *Done when* item can be met with the data the reader actually has
   (stand-ins included).
7. **Steps and code.** Default path first. Each command visible on its own. Everything
   needed before day 1 (accounts, access, rights, running services) is listed before day 1.
   Run each snippet, or trace it against the data it reads: time zones, empty splits,
   leakage through ID or future columns, labels missing from training.
8. **Consistency.** Counts, names, numbering and rules agree across sections (a rule that
   forbids what a later unit teaches; "eight people" and seven in the table).

## Output

Findings, grouped and in this order:

1. **Blocks a step**: the reader cannot continue (passes 6–7).
2. **Breaks understanding**: a term, pointer or jump the reader cannot resolve (passes 2–4).
3. **Slows reading**: density and shape (passes 5–6).
4. **Inconsistencies** (pass 8).

Each finding: section, what the reader hits, the fix. Close with the checker's counts.
Offer to apply the fixes; a review does not rewrite the guide.
