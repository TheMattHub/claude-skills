---
runs: 2
model: sonnet
max_turns: 8
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
---

I run a 3-day hands-on Python data course for analysts at a manufacturing company. They will work alone on their own Windows laptops, without administrator rights. Please write the "Day 1: set up your laptop" section of the participant guide. The setup is: install git and the uv Python tool, clone the course repository (github.com/acme-training/data-course), run `uv sync`, then run `uv run python check_setup.py`, which prints a short report. Participants open the guide on their own the evening before and cannot reach me until the course starts.
