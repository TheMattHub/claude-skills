Eval suite for the `thematthub-agent-waves` plugin: each skill is loaded for a matching request and left alone for an unrelated one.
Run: `claude plugin eval plugins/thematthub-agent-waves --ablation none -j 4`
Each case is a full, billed model run (1 run, sonnet, read-only tools).
Results land in `evals/results/` (gitignored).
Quality suite, with and without the plugin (`evals-quality/`): `claude plugin eval plugins/thematthub-agent-waves --eval-dir evals-quality --runs 4 -j 4`
It runs every case in both arms, so it costs about eight times a trigger run; results land in `evals-quality/results/` (gitignored).
