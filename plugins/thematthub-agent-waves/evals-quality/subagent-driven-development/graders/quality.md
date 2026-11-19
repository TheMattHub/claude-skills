---
type: llm
---

Judge the final answer against these observable criteria.

1. Each implementing subagent gets a self-contained brief with its own task text and needed context, not the whole conversation, and the plan says so.
2. Every task is reviewed after it is done by an agent other than its implementer, for both whether it meets the task's requirements and the code quality.
3. For the scoring engine, the expected values or tests are produced independently of the implementation (by an agent that sees the requirements but not the code, from hand-derived values), and the implementer may not change those expected values.
4. For the exporter refactor, the plan requires a before-and-after proof that output is unchanged (such as a hash of outputs on fixed inputs or a differential run), not only "tests pass".
5. The plan ends with a review of the whole branch (not just single tasks), done by a strong model, and states which model strength is used for the mechanical tasks versus the review.

PASS if at least 4 of the 5 criteria hold. FAIL otherwise. Name the criteria that failed.
