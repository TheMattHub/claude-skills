# Example console palette (2026-10-22)

Validated with the dataviz skill's `validate_palette.js`. Status colours are exempt from the series
lightness/chroma bands by design (they always carry a word or icon).

| Role | Light | Dark (slate blue) |
|---|---|---|
| bg | `#f4f6fa` | `#151b26` |
| panel | `#ffffff` | `#1c2331` |
| raised | `#eef1f6` | `#242d3e` |
| line | `#dde2ea` | `#313c51` |
| text | `#1a1f2b` (16.5:1) | `#e6ebf3` (13.2:1) |
| muted | `#586377` (6.1:1) | `#9aa6b8` (6.4:1) |
| dim | `#6b7588` (4.6:1) | `#76839a` (4.1:1, non-essential only) |
| accent (buttons, links) | `#2f6fe0` (white text 4.7:1) | `#2f6fe0` |
| series 1 ("yours") | `#2f6fe0` | `#4a8af4` |
| series 2 (baseline) | `#c56a12` | `#d47a24` |
| series 3 | `#0e8c7e` | `#16a08f` |
| status running (quiet) | `#0a8a78` | `#2fa58f` |
| status blocked / full | `#c99400` + word | `#d39a2e` + word |
| status down | `#d23f4a` + word/icon | `#ef5f57` + word/icon |
| status idle | `#6b7588` | `#76839a` |

Series results: light `#2f6fe0,#c56a12,#0e8c7e` all PASS (`--pairs all`, worst CVD Delta E 11.9);
dark `#4a8af4,#d47a24,#16a08f` all PASS (worst 12.7). The rejected blue/violet pair
(`#5b9bff,#ac94fa`) measured Delta E 0.9 under protanopia.

Other tones tried for the dark base: graphite `#1c1e22` (neutral), navy `#0f1524` (deeper);
slate blue was picked because the blue accent then belongs to the surface.
