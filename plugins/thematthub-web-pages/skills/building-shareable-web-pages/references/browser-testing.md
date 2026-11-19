# Testing pages in real browsers

## Three layers

1. **Pure script under node.** Export the page's pure functions (layout maths, verdict words, storage
   parsing) from the same script constant the file embeds, run them under `node` with a stub DOM. A test
   checks the written file's script equals that constant.
2. **The written file in a headless browser over the DevTools protocol.** No npm package: start Chrome/Edge
   with `--headless=new --remote-debugging-port=0 --user-data-dir=<tmp>`, read the port from
   `<user-data-dir>/DevToolsActivePort`, talk JSON over the WebSocket (node 22 has `WebSocket`). Random
   fixed ports collided across parallel tests and two tests drove one browser.
3. **Hostile inputs** for each: hostile names, empty data, missing optional fields, huge values, storage
   that throws (`Object.defineProperty(window, 'localStorage', {get(){throw new Error()}})`).

## What to assert in the browser

- No sideways scroll: `document.documentElement.scrollWidth <= innerWidth` at 360 and 1920 px
  (`Emulation.setDeviceMetricsOverride`), both themes (`Emulation.setEmulatedMedia` with
  `prefers-color-scheme`).
- Grid columns per width (1 on a phone).
- No layout shift: record `getBoundingClientRect()` of the transport, tabs and side rows; play, seek, change a
  status; the boxes are equal.
- No console errors (`Runtime.exceptionThrown`, `Log.entryAdded`).
- Workers: `--dump-dom --virtual-time-budget` returns before a worker finishes; drive with the protocol and
  wait on a page condition instead.
- Same numbers as the desktop engine: cells equal; interval bounds to 1e-9 relative (library versions).

## Screenshots

- `--screenshot` with `--window-size` cannot go below the browser's minimum window width: a "360 px" shot is
  cropped wider and suggests overflow that is not there. Use the protocol's device metrics, or measure.
- Shots before and after, both themes, 1440 and 360; look at them, then open the page in the user's own
  browser: users find what headless runs miss.

## Flaky tests

A flaky page test is a race or a load assumption until shown otherwise (a refusal sent before draining the
request body reset the connection; a time estimate measured on a loaded machine). Make the failure say why
(assert the window became active, print the focus widget) before raising a timeout.
