---
type: llm
---

Judge the final answer against these observable criteria.

1. Agents whose work touches the same file (utils.py, tests/test_core.py) are run one after another, or each agent works in its own separate working copy or branch, and the plan says how the results are merged.
2. The shared records (the changelog, bug numbers) are written by the coordinator from what agents report, or pre-assigned, instead of every agent editing them.
3. The plan has a written run log or status file, kept outside what is committed, that lets the work resume after an interruption such as a session limit, and says what the user should expect or do before leaving.
4. The coordinator checks agents' claims itself (reruns or reproduces them, does not simply accept "done" or "the environment is broken") and ends with a review of the whole combined result, not only per-agent reports.
5. Pushing to the remote happens once at the end (or when asked), not after every merge, and the full test run is done once rather than after each merge.

PASS if at least 4 of the 5 criteria hold. FAIL otherwise. Name the criteria that failed.
