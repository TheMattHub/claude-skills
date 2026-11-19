---
name: releasing-a-repo
description: Use when asked to release, prepare a release, bump or tag a version, or write release notes for any repository - "release 0.7.2", "prepare the next release", "tag it", "write the changelog for the release" - or right after a version bump. Bumps, tags and opens a DRAFT GitHub release with short notes; the user publishes it, since publishing can fire PyPI or other deploys.
---

# Releasing a repo

Draft everything; the user publishes. A published release is outward-facing and often irreversible
(a PyPI version can never be reused).

## Before anything

1. **Repo-specific file?** Check `references/<repo>.md`. This is an optional file you may add
   for a repository; none ships with this skill. If present, it overrides
   the generic steps below. A repo released more than once gets one, written after its first release.
   `references/example-release-notes.md` shows the notes style and what such a file can hold.
2. **What fires a publish.** Read `.github/workflows/*`: which events (`release: published`,
   `push: tags`, ...) upload or deploy. If a **tag push** deploys, the tag is the publish: stop
   after the bump and ask the user before pushing the tag.
3. **Previous release.** `git tag --sort=-v:refname | head -3` and `git show <last bump commit> --stat`
   give the tag format and every file that carries the version.

## Steps

1. **Version (semver).** Patch: fixes and additions. Minor: new features, or stricter validation
   that can refuse input that was accepted before. Major: removals or incompatible changes after 1.0.
   Say which and why in one line.
2. **Bump:** the same files as the last bump. In the changelog, `## Unreleased` becomes
   `## X.Y.Z (<date>)`, with a short paragraph on top for readers. Check every claim in that
   paragraph against the code: one note claimed a feature worked end to end when one path
   still refused it.
3. **Quick tests** that cover packaging and docs; the full suite only if the repo's notes ask.
4. **Commit** `Version X.Y.Z` (plus any co-author or attribution line the repository's conventions require), push.
5. **Tag:** `git tag -a vX.Y.Z -m "Version X.Y.Z"` on that commit, push the tag, unless a tag
   push deploys (see "Before anything", step 2).
6. **Short notes** to a scratch file: one bullet per theme, a bold label, one or two
   user-facing sentences, no internal bug or decision IDs. State a known limit where a reader
   would assume more. Example: `references/example-release-notes.md`.
7. **Draft:** `gh release create vX.Y.Z -R <owner/repo> --draft --verify-tag --title "X.Y.Z" --notes-file <file>`.
   Never create a release without `--draft`, and never `gh release edit --draft=false`.
8. **Report:** the draft's URL, the notes text, and what publishing will fire. After the user says
   it is published, verify the artifact: install the published artefact in a clean environment the way a user would
   (for a Python package, `pip install pkg==X.Y.Z` in a clean venv; `pip` applies to Python packages only) and log it.
