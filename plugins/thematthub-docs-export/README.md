# thematthub-docs-export

Turns a project's markdown documentation into a Word file, a PDF or both. Mermaid diagrams become images, and optional templates (a Word letterhead, a LaTeX class) give the output your organisation's look. Without templates you get plain, working exports.

## Requirements

| Tool | Install on Windows | Needed for |
| --- | --- | --- |
| PowerShell 7 | `winget install Microsoft.PowerShell` | running the script (always) |
| Pandoc 3.8 or later (tested with 3.12; the script uses `--syntax-highlighting`, added in 3.8) | `winget install JohnMacFarlane.Pandoc` | every export |
| Node.js and Mermaid CLI (`mmdc`) | `winget install OpenJS.NodeJS`, then `$env:PUPPETEER_SKIP_DOWNLOAD = "1"; npm install -g @mermaid-js/mermaid-cli` (the script uses the installed Edge or Chrome, so Chromium is not downloaded) | documents with a Mermaid block; others export without them |
| Microsoft Edge or Google Chrome | already on most Windows machines | rendering Mermaid diagrams |
| A LaTeX distribution providing `pdflatex` and `xelatex` | `winget install MiKTeX.MiKTeX` | PDF output only (`pdflatex` with a `pandocTemplate`, `xelatex` without) |
| Poppler (`pdftotext`, `pdffonts`) | `winget install oschwartz10612.Poppler` | the searchable-PDF checks after exporting |

The script is written for Windows; on macOS or Linux PowerShell 7 runs it, but several parts assume Windows (the default config path, the PATH refresh, the `;` path separator passed to pandoc, the browser lookup), so it is not supported there.

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
