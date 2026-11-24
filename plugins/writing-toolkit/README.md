# writing-toolkit

Seven skills for writing that a stranger can follow. Claude loads each one when your request matches.

| Skill | What it does | Example request |
|---|---|---|
| `writing-self-contained-text` | Makes a text understandable to a reader who has only the text: full sentences, named things, units. | "Write the questions we send to the supplier." |
| `writing-course-handbooks` | Structure and checks for guides that learners follow alone, with a checker script. | "Review this participant guide before the first tester." |
| `writing-docs-sites` | Plans or audits a documentation site: structure, landing page, learning path, AI readers. | "Improve our docs landing page." |
| `writing-research-papers` | Drafts and checks papers: venue, claims traced to evidence, references, submission checklist. | "Is this manuscript ready to submit?" |
| `writing-italian` | Natural Italian prose, with tables of calques and false friends; cover letters. | "Scrivi una lettera di presentazione." |
| `analysing-competitors` | Competitor analysis where every claim says how it was verified. | "Run a market scan of tools like ours." |
| `right-sizing-deliverables` | Matches a report or project to its realistic author, reader and effort instead of maximum completeness, and refuses to fake a human style. | "Make an 80/20 version of this course project." |

## What it reads, writes and runs

The skills are instructions; they run nothing. One script, `skills/writing-course-handbooks/scripts/check_handbook.py`, reads the markdown file you name and prints findings. It writes nothing and uses no network.

## Requirements

- Python 3, the only requirement, and only for that script.

## Optional companions

- The `docs-export` plugin of this marketplace, or another Word/PDF export tool such as Pandoc, for handbooks and papers.
- Other skills, if you have them, for brainstorming or planning; none is needed.

## Install

```text
/plugin install writing-toolkit --marketplace TheMattHub/claude-skills
```
