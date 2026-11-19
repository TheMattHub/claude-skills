# Development log

## Current status

Version 0.1.0 of every plugin kept in this repository (`docs-export`: 0.2.0).

| Plugin | Skills |
| --- | --- |
| writing-toolkit | writing-self-contained-text, writing-course-handbooks, writing-docs-sites, writing-research-papers, writing-italian, analysing-competitors |
| repo-publishing | open-source-repo-publication, releasing-a-repo |
| web-pages | building-shareable-web-pages, choosing-ui-colours |
| docs-export | exporting-docs |
| plant-data | connecting-to-plant-data |
| llm-integration | integrating-llms |

`decks` and `naga` are listed in the marketplace from their own repositories
(`TheMattHub/decks`; the `simulation-study` skill folder of `TheMattHub/naga`, with the engine's MCP
server declared in the marketplace entry).

## Checks

- `python -I tools/check_repo.py`: structure, description and length limits, dead links,
  personal or machine-specific content. Run before every push.
- `claude plugin validate . --strict`: manifest schema.
- `claude plugin eval plugins/<name> --ablation none -j 4`: does each skill load on a matching
  request and stay out of an unrelated one. Each case is a billed model run, so run a suite
  when that plugin's descriptions change, not on every commit.

## Bug register

IDs are stable; prefix `MK`.

| ID | Found | What | State |
| --- | --- | --- | --- |
| MK-1 | 2026-11-19, evals | `analysing-competitors` and `open-source-repo-publication` did not load on question-style requests ("what should I check before...") in 0 of 3 runs | fixed: descriptions now name that kind of request; 3 of 3 |
| MK-2 | 2026-11-19, review | `subagent-driven-development` told the reader to run its scripts "from this skill's directory", which fails for a plugin install | fixed: scripts are called by absolute path from the repository working tree |
| MK-3 | 2026-11-19, review | `NOTICE.md` in the agent-waves plugin (since moved out) listed only part of the files derived from the superpowers plugin | fixed |
| MK-4 | 2026-11-19, review | Two credits to a third-party repository had been removed during packaging | fixed: credits restored |

## Log

- 2026-11-19: first build. Skills packaged from working copies, personal and project-specific
  content removed, trigger evals written and run (22 cases), whole-repository review applied.
- 2026-11-19: `thematthub-docs-export` added with configurable templates (no company template shipped);
  a company-only plugin moved out of this repository; repository named `claude-skills`.
- 2026-11-19: plugins renamed with the `thematthub-` prefix (directory names are global and permanent), icons added,
  with/without quality evals added (`evals-quality/`), an experimental plugin delisted.
- 2026-11-19: final review applied (cleanup script links processes by whole folder names and
  refuses wide roots; stopping any process asks first; plant write rule made absolute; model ids
  updated). `decks` listed as `thematthub-decks`; `thematthub-naga` added; `renames` map added
  for the names published in the first release.
- 2026-11-19: the agent-waves plugin moved out of this repository to a private one; both of its
  published names map to `null` in `renames`. Icons for the two listings that live in other
  repositories are kept in `icons/` and shown in the README table.
- 2026-11-19: decided not to submit to Anthropic's directory (it accepts scripts only from Verified
  organisations, and three plugins ship scripts). The `thematthub-` prefix existed only for that
  directory, so the plugins are back to their plain names; `renames` maps the prefixed names to them.
