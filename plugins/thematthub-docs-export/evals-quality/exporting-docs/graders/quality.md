---
type: llm
---

Judge the final answer against these observable criteria.

1. The answer leaves the DEVLOG (internal notes) out of the client file, or asks the user whether it should be included.
2. The answer makes sure the Mermaid diagrams are rendered to images before or during the conversion.
3. The answer checks after export that the PDF text is searchable and copyable (for example fonts are not bitmap fonts, extracting the text finds words from the source).
4. The answer keeps the Markdown as the source: fixes are made there and the export is rerun, the output is not hand-edited, and the output folder is kept out of git.
5. The answer asks or settles who receives the file and puts the client name and a classification or revision on the cover, and checks the text reads on its own without internal references.

PASS if at least 4 of the 5 criteria hold. FAIL otherwise. Name the criteria that failed.
