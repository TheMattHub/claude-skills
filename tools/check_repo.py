"""Scripted gate for this marketplace: structure, skill limits, dead links, leaked personal data.

Usage:  python -I tools/check_repo.py [path ...]
With no path it checks the whole repository. Exit code 1 if any error is found.

Why a script: these checks are mechanical, so they run the same way before every push
instead of relying on a reviewer's attention.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_DESCRIPTION = 1024  # limit used by skill loaders outside Claude Code
MAX_SKILL_LINES = 500   # above this, detail belongs in references/
TEXT_SUFFIXES = {".md", ".json", ".py", ".ps1", ".sh", ".cs", ".txt", ".yaml", ".yml", ".js", ".lua", ".html", ".css"}

# Machine- or person-specific content that never belongs in a shared skill.
GENERIC_PATTERNS = {
    "Windows user path": re.compile(r"[A-Za-z]:\\+Users\\+(?!<|YOU|you|USERNAME|username|\$|%|\.\.\.)\w"),
    "macOS/Linux user path": re.compile(r"(?<![\w.])/(?:Users|home)/(?!<|you|USERNAME|username|\$)[a-z]\w+/"),
    "e-mail address": re.compile(r"[\w.+-]+@(?!example\.|users\.noreply\.github\.com|anthropic\.com|e2e\.local)[\w-]+\.[a-z]{2,}"),
    "hard-coded personal skills path": re.compile(r"~[/\\]\.claude[/\\]skills[/\\][\w-]+[/\\]"),
    "secret-shaped string": re.compile(r"(?:sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|\b\d{8,10}:[A-Za-z0-9_-]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY)"),
}
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
BACKTICK_PATH = re.compile(r"`((?:references|scripts|assets|examples)/[\w./-]+\.\w+)`")

errors = []


def err(path, msg):
    errors.append(f"{Path(path).relative_to(ROOT).as_posix()}: {msg}")


def private_terms():
    f = ROOT / ".private-terms.txt"
    if not f.exists():
        return []
    return [t.strip().lower() for t in f.read_text(encoding="utf-8").splitlines() if t.strip() and not t.startswith("#")]


def frontmatter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return None
    fields, key = {}, None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if km:
            key = km.group(1)
            fields[key] = km.group(2).strip().strip("\"'")
        elif key and line.startswith((" ", "\t")):  # folded multi-line value
            fields[key] += " " + line.strip()
    return fields


def check_skill(skill_md):
    text = skill_md.read_text(encoding="utf-8")
    fm = frontmatter(text)
    folder = skill_md.parent
    if fm is None:
        return err(skill_md, "no YAML frontmatter")
    if fm.get("name") != folder.name:
        err(skill_md, f"frontmatter name {fm.get('name')!r} differs from folder {folder.name!r}")
    desc = fm.get("description", "")
    if not desc:
        err(skill_md, "no description")
    elif len(desc) > MAX_DESCRIPTION:
        err(skill_md, f"description is {len(desc)} characters (max {MAX_DESCRIPTION})")
    lines = text.count("\n") + 1
    if lines > MAX_SKILL_LINES:
        err(skill_md, f"{lines} lines (max {MAX_SKILL_LINES}); move detail to references/")
    for md in folder.rglob("*.md"):
        body = md.read_text(encoding="utf-8", errors="replace")
        targets = set(LINK.findall(body))
        if md == skill_md:
            targets |= set(BACKTICK_PATH.findall(body))
        for target in targets:
            if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith(("<", "{")):
                continue  # URL or placeholder
            if not (md.parent / target).exists() and not (folder / target).exists():
                err(md, f"dead link: {target}")


def check_plugin(plugin_dir):
    manifest = plugin_dir / ".claude-plugin" / "plugin.json"
    if not manifest.exists():
        return err(plugin_dir, "missing .claude-plugin/plugin.json")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if data.get("name") != plugin_dir.name:
        err(manifest, f"name {data.get('name')!r} differs from folder {plugin_dir.name!r}")
    for field in ("version", "description", "license"):
        if not data.get(field):
            err(manifest, f"missing {field}")
    if not (plugin_dir / "README.md").exists():
        err(plugin_dir, "missing README.md")
    skills = sorted((plugin_dir / "skills").glob("*/SKILL.md")) if (plugin_dir / "skills").is_dir() else []
    if not skills:
        err(plugin_dir, "no skills/*/SKILL.md")
    for skill_md in skills:
        check_skill(skill_md)
    check_version_bump(plugin_dir, manifest, data.get("version"))


def git(*args):
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, encoding="utf-8")
    return r.stdout if r.returncode == 0 else None


def check_version_bump(plugin_dir, manifest, version):
    # Claude Code updates an installed plugin only when its version changes, so a content change
    # without a bump never reaches anyone. Compared with the published state (the upstream branch),
    # not commit by commit, so several unpushed commits can share one bump.
    base = git("rev-parse", "--verify", "-q", "@{upstream}") or git("rev-parse", "--verify", "-q", "origin/main")
    if not base:
        return  # not a clone, or nothing published yet
    base = base.strip()
    rel = plugin_dir.relative_to(ROOT).as_posix()
    published = git("show", f"{base}:{rel}/.claude-plugin/plugin.json")
    if published is None:
        return  # new plugin: its first version is the bump
    if json.loads(published).get("version") != version:
        return
    exclude = f":(exclude){rel}/.claude-plugin/plugin.json"
    changed = (git("diff", "--name-only", base, "--", rel, exclude) or "").split()
    changed += (git("ls-files", "--others", "--exclude-standard", "--", rel, exclude) or "").split()
    if changed:
        err(manifest, f"version {version} is the published one but {len(changed)} file(s) changed "
                      f"(e.g. {changed[0]}); bump it so installed copies update")


def check_marketplace():
    f = ROOT / ".claude-plugin" / "marketplace.json"
    if not f.exists():
        return err(ROOT / ".claude-plugin", "missing marketplace.json")
    data = json.loads(f.read_text(encoding="utf-8"))
    listed = set()
    for entry in data.get("plugins", []):
        src = entry.get("source")
        if isinstance(src, str):  # plugin kept in this repository
            target = ROOT / src
            listed.add(target.resolve())
            if not target.is_dir():
                err(f, f"plugin {entry.get('name')!r}: source {src} does not exist")
            elif target.name != entry.get("name"):
                err(f, f"plugin {entry.get('name')!r}: folder is named {target.name!r}")
    for d in sorted((ROOT / "plugins").glob("*/")):
        if d.resolve() not in listed:
            err(d, "plugin folder is not listed in marketplace.json")


def check_content(paths, terms):
    for base in paths:
        files = [base] if base.is_file() else base.rglob("*")
        for p in files:
            if not p.is_file() or ".git" in p.parts or "results" in p.parts or p.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if p.resolve() == Path(__file__).resolve() or p.name == ".private-terms.txt":
                continue  # these two files hold the patterns themselves
            for n, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                for label, pat in GENERIC_PATTERNS.items():
                    if pat.search(line):
                        err(p, f"line {n}: {label}")
                low = line.lower()
                for t in terms:
                    if t in low:
                        err(p, f"line {n}: private term {t!r}")


def main():
    args = [Path(a).resolve() for a in sys.argv[1:]]
    targets = args or [ROOT]
    terms = private_terms()
    if not terms:
        print("note: no .private-terms.txt, so only the generic patterns are checked")
    plugin_dirs = set()
    for t in targets:
        for manifest in t.rglob(".claude-plugin/plugin.json"):
            plugin_dirs.add(manifest.parent.parent)
    for d in sorted(plugin_dirs):
        check_plugin(d)
    if not args:
        check_marketplace()
    check_content(targets, terms)
    for e in errors:
        print("ERROR", e)
    print(f"{len(plugin_dirs)} plugin(s) checked, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
