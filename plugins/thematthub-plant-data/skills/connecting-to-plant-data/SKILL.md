---
name: connecting-to-plant-data
description: "Use when an app, simulation or digital twin reads live data from a plant or industrial system - OPC UA, MQTT, Sparkplug B, REST, MES or SQL tables, historians, PLC tag servers (Emulate3D, Kepware) - or sends recommendations, setpoints or commands back to one; when a model file, config or LLM tool would name a host, credential or query; or when reviewing such a connector for security."
---

# Connecting to plant data

## Overview

A plant connector is an I/O surface that an untrusted file or an LLM will try to steer.
Principle: **permission is the caller's, never the file's.** The file names a connection; the
operator who starts the process defines what that connection is. The generic rules (TLS on, read
only, fakes in tests, optional extras) are assumed. This skill covers the parts that are easy to
get wrong.

**What this skill assumes.** An app or simulation (for example a digital twin, which repeats a "twin cycle": read plant data, update the model) whose configuration lives in a "model file" that may be shared or written by someone else, and which reads plant systems through connector code and may write recommendations back. The simulation core is the part that computes the model; it never talks to the plant directly. Names like `Secret` and `changes(source, cursor)` are suggested shapes for your own code, not an existing library.

## Where things are defined

| Thing | Lives in | Never in |
|---|---|---|
| Host, port, URL, DSN, query | Operator's connections file (start flag) or the app's dialog | Model file, agent tool argument |
| Credential | A `Secret` resolved from the environment or the OS store; `repr` prints `<secret>` | URL, model file, logs, error text, pickles |
| Env vars a model file may read | A fixed prefix allow-list (e.g. `APP_DATA_*`) | Any other name; no `${NAME}` expansion for live sources |
| Which nodes/topics/tables | Model file, by connection name | Anywhere that also chooses the host |

Agent surfaces (MCP, assistant) get **no tool and no parameter** for connections: they come from
the server's start flag only. Keep a test that walks every tool schema and fails on one.

## Connecting

- Resolve the name once, vet every address, then connect **to the vetted address**, with TLS
  checked against the host name. Resolving again at connect time opens a DNS-rebinding hole.
- No redirects (a redirect is an error), no proxies, and no setting that turns verification off.
- A credential over an unencrypted channel is refused unless every address is loopback. **No
  override**: plants run MQTT 1883 and OPC UA "None" by habit; the operator adds TLS.
- Prefer the stdlib for small protocols (REST GET via `http.client` on the pinned socket). Use a library only when
  the protocol is too big to write (OPC UA: `asyncua`), as an optional extra, licence checked
  (asyncua is LGPL-3.0), limits set through its **public** settings (`max_messagesize`,
  `max_chunkcount`). Many MQTT libraries resolve the host themselves and read a packet of any
  declared size: check that, or write a subscribe-only client.

## Reading

- **Bound before parsing.** Read the declared length and refuse an oversized message before you
  allocate memory for it. Every size, count, rate and time has a ceiling in code; over it is
  dropped and counted, never grown. The operator may lower a bound below its ceiling; a model or tool may not.
- **One pull contract for pollers and subscriptions:** `changes(source, cursor) ->` events
  `(source, key, value, source_time, received, seq)` in receipt order, delivered at least once,
  with an exact `lost` count and a `gap` flag. An event **asserts a state, never an
  increment**, so applying it twice is harmless. A latest-value store hides losses: don't.
- A subscription runs in one daemon thread owned by whoever runs the twin cycle. The simulation
  core never imports a connector, and no connector calls into a run.
- **Values are data:** scalars into numeric and boolean targets only. Plant text never becomes an
  expression, path, block name or anything that selects code.
- Timestamps: normalise to UTC. Report naive timestamps, don't guess their zone. Keep source time
  and received time both.

## Writing back

- Sparkplug B **rebirth requests are commands** to an edge node: never send one. A node that
  publishes by alias then shows no values until its next birth; document that, don't fix it.
- Recommendations leave only as records in an **outbox the operator configured** (a file or
  queue they own): never setpoints, method calls or publishes. A record has a closed vocabulary,
  a content-hash id of the proposal (model, scenario, state, seed, action, KPI, horizon) so
  at-least-once delivery is idempotent, an expiry, the expected effect with its interval, and
  where it came from.
- Feedback is read like a feed. The observed effect is measured from the plant's own data, never
  taken from the reply.

## Review before shipping

Every new I/O surface gets a security review that attacks it: a hostile model file, a hostile
server (oversized frames, redirects, rebinding, endless streams), a hostile LLM. Re-attack after
the fixes. Test the encrypted modes for real against a loopback server (an asyncua server, a
local broker), not only the plain ones.

## Common mistakes

| Mistake | Fix |
|---|---|
| "Handle rebirth" in the MQTT client | Never send it; it is a write |
| Latest-value dict between connector and twin | Event log with cursor, `lost`, `gap` |
| Timeout per read, not per request | One deadline for the whole request |
| An MES adapter per system | One table adapter over `rows(table)`; a missing table reads empty |
| Library private internals to cap sizes | Its public limits; a server that acknowledges none, or a library that does not say, gets one warning and is still read (the operator chose it) |
