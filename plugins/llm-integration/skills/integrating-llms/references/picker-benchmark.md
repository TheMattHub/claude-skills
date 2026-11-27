# Benchmarking and distilling small-model pickers

## Overview
A picker benchmark is only as good as its test set, and most of the ways it lies are built in before the first engine runs. Measure the role the picker will really play, over all the options it will really see, at the precision and on the hardware it will really run.

## Test sets
- **Several writers, none of them the training data's writer.** Use 3-4 different models (or people) for about 40 requests each, every one given only the option names and the target, and tag each row with its writer. One writer's phrasing flatters engines trained or prompted in that style.
- **The deployed role.** If an agent calls the picker, also build a set from the agent's own queries: give the agent the real system prompt and the search tool as its only tool, plus a request with a known gold, and record its first query. Agents write short catalogue-like phrases, and these score very differently from user wording.
- **Frozen first.** Commit each set before any engine or teacher sees it. Dedupe it against training data by token overlap, log every dropped row, and record doubts in notes, never by editing the set.
- About 150 rows per set. With 25-40 rows, one or two rows decide the ranking.

## Engines
- **Rank all N options.** A keyword top-10 shortlist caps every engine at the shortlist's recall (in our case the gold was in it for 94 of 150 rows), which hides real differences. Shortlist only for engines that cannot take N, and say which ones.
- **Same precision and hardware as deployment.** If the bench loads fp16 on a GPU and the product loads fp32 on CPU, measure both. CPU time can be 10x GPU time.
- Baselines: keyword search alone, and the untuned base model.

## Distillation
- **Teacher gate before paying for labels.** First run the candidate teacher as a picker on the frozen sets. Pay for its labels only if it beats the current best teacher by a margin you set in advance (we used 3 points).
- Label about 1,000 training requests with the teacher's top-3, cached and resumable. Also train an "agreed" student on only the rows where the teacher's top-1 equals the generated gold: it costs nothing extra.
- One recipe and one seed, and no tuning against any test set.
- **Overfitting check:** a fine-tune on a few dozen questions memorises them (54/54 on its training questions, 11/25 on new ones). Always report training-set accuracy next to test accuracy.
- A student can beat its teacher on writers neither has seen. Check it per writer, never only overall.

## Metrics
- Top-1 and top-3 per set and per writer, median latency, and cost per decision.
- A paired sign test on the rows where the two engines disagree before calling a winner. Otherwise write "within noise".
- **Retries mean the next pick:** accuracy within 1, 2 and 3 tries against the cumulative time (decision time x tries used). A fast engine can catch a slow one this way. Retry k counts as right when the gold is in the first k of one ranking.
- Writer x engine table: does an engine do better on requests its own family wrote?

## Write-up
Lead with the answer and the recommendation. Then give one table with every engine, and charts of only the engines the story needs: the winners, the baselines, and failures that teach something. Show only the trustworthy sets in the headline. Move superseded rounds to the lab notebook, never delete them. Recompute every number from the result files.

## Running it unattended
Write one result file per engine and set, keyed by row id, so a restart skips finished rows. Run long steps as foreground chunks of 9 minutes or less, and train from a checkpoint. **REQUIRED SUB-SKILL:** use coordinating-agent-waves for overnight runs and session limits.

## Common mistakes

| Mistake | Fix |
|---|---|
| The same model writes the training data and the test set | test writers from other families, plus an agent-phrased set |
| Re-ranking a top-10 shortlist | rank all N |
| Benchmarking fp16 on a GPU, deploying fp32 on CPU | measure the deployed setup |
| Paying for big-model labels on faith | gate on the teacher as a picker first |
| "Retries" read as API error retries | the next-pick curve against time |
| A 3-row gap reported as a win | sign test |
