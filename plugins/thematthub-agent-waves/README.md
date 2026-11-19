# thematthub-agent-waves

Two skills for coordinating several Claude Code subagents on one repository. For people already
comfortable with subagents and git worktrees; not a first plugin for beginners.

## Before you use this

- It starts several agents at once, and they use tokens fast.
- Unattended runs schedule a recurring wake-up only after you agree.
- The cleanup script can stop processes: only ones linked to the repository, only after you agree.
- Developed and tested on Windows with Python projects; expect rough edges elsewhere.
- Do not run unattended on a machine with other important work running.

## What it reads, writes and runs

- `subagent-driven-development/scripts/task-brief` reads a plan file and writes one task's text under `.superpowers/sdd/<plan>/` in the repository.
- `review-package` reads the plan and git history (commit list, diff) and writes a review file to the same folder.
- `sdd-workspace` creates that folder with a self-ignoring `.gitignore` and a plan-path marker.
- The first two accept an optional output path argument; the skills do not use it.
- `coordinating-agent-waves/references/reap-orphans.ps1` (Windows) lists python, node, headless browser and PowerShell processes whose parent is gone and that are older than 15 minutes. By default it only lists. With `-Stop -RepoRoot <path>` it ends only those whose command line mentions the repository, and the skill asks you first.
- Scheduled wake-ups: a 30-minute recurring trigger in your session, set only after you agree; it ends with the session, a reboot or after 7 days.
- Git: worktrees, branches, merges and commits in your repository; pushes only when you ask.
- Nothing is sent to any service other than the Claude session itself.

## Install

```
/plugin install thematthub-agent-waves --marketplace TheMattHub/claude-skills
```

## Skills

- `coordinating-agent-waves`: briefs, worktree isolation, merge order, stuck checks, leftover processes, unattended runs, several sessions on one repository.
- `subagent-driven-development`: executes a written plan one task at a time: fresh implementer, review per task, independent checks, final review. `coordinating-agent-waves` builds on it.

## Requirements

git; `bash`, `awk` (Git Bash on Windows) for the scripts; PowerShell only for `reap-orphans.ps1`.

## Optional companion

The `superpowers` plugin (https://github.com/obra/superpowers) adds plan, worktree and branch-finishing skills; these work without it. Both plugins ship a `subagent-driven-development`; disable one.

## Attribution

`subagent-driven-development` is a modified fork of a `superpowers` skill (MIT, Jesse Vincent). See `NOTICE.md`.
