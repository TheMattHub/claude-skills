"""Mechanical checks for a course handbook written in Markdown.

Reports what a reviewer would otherwise scan 100 pages for: broken section links and
missing images, leftover placeholders, long sentences, glossary terms whose first use
is not a link, and week/day sections without a summary box, a "Check yourself"
section or a "Done when" checklist. It reports; the reviewer decides. Standard library only.

Usage: python check_handbook.py GUIDE.md [--max-words 30] [--glossary Termini]
Run it on the guide in its own folder: image paths are checked relative to it.
Section links may point to a heading or to an HTML anchor (<a id="x"></a>).
"""
import argparse
import re
import sys
from pathlib import Path

UNIT = re.compile(r"^(settiman[ae]|week|weeks|giorn[oi]|day|days|modul[oi]|module|lezione|lesson|unit)\b", re.I)
DONE = re.compile(r"(fatto quando|done when|criteri di completamento)", re.I)
CHECK = re.compile(r"^#{3,6}\s+(verifica|check yourself|mettiti alla prova)", re.I)
GLOSSARY_WORDS = ("termini", "glossario", "glossary", "terms")
PLACEHOLDER = re.compile(r"<[A-Z][A-Z0-9_]{2,}>|\b(TODO|TBD|FIXME|XXX)\b")
LINK = re.compile(r"!?\[([^\]]*)\]\(([^)\s]+)[^)]*\)")
# An HTML anchor marks a link target where Markdown has none, e.g. on a glossary term in a
# table cell. GitHub renders it; when exporting to Word or PDF, use a converter that keeps
# it (for example Pandoc).
ANCHOR = re.compile(r"<a\s+(?:id|name)=\"([^\"]+)\"")
TAG = re.compile(r"<[^>]+>")
TOC_ENTRY = re.compile(r"^\s*([-*]|\d+\.)\s+\[[^\]]*\]\(#[^)]*\)\s*$")


def slug(heading):
    # GitHub and pandoc (gfm_auto_identifiers) agree on this rule.
    text = LINK.sub(r"\1", heading).replace("`", "").lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def parse(lines):
    """Headings as (line_no, level, text); a mask of lines inside code fences."""
    heads, in_code, code = [], False, []
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            code.append(True)
            continue
        code.append(in_code)
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if m and not in_code:
            heads.append((i, len(m.group(1)), m.group(2)))
    return heads, code


def check_links(lines, heads, code, base):
    slugs, seen = set(), {}
    for _, _, text in heads:  # duplicate headings get -1, -2 like on GitHub
        s = slug(text)
        n = seen.get(s, 0)
        slugs.add(s if n == 0 else f"{s}-{n}")
        seen[s] = n + 1
    slugs.update(a for i, line in enumerate(lines, 1) if not code[i - 1] for a in ANCHOR.findall(line))
    out = []
    for i, line in enumerate(lines, 1):
        if code[i - 1]:
            continue
        for _, target in LINK.findall(line):
            if target.startswith("#"):
                if target[1:] not in slugs:
                    out.append(f"  line {i}: no heading or anchor for {target}")
            elif not re.match(r"^[a-z]+:", target):
                path = (base / target.split("#")[0].replace("%20", " "))
                if not path.exists():
                    out.append(f"  line {i}: file not found {target}")
    return out


def check_placeholders(lines):
    return [f"  line {i}: {m.group(0)}" for i, line in enumerate(lines, 1)
            for m in PLACEHOLDER.finditer(line)]


def prose_chunks(lines, code, stop):
    """Paragraphs and list items as (line_no, text), skipping code, tables, headings."""
    chunk, start = [], 0
    for i, line in enumerate(lines[:stop], 1):
        s = re.sub(r"^(>\s*)+", "", line.strip())  # a quoted box is prose too
        skip = code[i - 1] or not s or s.startswith(("#", "|", "<!--", "![")) or s.startswith("```")
        new_item = re.match(r"^([-*]|\d+\.)\s", s)
        if (skip or new_item) and chunk:
            yield start, " ".join(chunk)
            chunk = []
        if not skip:
            if not chunk:
                start = i
            chunk.append(re.sub(r"^([-*]|\d+\.)\s+(\[[ x]\]\s+)?", "", s))
    if chunk:
        yield start, " ".join(chunk)


def check_sentences(chunks, max_words):
    out = []
    for line_no, text in chunks:
        text = LINK.sub(r"\1", text).replace("**", "")
        for sentence in re.split(r"(?<=[.!?;:])\s+(?=[A-ZÀÈÉÌÒÙ«\"(*_`])", text):
            n = len(sentence.split())
            if n > max_words:
                out.append((n, line_no, sentence))
    return sorted(out, reverse=True)


def glossary_section(heads, lines, name):
    """Line and terms (first table column) of the glossary section."""
    wanted = (name.lower(),) if name else GLOSSARY_WORDS
    for k, (i, level, text) in enumerate(heads):
        if not any(w in text.lower() for w in wanted):
            continue
        end = heads[k + 1][0] - 1 if k + 1 < len(heads) else len(lines)
        rows = [l for l in lines[i:end] if l.startswith("|")][2:]  # skip header and ---
        if rows:
            return i, [TAG.sub("", r.split("|")[1]).strip().strip("*") for r in rows]
    return None, []


def term_pattern(term):
    """Regex for a term, tolerant of Italian/English plural endings on every word
    ("Cambio formato" also matches "cambi formato")."""
    term = re.sub(r"\s*\(.*?\)", "", term).strip()
    stem = lambda w: (re.escape(w[:-1]) + r"\w{0,2}") if len(w) > 3 and w[-1].lower() in "aeios" else re.escape(w)
    body = r"\s+".join(stem(w) for w in term.split())
    flags = 0 if term.isupper() else re.I
    return re.compile(rf"(?<!\w){body}(?!\w)", flags)


def check_terms(lines, code, gloss_line, terms):
    unlinked, unused = [], []
    for term in terms:
        bare = re.sub(r"\s*\(.*?\)", "", term)
        parts = [p for p in re.split(r",\s*|\s+e\s+|\s+and\s+", bare) if p] or [bare]
        first = None
        for i, line in enumerate(lines[: gloss_line - 1], 1):
            # Headings and table-of-contents entries are not a first use in prose.
            if code[i - 1] or line.lstrip().startswith("#") or TOC_ENTRY.match(line):
                continue
            # Blank out link targets so a term inside a URL is not a use.
            visible = LINK.sub(lambda m: m.group(0)[: m.end(1) - m.start() + 1].ljust(len(m.group(0))), line)
            hits = [m for p in parts for m in term_pattern(p).finditer(visible)]
            if hits:
                first = (i, line, sorted(hits, key=lambda m: m.start()))
                break
        if not first:
            unused.append(term)
            continue
        i, line, hits = first
        # Inside the text of an internal link (to the glossary or to the section that
        # explains it), or in bold, which marks the place where the guide defines it.
        # Any part of a compound term ("PLE e Professional") linked on that line counts.
        links = [(m.start(1), m.end(1)) for m in LINK.finditer(line) if m.group(2).startswith("#")]
        bold = [(m.start(), m.end()) for m in re.finditer(r"\*\*[^*]+\*\*", line)]
        linked = any(a <= h.start() and h.end() <= b for h in hits for a, b in links + bold)
        hit = hits[0]
        if not linked:
            a = max(0, hit.start() - 30)
            unlinked.append(f"  line {i}: {term!r} … {line[a:hit.end() + 40].strip()} …")
    return unlinked, unused


def check_units(lines, heads):
    out = []
    for k, (i, level, text) in enumerate(heads):
        if level != 2 or not UNIT.match(text):
            continue
        end = heads[k + 1][0] - 1 if k + 1 < len(heads) else len(lines)
        nxt = next((n for n, (_, lv, _) in enumerate(heads[k + 1:], k + 1) if lv <= 2), len(heads))
        stop = heads[nxt][0] - 1 if nxt < len(heads) else len(lines)
        body = [l for l in lines[i:end] if l.strip()]
        missing = []
        if not body or not body[0].lstrip().startswith(">"):
            missing.append("summary box (a > block right under the heading)")
        if not any(CHECK.match(l) for l in lines[i:stop]):
            missing.append("'Check yourself' section")
        if not any(DONE.search(l) for l in lines[i:stop]):
            missing.append("'Done when' checklist")
        if missing:
            out.append(f"  line {i}: {text} - no " + ", no ".join(missing))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("guide", type=Path)
    ap.add_argument("--max-words", type=int, default=30)
    ap.add_argument("--glossary", default=None, help="glossary heading text (default: auto)")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    lines = args.guide.read_text(encoding="utf-8").splitlines()
    heads, code = parse(lines)
    gloss_line, terms = glossary_section(heads, lines, args.glossary)

    def report(title, items, limit=None):
        print(f"\n{title}: {len(items)}")
        for item in items[:limit]:
            print(item)
        if limit and len(items) > limit:
            print(f"  … {len(items) - limit} more")

    report("Broken links", check_links(lines, heads, code, args.guide.parent))
    report("Placeholders", check_placeholders(lines))
    long_ones = check_sentences(prose_chunks(lines, code, gloss_line or len(lines)), args.max_words)
    report(f"Sentences over {args.max_words} words (longest first)",
           [f"  line {ln}: {n} words: {s[:110]}…" for n, ln, s in long_ones], limit=15)
    report("Week/day sections missing a part", check_units(lines, heads))
    if terms:
        unlinked, unused = check_terms(lines, code, gloss_line, terms)
        report(f"Glossary terms ({len(terms)}) whose first use is not a link to where they are explained", unlinked)
        report("Glossary terms never used before the glossary", [f"  {t}" for t in unused])
    else:
        print("\nGlossary: no glossary table found (use --glossary HEADING)")


if __name__ == "__main__":
    main()
