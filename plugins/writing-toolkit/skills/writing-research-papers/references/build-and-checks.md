# Build and checks

## arXiv (LaTeX), a proven setup
- Class `article`, 11pt a4paper; packages: fontenc/inputenc/lmodern/microtype, geometry (2.5 cm), amsmath,
  booktabs, tabularx, graphicx, xcolor, tikz (diagrams), listings, natbib `authoryear,round`, hyperref last.
- Build: `cd paper/arxiv && latexmk -pdf main.tex` (MiKTeX on Windows; runs bibtex with `plainnat`). Keep the
  log (`build.log`): look for "Output written on main.pdf (N pages)", no undefined citations or
  references, no overfull boxes you did not accept.
- Figures: `python paper/arxiv/figures/make_figures.py` from the repo root; matplotlib, `pdf.fonttype 42`
  so fonts embed; PDF output.
- arXiv upload bundle: sources plus `.bbl`, figures; no aux/log files. Test by compiling a clean copy.
  (Upload itself needs the author's word.)

## JOSS
- Preview with Docker: `docker run --rm --volume ${PWD}/paper/joss:/data --env JOURNAL=joss openjournals/inara`
- No Docker: `pandoc paper.md --citeproc -s -o preview.html` from the paper folder.
- `paper.bib` = the subset of the arXiv bib that `paper.md` cites; regenerate when either changes.
- Front matter: title, tags, authors (name, ORCID, affiliation index), affiliations (ROR), date, bibliography.

## Bibliography checks
- Every cite key exists; look for "undefined" in the log; no duplicate entries.
- Entries from memory carry `note = {verify}`; verify against the publisher, DOI or RePEc; then delete the note.
- Imported bibs (e.g. from a thesis): clean duplicated fields; complete volume and pages from the record.
- Grep both bibs for `verify` before submission; none may remain.

## Encoding
- LaTeX: write en dashes as `--`, thousands as `1{,}483`, non-breaking space as `~` (`Opus~5.5`).
- If the repo's hygiene tests require ASCII, keep the paper ASCII too; use `\'e` for accents.
- JOSS Markdown: `$...$` math, `[@key]` citations; braces in BibTeX protect capitals.

## Limits
- JOSS: short body, current limit on the venue page; count with `wc -w` minus front matter and references.
- arXiv: none; use the length the evidence supports.
