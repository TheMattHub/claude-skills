---
name: open-source-repo-publication
description: "Use when a private or internal repository is about to become public, or the user asks what to check before making one public: open-sourcing an existing project, publishing a private repo, prepping a portfolio or showcase repo, making a repo \"safe for others\", \"ready for the public\" or \"ready for contributors\", or making a public repo easier to discover and contribute to (topics, Discussions, contribution scope, issue routing, first release). Audits git history (not just the working tree) for real user data, credentials and company ownership; scrubs or rebuilds history; fixes insecure defaults; adds LICENSE/README/CONTRIBUTING/CODE_OF_CONDUCT/SECURITY/CI scaffolding; replaces real data with a synthetic demo dataset. Does not cover ongoing maintainer routines (issue triage, PR review cadence) once the repo is already public."
---

# Open Source Repo Publication

## Overview

The risk in open-sourcing an existing repo is rarely the current code — it's what's
baked into git history and left as insecure-by-default behavior. Deleting a file today
doesn't remove it from history; anyone can still clone the old commits. Treat this as an
audit-first task: find what's actually in the repo (working tree *and* history) before
touching anything, and let what you find decide the approach.

Run the audit before writing any README or LICENSE file: a repo that looks fine in its
current state can still have real PII or secrets sitting in old commits, or turn out to not
be the user's to publish at all.

## Workflow

1. **Audit before proceeding.**
   - Who owns this? Check `git remote -v` — a company/org remote plus "internal use"
     language in the docs means ownership needs the user's explicit call, not an assumption.
   - Scan the *working tree* for hardcoded secrets (`git grep` for `SECRET`, `PASSWORD`,
     `API_KEY`, etc.) and check `.gitignore` covers `.env`/credentials/local DB files.
   - Scan *history*, not just HEAD: `git log --all --diff-filter=A --name-only` for
     secret-shaped filenames; open any committed data files and check for real names,
     emails, password hashes. A file gitignored today can still be tracked in old commits
     — check with `git log --all --full-history -- <path>`.
   - Look for app behavior that *writes data into git automatically* (auto-commit /
     auto-snapshot features). If present, that's usually how real data got into history
     in the first place, and it's a root cause to fix, not just a symptom to clean up.
   - Inventory what's missing: LICENSE, CI, CONTRIBUTING, issue templates, `.env.example`.
2. **Surface blockers instead of guessing.** Ownership ambiguity and real PII/secrets in
   history are stop-the-line findings — report them plainly and ask before proceeding.
   Typical decisions that are the user's, not yours: license choice, copyright name,
   whether to scrub history in place or start fresh, demo-data vs. empty state.
3. **Pick a history strategy.** Default recommendation: a **fresh orphan-history
   branch** (see playbook) rather than rewriting the existing repo's history with
   filter-repo/BFG. An orphan branch has zero shared history with the original by
   construction — no risk of missing a blob — and never touches the original private
   remote. Only rewrite in place if the user specifically wants to keep one repo/URL and
   accepts that it breaks any existing clones/forks.
   - **The clean history always goes to a brand-new GitHub repo — never publish by
     flipping the existing repo's visibility to public**, even after an in-place
     history rewrite or force-push. If real secrets/PII were ever pushed to that repo's
     remote (true for any repo with real development history, not just a hand-authored
     example), GitHub doesn't guarantee immediate garbage-collection of objects that
     become unreachable after a force-push — they can stay fetchable by direct commit
     SHA, and the repo's Activity/Events feed can retain a compare link back to the
     pre-rewrite state, for a retention window. Flipping that same repo public exposes
     that window. Create a new repo for the release instead; if the name should stay the
     same, rename the old repo out of the way first (e.g. append `-private`) and keep it
     private — don't delete it outright unless the user explicitly wants that.
4. **Fix root causes, not symptoms.** For each unsafe default found in the audit, fix the
   behavior, don't just scrub its output:
   - Auto-commit/auto-export-to-repo features → default OFF, opt-in via env var.
   - Static/guessable default secret (`SECRET_KEY = "change-me"`) → generate a random
     per-process fallback with a logged warning, so zero-config startup still works but
     nothing ships a publicly-known secret.
   - Update `.gitignore` for the sensitive paths found; add `.env.example` if none exists.
5. **Add OSS scaffolding**: LICENSE, a README rewritten for a public audience (drop
   internal/company-only framing), CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md,
   issue templates, a PR template, and a CI workflow that runs the existing test suite.
   Ask for license choice and copyright name — don't assume.
6. **Replace scrubbed real data with synthetic demo data**, generated by driving the
   app's own real code (its own routes/functions), not hand-authored fixture JSON — that
   keeps computed fields, relationships, and derived state valid. Point to it from the README.
7. **Run the full test suite** after the defaults/behavior changes in step 4 — tests that
   implicitly relied on an old insecure default (e.g. "assumes auto-snapshot is on") will
   need updating to opt in explicitly.
8. **Fix commit identity before pushing.** A checkout configured with a work git identity
   bakes that email into the new public commit. Amend author/committer to what the user
   wants attributed publicly.
9. **Push to the brand-new remote** from step 3, never the original private `origin`. If
   the release should keep the original repo name: rename the old repo first (`gh repo
   rename <name>-private`), then `gh repo create <owner>/<original-name> --public`, then
   repoint the local `origin` and push. Before pushing, confirm the local branch tip is
   actually the latest intended commit — `git log --oneline -1` against what you expect,
   not just "no uncommitted changes" — a local branch can silently sit behind commits
   that only exist on a remote-tracking ref from earlier work. If a credential helper
   keeps authenticating as the wrong account after a fresh login, that's usually a stale
   host-scoped cache (see playbook) — don't work around it by uploading files through a
   browser instead, which bypasses `.gitignore` entirely.
10. **Show the project working in the README.** A public repo whose README is text-only
    reads as abandoned no matter how good the code is. For a project with a user interface
    or visual output, screenshot the running app; a library or a skills repository instead
    shows a short usage example or the output of a real command. For screenshots: run the app on the demo dataset, walk its pages, and capture the
    few screens that actually show what it does: one **hero image** directly under the
    title/badges (the screen that shows the product working — the map, the dashboard, the
    main output — not a marketing page or a settings form), then a `## Screenshots`
    section with one image per real capability the feature list claims. If a page has a
    signature animation, capture it as a short GIF alongside the stills. Lay them out so
    the README still fits on a screen or two: small opening visual under the intro, one
    full-width hero in the section, the rest as a row of click-to-enlarge thumbnails —
    never a stack of full-width images. Commit them under `docs/screenshots/` and
    reference them with relative paths. See the playbook for the capture recipe and the
    exact layout markup.
11. **Build every public-facing image from the demo dataset only.** Never screenshot or
    export from the real/private instance — that leaks the same PII through images
    instead of data files. Screenshots also pin the demo data down: if the dataset can't
    produce the screens you need (a null field the README claims is there), fix the
    dataset, don't stage the screenshot by hand.

12. **Set the repo up to be found and contributed to well**, not just published (checklist and
    commands in the playbook, "Discovery and contribution setup"):
    - Repo settings: description, topics, homepage; Discussions on for questions and ideas,
      empty wiki off; private vulnerability reporting on; a first release tag. Then check
      `gh api repos/<owner>/<repo>/community/profile` reports 100%.
    - CONTRIBUTING states the project's **scope** — what gets merged, what gets declined and
      why — not only setup commands. Ask for the failing case shown on the real code path,
      one concern per PR, PR titles written as release notes.
    - An issue `config.yml` routes questions to Discussions and warns against attaching
      private material; the PR template reminds fork users to check the base repository.
    - For agent/LLM projects, SECURITY.md states the threat model honestly: what untrusted
      content the agent reads (prompt injection), what runs locally, what it is not (a sandbox).
    - For skills and plugins: keep the skill folder self-contained (scripts inside it, paths
      relative to it) so other agents can use it, and say in the README which parts are
      runtime-specific.
    - For later versions of an already public repository, use `releasing-a-repo` (same plugin).

## Common pitfalls

- Assuming `git rm`/deleting a file fixes history — it doesn't; only an orphan branch or
  a history rewrite does.
- Screenshotting the real/private instance for "nicer" public screenshots — same leak, different medium.
- Shipping a README with nothing showing the project working (no hero image or screenshots
  for a UI project; no usage example or real command output for a library or skills
  repository) because the code was the "real" work. It's the first thing anyone judges the
  project by.
- Dragging a project folder into GitHub's web uploader as a shortcut past a git auth
  problem — skips `.gitignore` and can upload `.git` itself (the very history being scrubbed).
- Trusting that "I logged in again" fixed a push — a credential manager's cache is
  host-scoped and often doesn't refresh from a browser/app login done elsewhere.
- Leaving the auto-commit/auto-export feature on by default in the published template —
  it will recreate the same leak for the next person who clones it.
- Forgetting to change commit author/committer identity before the first public push.
- Flipping an existing repo's visibility from private to public after cleaning its
  history in place, instead of publishing through a new repo — GitHub can still surface
  the pre-cleanup commits via direct SHA or the Activity feed for a retention window
  after the force-push (see step 3).
- Pushing a local branch that's stale relative to the real latest commit (e.g. it only
  exists on a remote-tracking ref from a previous session) — verify the tip before
  pushing to the new repo, not just that the working tree is clean.

## References

See `references/playbook.md` for the exact git sequence for a clean orphan-history
release, scaffolding file templates, the demo-data-generation pattern, and credential
cache troubleshooting.
