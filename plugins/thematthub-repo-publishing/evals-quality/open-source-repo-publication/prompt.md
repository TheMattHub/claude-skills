---
runs: 2
model: sonnet
max_turns: 8
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
---

Our team has an internal tool repo (remote is github.com/acme-corp/line-planner, three years of history, README says "internal use only"). A data/ folder with customer exports was added to .gitignore last year, and the app auto-commits snapshots of its state to git. I want to make it public next week as open source. What steps would you take, in order?
