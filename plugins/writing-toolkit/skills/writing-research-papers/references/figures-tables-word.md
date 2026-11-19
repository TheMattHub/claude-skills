# Figures and tables in Word and PDF reports

Rules for any report, write-up or handbook built as Word/PDF (pandoc + python-docx + Word export, or by hand). They come from user corrections on real deliverables.

## Rules

| Element | Rule |
|---|---|
| Tables | Numbered title **above**: "Table N. Title". Every table has a title, written for that table (not "Step by step (2)"). |
| Figures | Numbered caption **below**: "Figure N. Caption". Every chart, flowchart, map and diagram is a figure. |
| Numbering | Word SEQ fields (`SEQ Table`, `SEQ Figure`), so Word renumbers if items move. Update fields before PDF export. |
| Placement | Figures and their captions centred; 12 pt space above a figure so it never touches a table or text. |
| Readability | Text inside a figure prints at about 7 pt or more. Wide charts use the full text width (6.5 in on Letter with 1 in margins); tall flowcharts about 6 in wide. Never shrink figures to save a page; add the page. |
| Layout balance | Readability first, then composition. If a figure jumps to the next page and leaves roughly a third of a page or more empty, trim the figure's own empty margins and reduce its width, down to the readability floor (about 7 pt text), so it fits; otherwise accept the page break. |
| Charts | Chart fonts sized for the printed width (matplotlib ~12 pt base at 9–11 in figure width). Legends outside the data area; data labels show values only. Two charts side by side only if their text stays readable at half width. |
| Tables (layout) | Columns sized to content; no column narrower than its longest word; header row shaded and bold; 8–9 pt body. |

## Pandoc traps

- **Declare the page in the reference .docx** (page size and margins). Without it pandoc assumes a 5.83 in text width and silently caps every image there, whatever width the markdown asks for.
- **Table captions:** `Table: Title` after a pipe table becomes a "Table Caption" paragraph above the table. Inside a list item it becomes an ordinary paragraph instead, so keep tables out of list items.
- **Indented text after a de-listed table** becomes a code block. Check for "Source Code" style paragraphs after building.
- **Equal column widths:** pandoc gives pipe-table columns equal widths; fix widths in post-processing (python-docx: fixed layout, cell widths and `w:gridCol`).
- **Percent widths** are relative to pandoc's assumed text width; use inches for full-width figures.

## Check before hand-off

1. List captions in the PDF text (`pdftotext file.pdf - | grep -E "^(Table|Figure) [0-9]+"`); every table and figure appears once, in order.
2. Render each page to an image and look: no figure text below ~7 pt, no legend over data, no overlaps.
3. Count images in the PDF (`pdfimages -list`) against the figures in the source, to catch dropped images (wrong relative paths).
