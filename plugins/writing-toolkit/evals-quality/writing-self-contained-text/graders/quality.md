---
type: llm
---

Judge the final answer against these observable criteria.

1. Every item that asks Marco for something is written as a full request with a verb and states what is wanted (for example "Please send us ..." or "Is the heating ...?"), not as a bare list of nouns such as "Type, line, rated power".
2. Each internal identifier from the draft (tORDER_EVENTS, "CS", "PB-14") is either explained in plain words or left out; none stays as an unexplained code.
3. The rewrite does not point Marco to a sheet, list or ticket he has not received, unless the email itself describes its content or the answer tells Luca it must be attached.
4. The "x80" figure is rewritten with what it counts and in what (for example 80 jumps of the energy counter, on which meters or period), or the answer tells Luca the missing detail is needed.
5. Where the draft does not say what "CS" stands for, the answer does not state an expansion as fact (such as "cold storage"); it asks Luca or writes around it.

PASS if at least 4 of the 5 criteria hold. FAIL otherwise. Name the criteria that failed.
