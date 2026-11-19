---
runs: 1
model: sonnet
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Glob, Grep, Skill]
---

My app calls a local Ollama model to extract JSON from invoices and it keeps hanging. What are the first things to check? Short answer.
