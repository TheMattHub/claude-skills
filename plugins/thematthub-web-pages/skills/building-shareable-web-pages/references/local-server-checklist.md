# A local server a browser page talks to

Any website the person has open can send requests to 127.0.0.1. A page's control server needs all of:

- Bind `127.0.0.1` on port 0; print the URL with flush; one writer process per data folder.
- A random token in the first URL, moved to an `HttpOnly; SameSite=Strict` cookie, then stripped from the
  address bar (redirect).
- `Host` must be loopback (DNS rebinding); every POST needs a matching `Origin` and
  `Content-Type: application/json` (a `text/plain` form post is the classic bypass); no CORS headers at all.
- Headers: `Referrer-Policy: no-referrer`, `X-Content-Type-Options: nosniff`, `Cache-Control: no-store`, a
  CSP on every HTML response; served user files under `Content-Security-Policy: sandbox`.
- Files confined by resolved path: `..`, symlinks, Windows `::$DATA`, device names (`CON`), trailing dots
  and spaces.
- Request hygiene: cap the body size; reject a negative `Content-Length`; read (drain) the body before a
  refusal (Windows resets the connection otherwise, which looks like a flaky test); guard logging of a
  request line over 64 kB.
- The token never goes to disk, into the page, into logs, or into an assistant's tool results; the server
  redacts API keys from streamed text and errors.
- HTML inserted by the shell (e.g. rendered Markdown) drops `javascript:` URLs and `on*` attributes; better,
  build it from text nodes.
- A plain fallback when a capability is missing (no key: the buttons copy text for the user to paste).

Review: an attacking pass before shipping, run against a real server: foreign Host, no Origin, text/plain
POST, `..` and `::$DATA` paths, a symlink, a negative length, a hostile reply; then attack again after the
fixes.
