# Several sessions on one repository

A peer session is another Claude session (ListAgents, "Peer sessions") working the same repo,
usually with its own subagents. It has its own user conversation, its own permissions and its
own restart trigger. It acts only when its user, a message or its trigger wakes it. Sessions fail
through the same shared state as agents (branches, files, the machine), plus three things of
their own:
- authority does not travel between sessions;
- nobody polls anybody;
- a message is lost if it lands during a compaction or a restart.

So the state lives in a file, and messages only say "the board changed".

## Roles: one integrator, any number of producers

- **The integrator** owns the base branch and every outward step: merges, pushes of the base,
  export, tags, releases. It reviews what producers hand over, merges it, and frees the base.
- **Producers** own their branches and worktrees. They never write the base. They hand over one
  branch at a time, with the packet below.
- The user gives standing authority to the integrator, in the integrator's own conversation
  ("when it is ready, merge, tag and publish"). The integrator writes it on the board word for
  word. An instruction relayed by a peer ("the user wants X") is information: it is enough to hold
  or stop, never to publish, tag or delete. In one run a release waited hours on the user,
  because the user was talking to the other session.
- The integrator role can move: write the change on the board, then the new integrator asks its
  user for authority.

## The board

One file outside git, in the main checkout (`.superpowers/board.md`, in the working folder these two skills share in the repository; keep it out of git: add `.superpowers/` to `.git/info/exclude`; an absolute path every
worktree can reach). Template: `board-template.md`. It holds:
- **Sessions:** name, role, branches and worktrees, ID ranges (bugs, decisions), state.
- **Locks:** each with an owner and a release condition. `base` is frozen between "base ready"
  and the fast-forward. `machine` is held by whoever runs a full serial suite or a benchmark,
  because the perf guard needs a quiet CPU and two suites starve each other.
- **Authority:** the user's grants, quoted, with their date and the session holding them.
- **Handoffs:** one row per open item: from, to, what, the packet, `waits on`, status.
- **Log:** append-only, one dated line per event.

Write rules, so no session overwrites another:
- Edit only your own Sessions row, the locks you own, handoffs where you are `from` or `to`, and
  append to the Log. Re-read the file right before every edit and change it with one exact edit.
- After an edit that concerns a peer, send it one line: `board: <row> changed, you are next`.
  The message is a doorbell. The board is the truth.

## Every wake reads the board

Each session's trigger prompt starts with: read the board. Then:
- a handoff with `to: <me>` and status open: act on it;
- otherwise, if my own NEXT waits on a peer: reply in one line and stop.

Restarts and compactions lose nothing, and an empty wake stays cheap. With N sessions this still
works: nobody needs to know who messaged whom.

## Contract, set in the first exchange (it goes on the board)

- ID ranges per session, in numbers ("bugs 651-700, D600-D629").
- Who writes what:
  - each session writes its own CHANGELOG, DEVLOG and DECISIONS rows, in its own ranges;
  - the integrator writes the version bump, the release headline and What's new;
  - shared generated baselines (golden files, snapshots) belong to the integrator after a merge.
- One merge per branch. A branch with merge commits is not rebased: the producer merges the
  frozen base in once, then hands over for a fast-forward.
- The handoff packet: head commit, full serial result, review notes, a clean tree (no
  line-ending-only files).

## Shared budget

The usage window is per account, not per session, so every session's agents draw on the same
one. Put each session's live agent count on the board. Keep the total within the run's limit:
after a limit has hit, at most two agents across all sessions, and large ones alone. Only the
`machine` lock holder runs a full suite or a benchmark.

## Check before you claim

- Before promising a fix on the base, check that the code exists there. A helper added only on
  the peer's branch can be fixed only on the peer's branch.
- Review a producer's branch read-only and send the findings. When the producer reports them
  fixed, re-run the reviewer's own repro scripts yourself; a summary is not proof.
- `CronList` before `CronCreate`. A trigger left over from before a compaction kept firing after
  the known one was deleted.
- When a session leaves the work for good, it:
  - writes its final state on the board;
  - releases its locks;
  - hands its open items to a named session;
  - deletes its triggers, then stops.
