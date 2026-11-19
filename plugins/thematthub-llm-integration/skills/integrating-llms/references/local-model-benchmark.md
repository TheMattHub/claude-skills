# Choosing a local model: benchmark on your own tasks

The examples come from an app that extracts fields from public funding calls and drafts application answers; the method applies to any document type. A "call" is one funding announcement; "EU" and "IT" mark the issuing portal (European or Italian).

Leaderboards do not predict which model extracts your documents faithfully on the user's laptop. Run a
spike: a throwaway `bench.py` in the scratchpad, not in the repo.

## Method

1. **Tasks = the app's real pipelines**, called through their own functions (e.g. `pipelines.scrape(cfg, url,
   text=...)`, `pipelines.draft(...)`), with each candidate passed as `cfg`. No separate prompts.
2. **Ground truth = records a person already checked** (the worked examples in the repo). Score field by
   field (e.g. 5 key fields → "4/5") plus the cross-check flags (`unverified`).
3. **Record per model and task:** score, wall time, and failure mode (no valid JSON, wrong date shape,
   invented number, ran out of time). Invented facts disqualify, whatever the score.
4. **Run on hardware like the users'**, GPU on and off, with the context length the installer will set
   (`OLLAMA_CONTEXT_LENGTH=16384`). Note the machine in the results.
5. **Try the thinking setting per model** (`reasoning_effort` none / low / model default): runaway reasoning
   was the most common cause of timeouts.
6. **Decide per role:** the fastest faithful model reads and extracts; the most faithful writer drafts. A pair
   usually beats one compromise model.
7. **Record the decision** in the devlog as a table (models × tasks, score and seconds) plus the chosen defaults,
   and put the constants in `llm.py` with a comment pointing at that entry.

## Reference result (2026-09-29, a laptop with a 4 GB GPU, Ollama, 16K context)

| | Gemma 4 E4B (6 GB) | Gemma 4 12B | gpt-oss 20B | Qwen 3.5 9B |
|---|---|---|---|---|
| Extract (EU call) | 3/5, 52 s | 4/5, 192 s | 3/5, 143 s | failed |
| Extract (IT call) | 5/5, 66 s | 4/5, 244 s | 3/5, 141 s | 5/5 but invented a budget |
| Draft (Italian) | failed | faithful, 603 s | invented targets | honest gaps |

Chosen: E4B reads, 12B drafts. Re-run when a new model family ships or the target hardware changes.

## Long agentic studies (multi-turn tool use, hours of attempts)

What went wrong in a 144-attempt study (Gemma via Ollama against headless Claude Code), beyond the method above:

- **The 16K context cuts tool-use loops.** Each turn adds to the transcript; 5 of 22 tool-arm failures were
  replies cut at the window. Report window cuts as a separate outcome, and rerun a sample at 32K.
- **Other work on the machine starves Ollama.** A test suite running at the same time made requests time out
  and the retry loop died. Hand the machine over explicitly ("machine free") or mark results taken under load.
- **Pilot first:** run 1 task per arm, then read every transcript. Here the pilot found three harness bugs
  (arguments sent as a JSON string, a missing argument not named, Windows long paths in the work directory).
- **Isolate the Claude arm:** `claude -p --model <m> --max-turns N --output-format stream-json --verbose
  --strict-mcp-config --mcp-config <only the server under test> --settings <file> --disable-slash-commands
  --no-session-persistence --tools <list>`, run in a throwaway folder. Otherwise the user's skills, MCP
  servers and memory leak into it. Record `total_cost_usd` per attempt.
- **Stop an arm on time, not only on errors:** when its results already point one way and finishing would
  take hours (the 12B arm, stopped at 42 of 72), stop it and say so on the results page, with the count.
