# Board: <repo>, <run>

Rules: `peer-sessions.md`. Edit only your own rows; re-read the file before editing; append to
the Log. A message to a peer only says which row changed.

## Sessions

| Session | Role | Branches / worktrees | IDs (bugs, decisions) | Live agents | State |
|---|---|---|---|---|---|
| <name> | integrator | base `<branch>` | 600-650, D590-D599 | 1 | reviewing post-x |
| <name> | producer | post-x (`../repo-x`) | 651-700, D600-D629 | 2 | building |

## Locks

| Lock | Owner | Since | Released when |
|---|---|---|---|
| base | <integrator> | <date time> | post-x fast-forwarded |
| machine | <session> | <date time> | full serial done |

## Authority (the user's words, given to the session that holds it)

| Date | Session | Grant |
|---|---|---|
| <date> | <integrator> | "<quote>" |

## Handoffs

| # | From | To | What | Packet | Waits on | Status |
|---|---|---|---|---|---|---|
| 1 | <producer> | <integrator> | post-x for review and ff | head <sha>, full serial <n> passed, notes <path> | - | open |

## Log

- <date time> <session>: <event>
