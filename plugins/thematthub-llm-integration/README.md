# thematthub-llm-integration

One skill for adding language-model calls to an app or script.

- **integrating-llms**: guides provider-neutral LLM calls (Claude, OpenAI, Ollama, LM Studio or any OpenAI-compatible server), bring-your-own-key or local models, structured JSON extraction, local-model choice, and debugging hangs, timeouts and invalid JSON.

Example request: "Add an AI feature to my script that extracts invoice fields as JSON, and let users run a local model."

## Requirements

Python 3.9+ for the reference files (`references/llm.py`, `references/fake_llm.py`) the skill copies into your project. `llm.py` uses the `requests` package. Nothing is tied to one operating system.

## What it reads, writes and runs

- Instructions plus two Python reference files, `llm.py` (the model-call module) and `fake_llm.py` (a fake server for tests). They are examples for you to copy into your own app; the plugin does not run them.
- Claude may copy and adapt them in your project when you ask, and may run your project's tests, under your normal Claude Code permissions.
- The plugin itself makes no network calls. In the app you build, API keys come from your own configuration or environment variables and are sent only to the provider you choose. Model names in the files can go stale, so check your provider's current list.

## Install

```text
/plugin install thematthub-llm-integration --marketplace TheMattHub/claude-skills
```
