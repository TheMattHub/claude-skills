# Venues (table checked October 2026; re-check every venue live, rules change)

## Table

| Venue type | Typical gate and format | Watch for |
|---|---|---|
| Journal | author guidelines, word or page limit, template, abstract style (structured?), keywords, highlights or graphical abstract on some, cover letter, suggested reviewers | scope fit, ethics and COI statements, data availability statement, reporting guideline checklist, preprint policy, open-access fee |
| Conference | call for papers, page limit, template, deadline, sometimes double-blind, camera-ready after acceptance, presenter registration | anonymisation, supplementary material rules, copyright form, archival vs non-archival |
| arXiv | endorsement, category fit (e.g. cs.MS, cs.SE; cross-list), LaTeX or PDF; no review | upload sources plus `.bbl`; versions are permanent; moderation can reclassify |
| SSRN, bioRxiv, medRxiv, OSF | no or light screening; medRxiv/bioRxiv need ethics and COI declarations, medRxiv screens clinical content | journal preprint policies; clinical claims need care |
| Zenodo and institutional repositories | deposit with metadata, DOI per version | licence choice, cite the DOI of the exact release or dataset version |
| JOSS (software) | repo public > 6 months, open development (releases, CI, CONTRIBUTING), evidence of research use (intent does not count); `paper.md` + `paper.bib`, ~250-1000 words; sections: Summary, Statement of need, State of the field, Software design, Research impact statement, AI usage disclosure, Acknowledgements, References | OSI licence, tests, docs, honest AI disclosure, DOI at acceptance |
| White paper / report | see `white-papers.md` | approvals, confidentiality |

Order that worked for software: preprint first (no gate), journal or JOSS once eligible.

## How to read a venue's guidelines
1. Find the current author guidelines or call for papers; note the date and URL.
2. Extract into a checklist: length and template; anonymity; required sections and statements (ethics,
   consent, COI, funding, data and code availability, AI use, author contributions); reporting guideline;
   figure and reference format; preprint and prior-publication policy; fees and licence; supplementary files.
3. Check the scope with two or three recent papers from the venue; copy their structure, not their words.
4. Keep the checklist in the paper folder; tick it at submission.

## Cover letter (journals)
One page: the question and finding in two sentences, why this venue, that the work is original and not under
review elsewhere, preprint and data status, COI and approvals, suggested and excluded reviewers if asked.
No hype; no claim the paper does not support.

## Double-blind conferences and journals
Remove names, affiliations, acknowledgements and funder names; cite own work in the third person; anonymise
repo and data links (anonymous mirror); strip PDF and file metadata; do not post a preprint if forbidden.
Restore everything for camera-ready.

## Camera-ready
Apply required changes, add acknowledgements and funding, ORCIDs, copyright or licence form, final template,
fonts embedded, page limit, source files if requested; rerun numbers if anything changed.

## Revision rounds and response to reviewers
- Read all reports, wait a day, then triage: accept, partly accept, rebut with evidence.
- Letter structure: a short thanks, then each comment numbered, quoted, followed by "Response" and "Change"
  (where). Same numbering across rounds.
- New analyses go into the manuscript, not only the letter; rerun the claims inventory.
- Provide a marked-up and a clean version if asked. Meet the deadline or ask the editor for time.
- Tone: grateful, specific, no sarcasm; disagree with evidence and cite it.
- Sending the revision is the author's act.

## AI-disclosure statement (where required)
Say generative AI was used; which tools or models and when (e.g. from commit co-author trailers); what the
author decided; how AI output was verified; that the author reviewed the text and takes responsibility. Keep
a model under study separate from tooling. Some venues bar AI as author or restrict AI in review: read the
policy.

## Availability sections
Licence, repository URL, install line, version described, commands that repeat each table, documentation
URL, archive DOI. For data: repository, access conditions, and why anything is restricted. Link only public
resources; a private repository is not availability.
