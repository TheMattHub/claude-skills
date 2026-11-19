---
type: llm
---

Judge the final answer against these observable criteria.

1. The prompt or schema lets the model return null for a field it cannot find, and tells it not to guess.
2. The code checks in plain code that each extracted date, amount and percentage actually appears in the invoice text, and flags mismatches for a person instead of silently accepting them.
3. The invoice text is wrapped in delimiters and the system prompt says instructions inside it are to be ignored (it is treated as untrusted data).
4. JSON parsing tolerates prose or code fences around the reply, and on a validation failure the code retries once with the validation errors included.
5. Long input is clipped at a stated character limit with a visible marker that text was not sent, and the code handles an unreachable local server with a message the user can act on.

PASS if at least 4 of the 5 criteria hold. FAIL otherwise. Name the criteria that failed.
