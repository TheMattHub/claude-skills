---
runs: 2
model: sonnet
max_turns: 8
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
---

I need a Python script that extracts invoice number, invoice date, total amount and VAT percentage from supplier invoices (the text is already extracted from the PDFs) using an LLM. Users should be able to use a local Ollama or their own API key. Show me the core design and the key code for the call and the parsing, kept short.
