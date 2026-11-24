---
runs: 2
model: sonnet
max_turns: 8
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
---

We have a written implementation plan with six independent tasks for a Python project: (1) a parser for supplier files, (2) a scoring engine that computes the ranking other modules use, (3) CLI wiring, (4) docs, (5) a config loader, (6) a refactor of the exporter that must not change its output. Describe in writing how you would execute this plan with subagents in this session: what each subagent is given, what review each task gets, what extra checks you add and how it ends. Do not start any agent and do not change any file; I only want the written plan.
