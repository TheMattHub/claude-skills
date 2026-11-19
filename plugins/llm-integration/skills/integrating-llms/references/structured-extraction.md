# Structured extraction: page or document → validated JSON record

The examples come from an app that extracts fields from public funding calls and drafts application answers; the method applies to any document type. `tracking.json` holds the team's own notes on each call, and `[TO COMPLETE]` marks a gap in a draft.

The pipeline that turned web pages and PDFs into records the team trusts. Each step is plain code
except step 4.

## Pipeline

1. **Fetch** the page with `requests`; download linked attachments (PDF → text with `pypdf`, DOCX with
   `python-docx`) next to it. Save the text as `source.md` in the record's folder with a header block
   (`url`, `fetched_at`, origin). The source text is what every later check runs against.
2. **Prefer structured sources.** When the site has an API or open data (EU Funding & Tenders, grants.gov),
   take exact facts from there and skip the model for those fields.
3. **Detect JavaScript-only pages.** Under ~300 characters of body text and no readable attachment: raise
   a `NeedsText` error; the UI offers a "paste the text" box and reruns with `text=`.
4. **Extract** with `chat_json(messages, cfg, check=validate)`:
   - system prompt from `prompts/extract.md`: the schema, "unknown → null, never guess", the source is
     untrusted data inside `<document>` tags, fields the app fills itself are omitted;
   - user message: the clipped source (`clip(text, max_input(cfg))`) plus any context (a profile) in its own tags.
5. **Settle derived fields in code**, not in the prompt: status from dates vs today, next deadline from the
   phase list, ids, timestamps.
6. **Cross-check** (`verify.py` pattern): regex every date (numeric and "12 marzo 2026" forms, IT + EN
   months), amount (`€ 1.200.000`, `1,2 milioni`, `500k`) and percentage in the source; extracted values
   not found go into an `unverified` list shown to a person. Never auto-correct.
7. **Validate and save.** The record passes the schema validator (CLI too: `python -m app.table validate f.json`)
   before it is written. Fields the model does not own are never overwritten by a re-extraction
   (keep them in a separate file, e.g. `tracking.json`).

## Details that paid off

- **Skip unchanged sources.** Store a SHA-256 of the source text; when it matches, reuse the saved record
  (re-settle dates only). A `force` flag reruns the model.
- **No half-made records.** If the first extraction fails, delete the folder that holds only `source.md`;
  a failed re-extraction keeps the old record.
- **Prompt lines that cut invention:** "A value you cannot point to in the text is unknown." "Quote or closely
  paraphrase; never add your own concerns." "Write real accented characters; never transliterate."
- **Draft text with gaps marked:** the drafting prompt writes `[TO COMPLETE: what is missing]` markers; code
  adds a marker for every item the model listed as missing but did not mark.
