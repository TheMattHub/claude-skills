---
name: writing-self-contained-text
description: Use for a text the reader receives without the author or the chat at hand - a document or report to send, questions for a client or supplier, a plan or handoff brief for another agent - in any language; and when a reader says a text is unclear, telegraphic, "needs context", "what does this refer to", or a sentence is missing its subject, verb or the actual request.
---

# Writing self-contained text

## Overview

The reader has only the text: no chat, no notes, no code, no earlier messages, no author to ask. Text written from inside a piece of work drops what the writer takes for granted: the verb of a request, the name of a thing, the material it refers to. Every sentence must be understandable on its own.

## The contract: a self-contained sentence or list item has

1. **Its subject, verb and object written out.** A request says what is asked: "For each machine we need the type, the line and the rated power"; "Is the heating on when the press is idle?". Never only the nouns ("Type, line, rated power") or a fragment ("Heating or auxiliaries?"). In a list of requests every item is a request ("We need...", "Please send...", "Is...?"), even if it repeats the same opening.
2. **Things named in the reader's words.** A table, column, code, tag or system is introduced with what it is: "the events table of the warehouse system (tORDER_EVENTS)", "the historian (the database of the plant's time series)". An abbreviation is spelled out the first time.
3. **Only material the reader has.** Internal ids, notebooks, branches, tools, our playbooks, our alarms, "the list we proposed": either describe the thing in one clause ("we are preparing automatic alerts that fire when...") or leave it out. Never refer to an attachment that is not attached.
4. **Numbers with their unit and what they count**: "80 jumps of the energy counter, on 22 meters", not "x80".
5. **Meanings taken from the source, never guessed.** Expand an abbreviation or describe an id only with what the source says. When the source does not say what it means, ask the author or write the sentence without it: a guessed expansion ("CS = cold storage") puts a false fact in front of the reader.

## Final check

Read each sentence alone, as the recipient. Rewrite it if they could not say:
- who or what it is about;
- what is asked of them, or what it states;
- where the thing it mentions comes from.

Then search the text for the writer's internal vocabulary (ids, file names, branch or tool names, project jargon) and treat each hit with point 3.

Combine with the skill for the genre (writing-italian, writing-course-handbooks, writing-docs-sites, writing-research-papers; same plugin) and the language: this contract is about what the reader needs to understand, those skills about form.
