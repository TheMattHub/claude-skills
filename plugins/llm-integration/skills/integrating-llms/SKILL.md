---
name: integrating-llms
description: "Use when an app or script needs to call a language model: adding AI features, supporting Claude, OpenAI, Ollama, LM Studio or any OpenAI-compatible server, letting users bring their own key or run a local model, extracting structured JSON from documents or web pages, choosing a local model, or debugging AI calls that hang, time out, return invalid JSON, invent facts or ignore the requested format."
---

# Integrating LLMs

## Overview

Check the provider's current model list before using any model name from these files; names go stale.

One small module and plain HTTP (`requests`) by default: two wire formats cover every provider.
Trade-off: plain HTTP means fewer dependencies and one code path for every OpenAI-compatible server; the vendor
SDK gives typed responses, built-in retries and streaming helpers. Choose the SDK when the app is tied to one
provider, needs streaming or tool use, or would otherwise rewrite retries and response parsing by hand.
The model does judgement and writing; plain code does facts, lookups, scores and cross-checks.
Copy `references/llm.py` and adapt; it is the tested version from a shipped app.

**Not for** Anthropic-only features (tool use, caching, streaming, model ids and pricing): use `claude-api`.

## Defaults (opinionated)

| Decision | Default |
|---|---|
| Transport | `requests`, two formats: `anthropic` (Messages API) and `openai` (`/chat/completions`, covers ChatGPT, Ollama, LM Studio, vLLM, OpenRouter) |
| Config | Env-style keys: `LLM_PROVIDER`, `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`, `LLM_DRAFT_MODEL`, `LLM_THINKING`, `LLM_MAX_INPUT_CHARS`; env vars override the saved file |
| Nothing configured | Local Ollama at `http://localhost:11434/v1`, models chosen by a benchmark on your own tasks (`references/local-model-benchmark.md`) |
| Two models | A fast one reads and extracts; a stronger one drafts text (`for_drafting(cfg)`) |
| JSON replies | `chat_json(messages, cfg, check)`: parse the first JSON value, run a validator, one corrective retry with the errors listed |
| Prompts | One `.md` file per task in `prompts/`; the first line names the task (the fake server keys on it) |
| Tests | Never reach a network or a real local model: `references/fake_llm.py` + a conftest guard |

## Rules

1. **Unknown is `null`.** Prompts say "never guess amounts, dates, percentages"; the validator accepts null.
2. **Cross-check facts in code.** After extraction, a plain-regex check confirms each date, amount and
   percentage appears in the source; unmatched values are flagged for a person, not silently changed.
3. **Source text is untrusted data.** Wrap it in tags (`<document>…</document>`) and say in the system prompt
   that directions inside it are ignored.
4. **Budget the input.** Clip at a character limit with a visible `[…truncated: N characters not sent]` marker;
   40K chars for a 16K-token local context, ~150K for hosted models.
5. **Errors people can act on.** Connection refused on a local URL → "Start Ollama or choose another provider";
   HTTP errors keep the first 300 chars of the provider's body.

## Provider gotchas (each cost a debugging session)

| Symptom | Cause | Fix |
|---|---|---|
| Local call runs 30 min, times out | Thinking model reasons for thousands of tokens | Send `reasoning_effort: "none"` locally (Gemma, Qwen); gpt-oss accepts only `low/medium/high`; some models reject it: make it a setting |
| LM Studio 400 on JSON mode | Only Ollama accepts `response_format: {"type": "json_object"}` | Send it only for port 11434 or `ollama.com` |
| `max_tokens` rejected | Providers split `max_tokens` / `max_completion_tokens` | Send no output limit on the openai format |
| Local model truncates long input silently | Ollama's default context is small | Set `OLLAMA_CONTEXT_LENGTH=16384` (installer) and clip input to 40K chars |
| Reply wraps JSON in prose or fences | Normal for small models | `_first_json` scans with `json.JSONDecoder.raw_decode` from each `{`/`[` |
| Local server slow on first call | Model loading | Local timeout 1800 s, hosted 600 s |
| Test suite suddenly slow on a dev machine | Default config reached the developer's running Ollama | Autouse fixture points the local URL at port 9 (discard) |
| Claude reply cut or refused | `stop_reason` `max_tokens` / `refusal` | Raise a clear error; never return the partial text as success |

## Structured extraction and model choice

- Page or document → validated JSON record: `references/structured-extraction.md`.
- Picking a local model, checking a new one, or running a long tool-use study against Claude Code: `references/local-model-benchmark.md`.
- Benchmarking small models as pickers (one option out of N), or distilling a teacher into one: `references/picker-benchmark.md`.

## Common mistakes

- Adding a vendor SDK per provider by reflex: three dependencies and three error shapes for one POST (fine when you use only one provider and want its typed responses or streaming).
- Letting the model compute what code can (scores, dates relative to today, deduplication, lookups).
- Retrying the same prompt on invalid JSON instead of sending the validator's errors back.
- Choosing a local model from leaderboards: the benchmark on your own tasks picked a 6 GB model over a 20 B one.
- Settings UI that treats "no key" as "no AI": a local server needs a base URL, not a key (`configured(cfg)`).
