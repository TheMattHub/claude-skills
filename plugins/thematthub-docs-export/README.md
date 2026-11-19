# thematthub-docs-export

Turns a project's markdown documentation into a Word file, a PDF or both. Mermaid diagrams become images, and optional templates (a Word letterhead, a LaTeX class) give the output your organisation's look. Without templates you get plain, working exports.

## Requirements

A Word export needs only PowerShell 7 and Pandoc; PDF and Mermaid diagrams need the rest.

| Tool | Install on Windows | Needed for |
| --- | --- | --- |
| PowerShell 7 | `winget install Microsoft.PowerShell` | running the script (always) |
| Pandoc 3.8 or later (tested with 3.12; the script uses `--syntax-highlighting`, added in 3.8) | `winget install JohnMacFarlane.Pandoc` | every export |
| Node.js and Mermaid CLI (`mmdc`) | `winget install OpenJS.NodeJS`, then `$env:PUPPETEER_SKIP_DOWNLOAD = "1"; npm install -g @mermaid-js/mermaid-cli` (the script uses the installed Edge or Chrome, so Chromium is not downloaded) | documents with a Mermaid block; others export without them |
| Microsoft Edge or Google Chrome | already on most Windows machines | rendering Mermaid diagrams |
| A LaTeX distribution providing `pdflatex` and `xelatex` | `winget install MiKTeX.MiKTeX` | PDF output only (`pdflatex` with a `pandocTemplate`, `xelatex` without) |
| Poppler (`pdftotext`, `pdffonts`) | `winget install oschwartz10612.Poppler` | the searchable-PDF checks after exporting |

The script is written for Windows; on macOS or Linux PowerShell 7 runs it, but several parts assume Windows (the default config path, the PATH refresh, the `;` path separator passed to pandoc, the browser lookup), so it is not supported there.

## What it reads, writes and runs

I checked this against `skills/exporting-docs/scripts/export-docs.ps1`.

- **Reads:** the project's markdown files (by default `README.md`, `HANDBOOK.md`, `CONCEPTUAL_MODEL.md`, `RESOURCES.md`, `EXPERIMENTS.md` and `DEVLOG.md`, or the files you name), images those files link to, the optional revisions file you name, `~/.claude/docs-export.json`, and the template files named there. It also reads the machine and user `PATH` to find tools, checks whether Edge or Chrome is installed, and asks `git` for your configured user name.
- **Runs:** `pandoc`, `pdflatex` or `xelatex` (PDF only), and the Mermaid CLI `mmdc` (only when a document has a Mermaid block), which starts your installed Edge or Chrome in the background to draw the diagram.
- **Writes:** an `export` folder in the project holding the `.docx` and `.pdf` files, and a `.build` folder inside it with intermediate files (combined markdown, diagram images, copied images, the unpacked LaTeX template, LaTeX logs). The `.build` folder is deleted and recreated on each run. Nothing is written outside the project except what the tools themselves do.
- **Does not:** download or install anything, or send data over the network. A missing tool stops the script with the install command for you to run yourself.

Because `DEVLOG.md` is in the default list, name the files with `-Files` when exporting for someone outside the team.

## Settings

Optional, in `~/.claude/docs-export.json`:

```json
{
  "wordTemplate": "C:\\path\\to\\letterhead.docx",
  "latexTemplate": "C:\\path\\to\\latex-class.zip",
  "pandocTemplate": "C:\\path\\to\\bridge.latex"
}
```

Write Windows paths with backslashes doubled, or use forward slashes (JSON does not accept a single backslash).

- `wordTemplate`: a `.docx` whose header, footer and styles the Word output takes.
- `latexTemplate`: a folder or zip with your LaTeX class.
- `pandocTemplate`: a pandoc template that loads that class. Required with `latexTemplate`; allowed alone. `skills/exporting-docs/templates/example-bridge.latex` is a starting point.

## Example

> Export the project's documentation to Word and PDF for the client Acme.

## Install

```
/plugin install thematthub-docs-export --marketplace TheMattHub/claude-skills
```
