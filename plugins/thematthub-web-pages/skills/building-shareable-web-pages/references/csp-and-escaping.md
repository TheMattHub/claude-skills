# CSP, escaping and frames for a self-contained page

## The page shape

```html
<!doctype html><html><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'sha256-<S1>' 'sha256-<S2>'; style-src 'sha256-<C1>'; img-src data:; base-uri 'none'; form-action 'none'">
<script id="theme-pick">/* sets data-theme from storage before paint, in try/catch */</script>
<style>/* one sheet, CSS variables per theme */</style>
</head><body>...static markup...
<script type="application/json" id="data">{ escaped JSON }</script>
<script>/* constant code: reads #data, draws with textContent / canvas */</script>
</body></html>
```

- The code never changes per build; only `#data` does. Anything per-build inside a pinned script changes
  its hash and the page refuses to run (a mail gateway that rewrites the file blanks it: accepted).
- Escape the JSON block: replace `<` with `<`, `>` with `>`, `&` with `&`, `/` with `\/`
  (so `</script>` cannot close the block). Read it with `JSON.parse(el.textContent)`.
- Hash: `base64(sha256(exact bytes between the tags))`; compute it from the same string you write.
- Per-element styling goes through CSSOM (`el.style.left = ...`), which a hash-only `style-src` allows;
  no `style=` or `on*=` attributes in markup.
- Static test on the written file: every `<script>`/`<style>` body's hash is in the policy; the code has no
  `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, `new Function`, `fetch`,
  `XMLHttpRequest`, `WebSocket`, `EventSource`, `navigator.sendBeacon`, no `//host` URLs, no `<a download>`
  unless intended.
- Hostile-name test: data whose names are `constructor`, `__proto__`, `toString`, `</script>`, a 10 kB
  string, RTL text; the page draws and no prototype is polluted.

## Frames

- `<iframe sandbox="allow-scripts" srcdoc="...">` gives an opaque origin: it cannot read the parent, the
  parent's storage or cookies; its own `localStorage` throws (catch it; pass the theme in as an attribute).
- The parent's CSP must list the frame's script and style hashes (srcdoc inherits the policy).
- Theme changes inside the frame need either a reload of `srcdoc` (simple, loses the frame's playhead) or a
  `postMessage` protocol (more code).

## What a policy does not cover (measured)

- Chrome/Edge open an empty TCP connection when a frame navigates to an address, even when blocked.
- WebRTC can leave under any CSP; a worker can use `indexedDB`.
- Firefox does not apply CSP to `file:` reads; a `data:` module worker is the one worker kind that cannot
  read a neighbouring file there.
- So "this page sends nothing" is a test with a canary HTTP server and the driver attached to every target
  (`Target.setAutoAttach`), plus the static API test above.

## Opened from disk

- Chrome, Edge and WebKit block reading a neighbouring file from a `file:` page (Firefox allows it). A "live"
  page is therefore the whole file rewritten atomically (temp file + rename) with `<meta http-equiv=refresh>`
  at about half the data cadence (1 to 30 s); a failed write leaves the old file whole; the reload keeps
  scroll position.
