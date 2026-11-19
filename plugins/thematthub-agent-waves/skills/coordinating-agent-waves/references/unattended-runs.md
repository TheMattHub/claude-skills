# Unattended runs: session limits and restart triggers

## Budget

- The rolling usage window is shared by the coordinator and every agent it runs. Its size depends
  on the subscription, and the coordinator cannot see what is left, so "stop just before the
  limit" cannot be done. Make every unit of work survive being killed instead (next section).
- With the restart trigger set, a limit hit no longer stops the run. It costs the in-flight work
  of the agents it kills: their uncommitted changes and their context. Re-dispatched agents start
  over from their last commit.
- So concurrency follows evidence, not presence. Start with the usual waves (disjoint items in
  parallel). Once a limit has hit in this run, the window cannot hold that wave: drop to at
  most two agents, large items (opus/fable, long reviews) alone, for the rest of the run. On
  this repo's subscription, two large agents at once exhausted the window twice in one night;
  a larger plan may never hit it, and then the rule never fires.

## Make work survive a kill

- Run log outside git (e.g. `.superpowers/<run>.md`; `.superpowers/` is the working folder these two skills share in the repository; keep it out of git: add `.superpowers/` to `.git/info/exclude`), updated after every step. End it with a
  `NEXT:` line: heads, worktrees, what is dispatched, what to re-dispatch if it dies.
- Agents commit once per task. Reviewers append findings to a file as they go: a review killed
  at the limit otherwise loses everything (it happened twice).
- Long external processes (benchmarks, model runs) go through `run_in_background`, so their exit
  wakes you. Write one result file per attempt and skip finished ones on restart. A reboot kills
  them: the restart check tests that they are alive and restarts them.
- The COORDINATOR starts long runs, never an agent. An agent that waits on its own background
  job wakes the coordinator every few minutes (each pause is a task notice) and spends the
  window; brief agents to hand back when their code is done, with the command to run.
- Keep each package's brief in a file beside the run log (`.superpowers/<package>-brief.md`)
  with a "State and next steps" section the agent appends to at each commit. Re-dispatching a
  dead agent is then one short prompt ("read the brief file and the branch's commits, continue"),
  not a long brief re-sent into the next window. Agents also die of network drops, not only of
  limits: the same restart covers both.

## Restart trigger (CronCreate)

Ask before scheduling (Going unattended, step 2): one question, then wait. It states the
wake-up every 30 minutes that restarts work in this session, how it ends (the session, a reboot
or 7 days), that agents will run and use tokens while the user is away, and whether leftover
worker processes linked to this repository may be stopped during the run. Write the answers in
the run log (`Permissions: wake-up yes/no; stop leftovers yes/no`). The wake prompt below reads
that line.

Measured cost of one wake with nothing to do, coordinator context ~300k tokens. Equivalents
follow API weights (1-hour cache write 2x, read 0.1x); the subscription meter is assumed to
scale the same way.

| Wake | Cache write | Cache read | ~Input-token equivalents |
|---|---|---|---|
| Cold (over 1 h since the last turn) | 250k | 310k | ~530k |
| Warm (under 1 h) | 1k | 570k | ~60k |
| During the limit (refused) | 0 | 0 | 0 |

Idle cost per hour at ~300k context, and the longest wait after a reset:

| Schedule | Cost/h | Longest wait | Note |
|---|---|---|---|
| Every 3 h | ~180k | 3 h | Every wake cold |
| Hourly | ~530k | 1 h | Worst: 60 min plus jitter always lands past the 1-hour cache, so every wake is cold |
| Every 30 min (`13,43 * * * *`) | ~120k | 30 min | **Default**: every wake warm |
| Every 15 min | ~240k | 15 min | Twice the cost for 15 minutes less wait |

- Cost scales with the context size: at 60k context a warm wake costs ~12k. The model cannot
  compact itself: a cron prompt `/compact` arrives as plain text, and no tool triggers it.
  Options, in order:
  1. Ask the user to type `/compact` right after the trigger is set (Going unattended, step 4).
  2. Hands-free, if the user agrees: a lower auto-compact window (the `autoCompactWindow`
     setting or `/autocompact <tokens>`, e.g. 120000) keeps the context small for the whole run.
     This is a settings change: ask first.
  3. The user starts the run in a fresh session that only reads the run log.
- Wake prompt (fill in the log path and the run's own resume steps):

  ```text
  Restart check for <run>. Read the last 8 lines of <run log>, run `git worktree list` and
  ListAgents, and check <external processes, if any>. Run the leftover sweep
  (`powershell.exe -NoProfile -ExecutionPolicy Bypass -File <this skill's folder>/references/reap-orphans.ps1`, folder filled in from the skill's base directory; Windows only). If the run log
  records "stop leftovers yes", add `-Stop -RepoRoot <repository path>` and say how many it stopped;
  otherwise run it as the dry run and write the list to the log. Never stop a process the list marks as unrelated. If an agent is running or the NEXT line
  says done, reply in one line and stop. Otherwise resume from NEXT: re-dispatch only the dead
  item (one agent if a limit hit this run), restart a dead external process, then continue as
  the log says.
  ```
- The job lives only in the session. A closed VS Code or a reboot kills it, and overnight sleep
  most likely stopped it too (an hourly job did not fire for 8 hours). Before the user leaves,
  ask them to set "never sleep" on mains power and Windows Update active hours. After a restart,
  the user says "resume from the run log".
- Recurring jobs expire after 7 days. `CronDelete` the job when the run is done.
