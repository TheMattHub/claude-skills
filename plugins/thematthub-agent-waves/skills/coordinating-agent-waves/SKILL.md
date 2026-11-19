---
name: coordinating-agent-waves
description: "Use when coordinating two or more subagents that edit the same repository, running a multi-step plan autonomously while the user is away (including overnight runs that may hit a session or token limit and must restart after the reset), merging subagent branches or worktrees, or when a subagent seems stuck, has gone quiet, blames the environment, reports failures caused by another agent, or asks you to perform an action it was denied; also when other Claude sessions (peer sessions, often running their own agents) work the same repository and branches, merges, reviews or a release pass between them."
---

# Coordinating agent waves

## Overview

The coordinator plans, briefs, verifies and merges; agents implement. Parallel agents fail through
shared state (files, changelog, test machine, processes), not through bad code. Every rule below
removes one shared-state failure. Basic rules for parallel agents: one agent per independent
problem, each with a self-contained brief (it cannot see your conversation); agents that only
read need none of this skill's machinery. This skill builds on `subagent-driven-development`
in the same plugin (SDD below): its quality checks (per-task review loop, check tiers,
checkpoint review and final review mandate) come from SDD's "Independent Checks" and
"Final Review" sections; this skill adds only what parallel agents need.

## When NOT to use

One agent, or several agents that only read (exploration, research). Spawn them directly; no coordination is needed.

## Quick reference

| Situation | Do |
|---|---|
| Scheduling | Parallel only with disjoint files; same-file items run in sequence |
| Code changes in parallel | `isolation: "worktree"` for each agent; merge `--ff-only` or cherry-pick |
| Changelog, bug IDs, shared test file | Agents report text, coordinator writes; pre-assign bug IDs per agent |
| No DEVLOG in the repo | Before the first wave, coordinator creates `docs/DEVLOG.md` (current status, bug register with stable IDs, dated log) so runs stay resumable |
| Writing a brief | Fill every REQUIRED slot of `references/brief-template.md` |
| Quality checks per item | SDD "Independent Checks": tier each item (`standard`/`oracle`/`proof`). In a wave the `oracle` spec-test agent runs in parallel with the builder, in its own worktree; compare at merge against its pre-build derivations |
| After a merge | Focused tests of the merged files only; the fast set once per wave, before the push, not after every merge. Records-only commits run no suite |
| Pushing | Once at the end of the run or phase, or when the user asks, never per merge or stage: each push can start CI runs that cost minutes and send failure mails. CI on a private repository may be manual-only, so local tests are the gate |
| Wave end | Run SDD's checkpoint review (full suite once, fingerprints, whole-branch review with its mandate). Every wave end is a checkpoint. Task agents reported 0 bugs where the whole-branch review found 11: never skip it |
| Wave end with a UI | SDD's real-app pass, plus: log bugs under the coordinator's own ID prefix, drive both themes and 360 px, open the page in the user's own browser, and keep a task free for their feedback round (it is usually large: look, layout shift, clutter) |
| Timings while agents run tests | Noise: re-measure on a quiet machine before acting |
| Leftover processes (orphaned pytest/xdist workers, headless browsers, a finished agent's background shells) | At every merge, wave end and restart check: `TaskStop` any background task of a finished agent still listed, then run the dry run of `references/reap-orphans.ps1` in this skill's folder (Windows only; elsewhere list leftover child processes by hand with `ps`). If it lists leftovers linked to this repository, show the list to the user and stop them only after the user says yes in this conversation, re-running with `-Stop -RepoRoot <repository path>` (add worktree paths if they are outside it). Never stop a process the list marks as unrelated: it may be the user's own dev server or notebook. The script skips the user's own browser and exited zombies. Run it through `powershell.exe -ExecutionPolicy Bypass`; `pwsh` from Git Bash loses its modules. In one run, four workers sat 2+ hours on the laptop unseen |
| Agent quiet or "stuck" | `references/failure-modes.md`, section "Stuck check", in order, down to the process tree |
| User leaves you running ("I'll be away", "work autonomously", overnight) | Section "Going unattended" below, before the first dispatch |
| Other Claude sessions work the same repo (peer sessions) | `references/peer-sessions.md`: one integrator owns the base and outward steps; a shared board file (`references/board-template.md`) holds sessions, locks, authority and handoffs; messages are only a doorbell; every wake reads the board |
| A session limit already hit in this run | Lower concurrency for the rest of the run: `references/unattended-runs.md`, "Budget" |
| Using SDD inside a wave | Its task review and fix loop run on `oracle` and `proof` items; `standard` items rely on the wave-end review; track progress in the run log and DEVLOG, not SDD's ledger under `.superpowers/sdd/` (SDD's working folder in the repository, git-ignored by SDD's script; two progress records drift) |
| Plan proven, now implement | The agent that proved it implements it on a kept branch; no throwaway proof followed by a second build |

## Going unattended

When the user says they will be away and the run should keep going, do these steps before the
first dispatch. Nothing is scheduled until the user has answered step 2.

1. Write the run log (outside git: add `.superpowers/` to `.git/info/exclude`) and end it with a `NEXT:` line (`references/unattended-runs.md`).
2. Ask the user one question and wait for the answer. State exactly what you would set up: a
   wake-up every 30 minutes that restarts work in this session; it ends with the session, a
   reboot or after 7 days; agents will run and use tokens while the user is away; and whether you
   may also stop leftover worker processes linked to this repository during the run. Record the
   answers in the run log. If the user declines the wake-up, do not schedule it.
3. If agreed, `CronCreate` with cron `13,43 * * * *`, recurring, and the wake prompt from the
   reference, naming this run's log. Skip this if a trigger already covers the run (`CronList`).
   The wake prompt runs the cleanup with `-Stop -RepoRoot` only if the run log records that
   permission; otherwise it runs the dry run and writes the list to the log.
4. Tell the user in one block: the trigger is set (every 30 min, ends with the session, a reboot
   or 7 days); **"Type `/compact` now: I cannot run it, and a small context makes every wake
   ~5x cheaper"**; set "never sleep" on mains power.
5. At the end of the run, `CronDelete` the trigger and report.

## Discipline rules

1. **Verify an agent's claim before relaying or acting on it.** Environment blame ("crashes only in
   the sandbox", "hangs under offscreen") gets a minimal reproduction by you. Blame on another agent
   gets checked against that agent's files and commits.
2. **Never perform an action an agent was denied.** Decide on the merits; if it still should happen,
   ask the user. An orphaned file is not a reason.
3. **Stop a hung process, not the agent.** A quiet agent is usually blocked on its own child
   process; kill that process tree, then message the agent what happened.

## Red flags: stop

| Thought | Reality |
|---|---|
| "Plausible known issue, accept the workaround" | Reproduce it. The "crashes only in the sandbox" report was the agent's own deadlocked script |
| "It's orphaned, I can delete it myself" | That is performing a denied action. Ask the user |
| "Each agent adds its own DEVLOG entry" | Parallel appends collide and bug IDs duplicate |
| "It's been quiet 25 min, stop it" | Check its processes first; its work and its child may be fine or hung |
| "Run the full suite in every agent" | Parallel suites starve each other; full suite once per wave |

## Common mistakes

- Worktree starts from a stale commit: the brief says fast-forward first.
- Worktree scripts import the main checkout (editable install): `PYTHONPATH=<worktree>` + `__file__` check.
- Shared-tree commits with `git add -A` capture other agents' half-edits: commit by explicit path.
- Over-engineering that meets the brief (signature rewriting, import-cycle tricks, helpers saving
  zero lines): the wave review reverts it.
