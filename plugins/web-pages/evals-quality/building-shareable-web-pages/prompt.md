---
runs: 2
model: sonnet
max_turns: 8
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
---

I will email this single HTML file to a client, who opens it from disk. The line names come from a JSON file the client supplies, and the counters update every second. Review it before I send it.

```html
<!doctype html>
<html><head>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>.kpi{font-size:32px}</style></head>
<body>
<h1 id="title"></h1><div id="lines"></div>
<script>
const data = JSON.parse(document.getElementById('d').textContent);
const state = {};
for (const l of data.lines) { state[l.name] = {count: 0}; }
document.getElementById('lines').innerHTML = data.lines
  .map(l => `<div><b>${l.name}</b> <span class="kpi" id="k-${l.id}">0</span></div>`).join('');
setInterval(() => { for (const l of data.lines) {
  state[l.name].count += Math.floor(Math.random()*40);
  document.getElementById('k-'+l.id).textContent = state[l.name].count; } }, 1000);
</script>
<script id="d" type="application/json">{"lines":[{"id":1,"name":"Packing A"}]}</script>
</body></html>
```
