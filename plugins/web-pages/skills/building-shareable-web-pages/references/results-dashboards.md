# Dashboards that present model or experiment results

Read this when a page shows simulation, what-if or experiment results. The general rules (labels, live data, clutter, visible failures) stay in `SKILL.md`.

- **The question and a plain answer** on top, computed by one function from the numbers: "Yes, very likely"
  only when the whole interval clears the target, "No" when wholly on the wrong side, else "Not clear yet";
  a run repeats until clear, capped; within a practical-equivalence band the answer is "No change you would
  notice". A verdict never comes from colour.
- **Intervals, targets, words:** each KPI as an interval bar (yours vs baseline), the target as a line, the
  delta with an arrow and a word ("better", "worse", "no clear change").
- **Where it hurts:** one callout naming the cause (the bottleneck and why), only when there is one; it may
  not name a passive container (a buffer) instead of the process behind it.
- **Can I trust this?** The checks passed, warm-up removed, replications and precision; state what a
  deliverable is a version of ("made for v002"); show limits in the page (unsupported browsers, data date)
  instead of a blank screen.

## Common mistake

| Mistake | Fix |
|---|---|
| Answer by colour | One function, words, interval vs target |
