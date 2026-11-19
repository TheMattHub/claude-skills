# Failure modes and checks

## Stuck check (in order; answer the user with the evidence)

1. `ListAgents`: running or completed?
2. Commits on its branch (`git log --oneline <base>..<branch>`) and `git status` of its tree.
3. Newest file mtimes in its tree (`find . -name "*.py" -printf '%TH:%TM %p\n' | sort -r | head`).
4. Processes with start time and command line. Windows:
   `Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select ProcessId, ParentProcessId, CreationDate, CommandLine`.
   Anything older than the longest legitimate command is suspect; follow ParentProcessId to the
   shell that launched it (a heredoc script shows its whole body in the parent's command line).
5. `py-spy dump --pid N` (add `--locals`) on the suspect: the stack names the blocking line.
6. Only for a process step 4 showed to be that agent's child: show the user the process and its
   parent and ask before stopping it; in an unattended run, stop it only if the run log records
   `stop leftovers yes`, otherwise log it and move to other work. Then kill the process TREE
   (`taskkill /PID <root> /T /F`), confirm it is gone, and message the agent: what hung, that it
   was killed, and to rerun under a hard timeout.

## Failure modes seen in a long run (symptom -> cause -> prevention)

| Symptom | Cause | Prevention |
|---|---|---|
| Test run alive for an hour | A failure path opened a modal dialog; offscreen Qt never returns | Autouse fixture makes dialog openers raise in tests; hard `timeout` on every command |
| Agent "running" for hours after its work | Its scratch script deadlocked in `thread.wait()` (queued `quit()` never delivered because the main loop stopped) and outlived it | Stuck check above; timeouts in every brief |
| Other agents' tests fail with import errors | One agent's mid-edit state (import cycle, half-split commit) in the shared tree | Worktree isolation for parallel code changes |
| Worktree checks pass but test old code | Scripts run by path import the main checkout via the editable install | `PYTHONPATH=<worktree>` and a `__file__` check |
| Worktree far behind | Worktree created from an old commit | Fast-forward to the main branch first |
| Oracle test fails against a correct engine | The test's own model had a tie or a degenerate start | Check test construction first; fix construction, keep expected values |
| Review finds clever code | Brief satisfied literally (signature surgery, lazy re-exports, zero-saving helpers) | Wave review mandate: simpler, not cleverer |
| Suite 50-60 s instead of 30 s | Several agents running suites at once | Re-measure quietly |
| Order-dependent test failure | Global state (settings) leaking between tests | Reproduce with an ordered serial pair before and after the fix |
| Harness refuses `isolation: "worktree"` ("git resolves its working tree to ...") | Drive-letter case differs between the session path and git's (`c:\` vs `C:/`) | `git worktree add -b <branch> <scratchpad>/wt/<name> <main>` yourself; brief the agent to cd there, set PYTHONPATH to it, never touch the main checkout; merge the branch yourself |
| Same refusal, and the agents only ADD files (one new file each, no edit to existing code) | Same cause; a known issue at the time of writing, check whether it still applies | No worktree: run them in the main checkout, each owning its one file, git read-only for agents, coordinator verifies and commits by explicit path (12 agents in two waves, no collision). Each refused launch leaves a locked worktree and branch: check clean and merged, `git worktree unlock`, remove, delete the branch. Hand-made worktrees (row above) go around the harness's check; ask the user before making that the default |
| Deleted/renamed module still imports inside a worktree | An editable install's finder maps the package to the main checkout | PYTHONPATH=<worktree root> for every command; check `<pkg>.__file__` |
| Agent writes to the user's real profile | A subprocess or UI path resolves the user data dir; tests set no override | Session-wide env override in conftest before any import; a test that a subprocess sees it |
| Parallel suite hangs after "node down" at ~97 % | A refactor moved code to a new module; a test's monkeypatch of the OLD module no longer applies and a real modal opens | Verbose `-n auto -v` run, last test on the dead worker; patch the new module; make the modal guard cover every Qt-using test |
| Pre-assigned bug IDs already taken | A peer session used them in tests and the CHANGELOG but never added register rows | Reserve after grepping the regression tests and both changelogs, not the register alone |
| Coordinator's own root fix breaks every grouped edit | A guard made a property false "while a transaction is open", and listeners were notified inside that window | Final review on the coordinator's commits too; for a new state guard, test what a listener reads at notification time |
| Public export gate fails on a just-merged test | A test file mixed engine and UI tests; the product was reached via a sibling test module or a fixture, invisible to the import-based classifier | Brief: UI tests in `test_ui_*.py` files that import the product; run the export gate before pushing |
| Worktree agent "cannot write the brief's State section" | The worktree isolation guard blocks writes to the main checkout | Brief: State lines go in the hand-back report; the coordinator appends them |
| `git worktree remove` refuses a finished agent's worktree ("locked") | The harness locks each agent worktree and the lock outlives the agent | Check the branch is merged, `git worktree unlock`, then remove and delete the branch |
| Spec-test agent's tests pass only because the builder edited the spec | The builder may correct spec values while building; tests written later follow the amended spec, so build and test agree by construction | Spec-test agent writes from the design FIRST (in parallel with the build) and reports every value it derived; at merge compare against its pre-build derivations, and treat a builder's value change as a claim to re-derive |
| A gated outward step (publish, tag) denied to an agent | The permission system's "public surface" rule | Do not retry it yourself; leave exact commands for the user; do it only on the user's explicit word |
| Final reviewer dies at a usage limit mid-run | Weekly limit on the review model | Reviewer appends findings to a file as it goes (it did: nothing lost); fix from the file, note what the review did not reach |
| Merged perf work is slower on small models though each agent proved a win | Each agent benched its own change at scale; per-event bookkeeping from two changes adds up on short runs (in one run: +5% on the small models after a 2.3x gain at 100x scale) | After merging perf work, A/B the old and merged trees alternated in one window on the small set too, not only the big benchmark |
| An agent probing a repo tool with `--help` wrote a folder named `--help` into the repo root | The tool takes any single argument as its target folder and replaces the folder's content: no argument parser | Brief: read a tool's source before the first run and give every writer an explicit scratch target; in the repo, a test that every tool with a `__main__` builds an ArgumentParser |
| Repros, cold walks and tools ran another engine than the checkout, though the versions matched | A released wheel of the same package sat in site-packages beside the editable install; it wins for console scripts, for a script run by path and from any folder but the repo root | Brief: run from the repo root or put the repo first on `sys.path`, and print `<pkg>.__file__` once; a status script that fails when a second copy of the package is installed |
| A "new user" walk or a count was coloured by the user's own extensions or settings | The per-user store is loaded on import, from a fresh venv too | Brief: point the user-data variable at an empty scratch folder before any import; never write the real store |
| A command given to the user ran in the wrong Python | A placeholder for the interpreter in the repo's docs can be a real command in the user's shell (e.g. `py`, which follows the active venv) | Give the user the interpreter's full path in every pasted command and say which environment it targets; have the status script print the interpreter and the removal commands in paste-ready form |
| Before an environment change the user was told "safe now", but desktop MCP servers of the same interpreter were still running | Other applications start servers from the development interpreter; the orphan sweep only sees this session's leftovers | Before proposing an install or uninstall, list every process of that interpreter by command line and name the applications to close first |
