"""One chat call over the user's own AI provider. Copy into the app package and adapt the constants.

Two wire formats cover every supported provider:
  anthropic - Claude via the native Messages API
  openai    - ChatGPT, Ollama, LM Studio, or any OpenAI-compatible server (LLM_BASE_URL)
Plain `requests` instead of vendor SDKs: one dependency for every provider.
Config keys: LLM_PROVIDER, LLM_BASE_URL, LLM_API_KEY, LLM_MODEL, LLM_DRAFT_MODEL, LLM_THINKING,
LLM_MAX_INPUT_CHARS. With none set, the app uses the local pair below on Ollama.
Python 3.9 compatible.
"""
from __future__ import annotations

import json
from urllib.parse import urlparse

import requests

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
# Model names go stale: check the provider's current model list before using this one.
DEFAULT_CLAUDE = "claude-opus-5-5"  # check the claude-api skill for current model ids
# Server-side refusal fallback; only these models accept the parameter (verify with the claude-api skill).
FALLBACK_MODELS = {"claude-opus-5-5", "claude-opus-5", "claude-sonnet-5-5", "claude-fable-5-2", "claude-fable-5-1"}
TIMEOUT = 600  # drafting a long document can take minutes
LOCAL_TIMEOUT = 1800  # a laptop reading a long document on its processor

# Pick these with a benchmark on the app's own tasks (references/local-model-benchmark.md).
LOCAL_URL = "http://localhost:11434/v1"
LOCAL_MODEL = "hf.co/unsloth/gemma-4-E4B-it-GGUF:Q4_K_M"  # reads and extracts, 6 GB
LOCAL_DRAFT_MODEL = "gemma4:12b"  # drafts text faithfully
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}


class LLMError(RuntimeError):
    pass


def clip(text: str, limit: int) -> str:
    # ponytail: hard cut at the input budget; chunk the source if real inputs keep hitting it
    return text if len(text) <= limit else text[:limit] + f"\n\n[…truncated: {len(text) - limit} characters not sent]"


def with_defaults(cfg: dict) -> dict:
    """No provider chosen and no key: the local Ollama pair. A saved key alone means Claude."""
    if cfg.get("LLM_PROVIDER") or cfg.get("LLM_API_KEY"):
        return cfg
    local = {"LLM_PROVIDER": "openai", "LLM_BASE_URL": LOCAL_URL, "LLM_MODEL": LOCAL_MODEL,
             "LLM_DRAFT_MODEL": LOCAL_DRAFT_MODEL}
    return dict(cfg, **{k: v for k, v in local.items() if not cfg.get(k)})


def is_local(cfg: dict) -> bool:
    """A model server on this computer (Ollama, LM Studio): slower, smaller context, no key."""
    return cfg.get("LLM_PROVIDER") == "openai" and urlparse(cfg.get("LLM_BASE_URL") or "").hostname in LOCAL_HOSTS


def for_drafting(cfg: dict) -> dict:
    return dict(cfg, LLM_MODEL=cfg["LLM_DRAFT_MODEL"]) if cfg.get("LLM_DRAFT_MODEL") else cfg


def max_input(cfg: dict) -> int:
    # 40,000 characters (~11K tokens) leave room for instructions and the reply in a 16K local context
    return int(cfg.get("LLM_MAX_INPUT_CHARS") or (40_000 if is_local(cfg) else 150_000))


def configured(cfg: dict) -> bool:
    """An AI provider is set up: a key, or a local OpenAI-compatible server without one."""
    return bool(cfg.get("LLM_API_KEY") or cfg.get("LLM_PROVIDER") == "openai" and cfg.get("LLM_BASE_URL"))


def _anthropic(messages: list, cfg: dict) -> str:
    model = cfg.get("LLM_MODEL") or DEFAULT_CLAUDE
    headers = {"x-api-key": cfg.get("LLM_API_KEY", ""), "anthropic-version": "2023-06-01",
               "content-type": "application/json"}
    body = {"model": model, "max_tokens": 16000,
            "system": "\n\n".join(m["content"] for m in messages if m["role"] == "system"),
            "messages": [m for m in messages if m["role"] != "system"]}
    if model in FALLBACK_MODELS:
        headers["anthropic-beta"] = "server-side-fallback-2026-07-01"
        body["fallbacks"] = "default"
    r = requests.post(cfg.get("LLM_BASE_URL") or ANTHROPIC_URL, headers=headers, json=body, timeout=TIMEOUT)
    if r.status_code >= 400:
        raise LLMError(f"Claude API error {r.status_code}: {r.text[:300]}")
    data = r.json()
    if data.get("stop_reason") == "refusal":
        raise LLMError("The model refused this request")
    if data.get("stop_reason") == "max_tokens":
        raise LLMError("The reply was truncated at the output limit")
    return "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")


def _openai(messages: list, cfg: dict, json_reply: bool = False) -> str:
    base = (cfg.get("LLM_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    headers = {"content-type": "application/json"}
    if cfg.get("LLM_API_KEY"):
        headers["Authorization"] = f"Bearer {cfg['LLM_API_KEY']}"
    # No token limit sent: providers disagree on max_tokens vs max_completion_tokens, and their defaults suffice.
    if not cfg.get("LLM_MODEL"):
        raise LLMError("Set a model name in Settings (e.g. the one shown by your provider or `ollama list`)")
    body = {"model": cfg["LLM_MODEL"], "messages": messages}
    local, host = is_local(cfg), urlparse(base).hostname or ""
    if local and cfg.get("LLM_THINKING", "none") != "model":
        # Local thinking models otherwise reason for thousands of tokens before answering (one ran 30 minutes
        # on one call). "none" suits Gemma and Qwen; gpt-oss only accepts low/medium/high.
        body["reasoning_effort"] = cfg.get("LLM_THINKING") or "none"
    if json_reply and (urlparse(base).port == 11434 or host.endswith("ollama.com")):
        body["response_format"] = {"type": "json_object"}  # Ollama only: LM Studio rejects json_object
    try:
        r = requests.post(base + "/chat/completions", headers=headers, json=body,
                          timeout=LOCAL_TIMEOUT if local else TIMEOUT)
    except requests.ConnectionError:
        if local:
            raise LLMError(f"The local AI at {base} is not answering. Start Ollama (or LM Studio), or choose "
                           "another provider in Settings.")
        raise
    if r.status_code >= 400:
        raise LLMError(f"AI provider error {r.status_code}: {r.text[:300]}")
    return r.json()["choices"][0]["message"]["content"] or ""


def chat(messages: list, cfg: dict, json_reply: bool = False) -> str:
    if cfg.get("LLM_PROVIDER", "anthropic") == "anthropic":
        return _anthropic(messages, cfg)
    return _openai(messages, cfg, json_reply)


def _first_json(text: str):
    dec = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch in "{[":
            try:
                return dec.raw_decode(text, i)[0]
            except ValueError:
                continue
    raise ValueError("no JSON object found in the reply")


def chat_json(messages: list, cfg: dict, check=None):
    """Chat, parse the first JSON value in the reply, run check(data) -> [errors]; one corrective retry."""
    messages = list(messages)
    for attempt in range(2):
        reply = chat(messages, cfg, json_reply=True)
        try:
            data = _first_json(reply)
            errs = check(data) if check else []
        except ValueError as e:
            errs = [str(e)]
        if not errs:
            return data
        messages += [{"role": "assistant", "content": reply},
                     {"role": "user", "content": "Your reply has these problems:\n- " + "\n- ".join(errs)
                      + "\nReply again with the corrected JSON only."}]
    raise LLMError("The AI reply was not valid after one retry: " + "; ".join(errs))
