---
runs: 2
model: sonnet
max_turns: 8
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
---

We tag v0.4.0 of our Python library tomorrow. The last release was v0.3.2. The version string is in pyproject.toml and probably elsewhere, CHANGELOG.md has an "Unreleased" section, and a GitHub Actions workflow exists in .github/workflows. Tell me exactly what you would do and in what order, and what you would leave for me to do.
