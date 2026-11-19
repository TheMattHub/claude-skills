# Docs-site best practices (surveyed October 2026)

Source: a live survey of NumPy, pandas, SciPy, SimPy, salabim, Mesa, Ciw docs and the Diataxis and llms.txt references. Tags: verified (fetched 2026-10-18; WebFetch summaries, not verbatim), snip, [m] memory, n/f not found. AnyLogic answered 403; Plant Simulation help is behind a login.

## Best practices
1. Audience cards on the landing page (newcomer / concepts / reference / contributor). NumPy, pandas, SciPy. Gets each reader to the right page in one click. verified
2. Task-phrased tutorial titles ("How do I select a subset..."). pandas. Matches how people search. verified
3. Four-way split tutorial / how-to / reference / explanation, named plainly. Ciw (and Diataxis). Each page has one job. verified
4. "Coming from X" comparison pages (R, SQL, Excel). pandas. Routes planners and analysts by tool they already know. verified
5. Runnable example on the landing page, plus install line next to it. SimPy (example), Mesa (install). Proves value in 10 lines. verified; combine both
6. Examples built up in steps (bank model, then variants). salabim. Teaches modelling, not only syntax. verified
7. Version and release date in the header, switcher, downloadable HTML. NumPy, pandas, SciPy. Readers and agents know which version they read. verified
8. Migration guide per major version and release notes in nav. Mesa, NumPy, pandas. Trust and upgrade path. verified
9. "Citing" page with CITATION.cff / JOSS. Mesa, Ciw. Academic credibility. verified
10. Numpydoc-style API with Parameters/Returns/See Also/Examples, doctested. NumPy, pandas, SciPy. Examples never rot. [m]
11. Background/explanation section on mechanisms and bibliography. Ciw. Lets modellers check semantics. verified
12. llms.txt plus .md page copies with rel=alternate. Anthropic, Pydantic, uv (not the simulation tools). Cheap path for agents; none of the surveyed simulation docs has it, so it is an opening. verified
13. Separate example library and extensions list. Mesa. Keeps core docs short. verified
14. Light/dark toggle, "On this page" TOC, copy buttons (pydata theme). snip/[m]

## Avoid
- Landing with no code and no install line (NumPy, pandas, SimPy each miss one). verified
- Version only in a dropdown whose contents are not visible to crawlers; agents cannot tell which version they read. verified (switcher contents not in fetched text)
- One long class-by-class manual with no task entry points (salabim). verified
- No validation/verification page: none of the open-source simulation tools surveyed has one (verification vs analytic results is only implied in tests) [m]; a gap, or a differentiator for you.
- Hiding "10 minutes" inside the User Guide instead of Getting started (pandas). verified
- Docs behind login or bot blocks (AnyLogic 403, Plant Simulation): unusable by agents and prospects. verified/[m]
- Plain RTD theme with no audience routing (SimPy). verified
