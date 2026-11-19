Eval suite for the `docs-export` plugin: the skill is loaded for a matching request and left alone for an unrelated one.
Run: `claude plugin eval plugins/docs-export --ablation none -j 4`
Each case is a full, billed model run (1 run, sonnet, read-only tools).
Results land in `evals/results/` (gitignored).
