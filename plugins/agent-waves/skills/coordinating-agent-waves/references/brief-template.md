# Agent brief template

Every slot marked REQUIRED appears in every implementation brief. Copy, fill, send.

```text
[REQUIRED goal] Implement <item> (<one line>) of <plan/spec path> in <repo path>, branch <branch>.
[REQUIRED isolation] Worktree: FIRST `git merge --ff-only <branch>`; work and commit only here;
  set PYTHONPATH=<worktree root> for every command and print <pkg>.__file__ once.
  (Shared tree instead: commit by explicit path only.)
[REQUIRED commands] Interpreter <path>; env <vars>; EVERY command under a hard `timeout N`.
[REQUIRED map] Code involved, from exploration: <file:line -> what>, ... (verify line numbers).
[REQUIRED scope] Change <what>. Behaviour: <identical | only these fixes>.
[REQUIRED ownership] You own <files>. Do NOT edit <files> (owned by <agent/item>).
[REQUIRED shared files] Do not edit <changelog/plan>; report entry text. Bug IDs: <pre-assigned>.
  New bug: xfail(strict) test citing the ID first, then fix, then remove the marker.
[REQUIRED proof] Fast suite green; fingerprint `<command>` identical to <baseline> (cmp);
  <differential | snapshot | docs regeneration without diff>. Full suite: not per agent.
[REQUIRED commit] <one per item>, message "<prefix>: ..." ending "<attribution>". Do not push.
[REQUIRED report] Files and line counts; decisions and ambiguities resolved (specific enough to
  check tests against); what was left and why; proof results with timings; changelog text.
```

Oracle brief: add "Do not read the implementation in progress; expected values from the spec and
hand derivation only; state assumptions in docstrings; the file must collect before the
implementation exists."

Review brief: list the commits; the goal (simpler code, one source of truth); each suspected
over-engineering or bug by name; the bug protocol; permission to replace clever code with plain code.
