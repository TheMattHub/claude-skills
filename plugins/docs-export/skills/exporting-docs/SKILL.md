---
name: exporting-docs
description: Use when project documentation written in markdown (README, conceptual model, devlog, resources, handbook, report) must be shared as a Word or PDF file - "export the docs", "make a Word version", "PDF for the client", "send the documentation" - including documents with Mermaid diagrams and letterhead or LaTeX templates. Not for writing the documents, and not for editing an existing .docx or .pdf.
---

# Exporting markdown documentation to Word and PDF

Markdown stays the source. One script turns a project's documents into a Word file, a PDF or both, with your templates applied if configured and Mermaid diagrams rendered as images. Never edit the exported files by hand: change the markdown and export again.

## Run it

```powershell
pwsh "<skill folder>/scripts/export-docs.ps1" -ProjectDir <project folder> -Format both
```

`<skill folder>` is this skill's base directory, which Claude Code reports when the skill loads. Call the script by its absolute path, from the project being exported.

With no other option the script takes `README.md`, `HANDBOOK.md`, `CONCEPTUAL_MODEL.md`, `RESOURCES.md`, `EXPERIMENTS.md` and `DEVLOG.md`, in that order, skipping those that do not exist. It writes one combined file per format to `<project>\export\`, named after the project folder.

| Option | Use |
| --- | --- |
| `-Format docx`, `pdf` or `both` | Output type; `docx` is the default |
| `-Files a.md,b.md` | Choose the documents and their order |
| `-Separate` | One output file per document |
| `-HideLinks` | PDF: links not coloured (they are coloured by default, so readers see what is clickable); for documents meant for print |
| `-Title`, `-Subtitle`, `-Client`, `-Author` | Cover fields; title defaults to the folder name, author to `git user.name` |
| `-Revision`, `-RevisionNote`, `-Classification` | Revision row and classification box on the PDF cover. `-Classification` is free text (default `unclassified`), passed to the template unchanged |
| `-RevisionsFile revisions.yaml` | Full revision table instead of the single row: a YAML file in the project with a `revisions:` list of `rev`, `note`, `date`, oldest first, one row per revision |
| `-Lang en` or `it` | Language of the PDF's generated headings and hyphenation |
| `-WordTemplate`, `-LatexTemplate`, `-PandocTemplate` | Override the configured templates for one run |
| `-ConfigPath` | Read the settings from another file than `~/.claude/docs-export.json` |

## Before exporting

1. Ask who receives the file and in which format, unless the user said so. Client name and classification go on the cover.
2. Check that `export/` is in the project's `.gitignore`. The output is generated and stays out of git.
3. Before exporting for someone outside the team, ask which documents are internal and leave those out. Development logs and findings files usually are: the recipient has no need for them, and they often hold things not meant to leave the team.

## After exporting

The script prints one line per file with the tables and figures it found against those in the source, and the PDF page count. A line marked `CHECK` means content was lost.

Then look at the result yourself: open the PDF with the Read tool and check the cover, one table and one diagram. Report the file paths to the user. Word asks to update fields when the file first opens; answering yes fills the table of contents.

Check that the PDF can be searched. A page can look right while viewers cannot find its text:

- `pdffonts FILE.pdf` lists no `Type 3` font. Type 3 fonts are bitmaps without a Unicode map: Acrobat and Edge cannot search their text, and it blurs when zoomed.
- `pdftotext -enc UTF-8 FILE.pdf -` contains a few code terms and accented words from the source, and no `↪`, the mark of a wrapped code line, and no word split across lines by a hyphen (`azien-` / `dale`). The template turns hyphenation off for this reason: the hyphen stays in the text layer and Ctrl+F misses the word.
- Compare a word's count in the PDF text with its count in the source's visible text, leaving out link targets and anchor ids, which also contain words.

## Writing for the PDF

- **Code lines under about 85 characters.** Longer lines wrap with a `↪` mark, which breaks Ctrl+F and copy-paste of the command. With an accented character on the wrapped line, pdflatex stops altogether. Put comments on their own line and split long commands (PowerShell: a backtick at the end of the line).
- **Link targets where Markdown has none**, such as a term in a glossary table: write `<a id="g-term"></a>` in the cell and link to `#g-term`. GitHub renders the anchor, and `scripts/html-anchors.lua` (next to the export script) keeps it in Word and PDF. Without the filter, LaTeX drops raw HTML and the link leads nowhere.
- **A file that leaves your organisation is read alone.** Before exporting, check that every sentence has its subject, verb and explicit request, and that nothing refers to internal ids, notes or attachments the recipient lacks (the `writing-self-contained-text` skill of the `writing-toolkit` plugin does this check, if installed).
- Text inside Mermaid diagrams and screenshots is an image: it cannot be searched. Put the terms a reader will look for in the prose too.

## Templates

The script reads three optional settings from `~/.claude/docs-export.json`, so template files stay out of the project:

```json
{
  "wordTemplate": "C:\\path\\to\\letterhead.docx",
  "latexTemplate": "C:\\path\\to\\latex-class.zip",
  "pandocTemplate": "C:\\path\\to\\bridge.latex"
}
```

Write Windows paths with backslashes doubled, or use forward slashes (JSON does not accept a single backslash).

- **Word:** `wordTemplate` is any `.docx`. Pandoc takes its header, footer, margins and styles.
- **PDF with your own class:** `latexTemplate` is a folder or zip holding your LaTeX class and its assets. `pandocTemplate` is a pandoc LaTeX template that loads that class and feeds it pandoc's body, using the variables `client`, `revision`, `revision-note`, `classification`, `title`, `subtitle`, `author`, `date`. It also receives `english` (set to `true` when `-Lang en`, so the template can pick the main language; the example template ignores it), `hidelinks` (set to `true` with `-HideLinks`; the example template then switches off link colouring) and `revisions` (the list from `-RevisionsFile`, each entry with `rev`, `note`, `date`; the example template prints it as a table after the cover). A PDF build needs both keys: with `latexTemplate` alone the script stops and names the missing key.
- **PDF with a template but no class:** `pandocTemplate` alone is allowed. `templates/example-bridge.latex` in this skill's folder is a minimal one built on the standard `article` class; copy it as the starting point for a company class.
- **No template configured:** the PDF gets pandoc's plain layout (built with `xelatex`).

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

## When it fails

| Symptom | Cause and fix |
| --- | --- |
| `Mermaid diagram N in X.md failed to render` | Syntax error in that block. The message carries Mermaid's own error |
| `pdflatex failed` with `Unicode character` | A character the font lacks. Replace it in the markdown, or write it as a word |
| `pdflatex failed` with `File ... not found` | A LaTeX package is missing. Install it with the MiKTeX console |
| `latexTemplate is set but pandocTemplate is missing` | Add the `pandocTemplate` key (see Templates), or remove `latexTemplate` |
| `pdflatex failed` with `Invalid UTF-8 byte sequence (…\FancyVerbBreakAnywhereBreak)` | A code line long enough to wrap holds an accented character, and the line breaker splits it. Shorten the line (see Writing for the PDF) |
| Ctrl+F in the PDF misses words in code, commands or file names | The code font is a bitmap (Type 3): `pdffonts` shows it. `templates/example-bridge.latex` sets Latin Modern Mono (`\ttdefault{lmtt}`); a custom template needs the same line |
| A link in the PDF lands at the top of a section, not on the word | It points to a heading. Give the word its own `<a id>` anchor (see Writing for the PDF) |
| A table runs off the PDF page | A cell holds one unbroken string longer than about 40 characters, such as a path. Shorten it or move it out of the table |
| `pandoc failed` on the `.docx` | The previous export is open in Word. Close it and run again |
| Tables without borders in Word | The file was produced without this script. Run the script |
