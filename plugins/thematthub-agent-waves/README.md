# thematthub-agent-waves

Two skills for coordinating several Claude Code subagents on one repository.

**Who it is for:** people already comfortable with Claude Code subagents and git worktrees.
It is not a first plugin for beginners.

## Install

```
/plugin install thematthub-agent-waves --marketplace TheMattHub/claude-skills
```

## Skills

- `coordinating-agent-waves`: the coordinator's playbook for two or more agents editing the same
  repository. Briefs, worktree isolation, merge order, stuck checks, leftover processes,
  unattended overnight runs, and several sessions sharing one repository.
  Example: "Run these four independent fixes in parallel, merge them, and review the result."
- `subagent-driven-development`: executes a written plan one task at a time. A fresh implementer
  per task, a review after each, independent checks for risky tasks, and a final whole-branch
  review. It depends on nothing else; `coordinating-agent-waves` builds on it.
  Example: "Execute docs/plans/export-plan.md with subagent-driven development."

## Cost

Several agents run at once and use tokens fast. Reviews and re-reviews add more. Start with a
small plan and watch usage before an unattended run.

## Requirements

- git.
- `bash`, `awk` and `git` for the three scripts in `subagent-driven-development/scripts/`
  (they are bash scripts; on Windows, Git Bash provides them).
- PowerShell, only for `references/reap-orphans.ps1`, the Windows-only cleanup of leftover
  processes. Elsewhere, list and stop them by hand with `ps` and `pkill`.

## Optional companion

The `superpowers` plugin (https://github.com/obra/superpowers) adds skills for writing plans,
worktrees and finishing a branch. The skills here work without it and say what to do instead.

This plugin's `subagent-driven-development` has the same name as the skill in the `superpowers` plugin it
derives from; with both installed Claude sees two near-identical skills, so disable one of them.

## Attribution

`subagent-driven-development` is a modified fork of a skill from `superpowers` (MIT, Jesse
Vincent). See `NOTICE.md`.
