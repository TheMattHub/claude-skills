# Notice

Every file of the skill `subagent-driven-development` derives from the `superpowers` plugin
(https://github.com/obra/superpowers), copyright (c) 2025 Jesse Vincent, MIT licence: `SKILL.md`,
`code-reviewer.md`, `implementer-prompt.md`, `re-review-prompt.md`, `task-reviewer-prompt.md`,
the three files in `scripts/`, and the four files in `references/` (`fix-loop.md` from
upstream's `references/fix-loop.md`; `example-workflow.md`, `model-selection.md` and
`rationalizations.md` were split out of upstream's earlier `SKILL.md`). The licence text is
reproduced below. The skill `coordinating-agent-waves` is original to this plugin, also MIT
licensed.

Changes made in this fork:

- Added "Independent Checks" with `standard`, `oracle` and `proof` tiers, a spec-test agent for
  `oracle` tasks, and a behavioural proof for `proof` tasks.
- Added a checkpoint review after tasks that later tasks build on, and a "Final Review" mandate
  (simpler code, one source of truth, cross-task seams, coordinator commits).
- Capped the per-task fix loop at five rounds with escalation to a more capable model, and
  added "rulings, not stalls": decisions are recorded in a ledger instead of waiting on a human.
- Added the rule to verify an implementer's claims (environment blame, earlier tasks) before acting.
- Moved the fix loop, worked example, rationalisation table and model-selection detail into
  `references/`; copied the review prompt in as `code-reviewer.md`; made references to other
  skills optional.

## MIT License

Copyright (c) 2025 Jesse Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
