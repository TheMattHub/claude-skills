---
runs: 2
model: sonnet
max_turns: 8
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
---

I will be away until tomorrow morning and want four subagents to work on our Python repo in parallel overnight. A refactors the scoring module (touches utils.py), B adds a new export feature (touches utils.py and tests/test_core.py), C fixes three known bugs (one in utils.py), D updates the docs and the CHANGELOG. Write me a plan of how you would organise this work. Do not start any agent and do not change any file; I only want the written plan.
