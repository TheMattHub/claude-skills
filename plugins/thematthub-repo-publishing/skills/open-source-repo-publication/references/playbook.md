# Open Source Repo Publication — Playbook

## Audit commands

```bash
# Ownership signal
git remote -v

# Secrets in the current tree (adjust pattern to the stack)
git grep -inE "SECRET_KEY|api[_-]?key|password\s*=|AWS_SECRET|BEGIN (RSA|PRIVATE) KEY" -- . ':(exclude)*.json'

# Was this path ever tracked, even if gitignored now?
git log --all --full-history -- path/to/file

# What filenames were ever added, across all branches?
git log --all --diff-filter=A --name-only --pretty=format: | sort -u | grep -iE "\.env|secret|credential|\.pem|\.key$"

# How many commits touch a suspect data path?
git log --oneline -- data/ | wc -l
```

Open a sample of any committed data files directly (`python -m json.tool` / `head`) and
look for real emails, names, or hashes — table/column names alone won't tell you.

## Clean orphan-history release

Use when the goal is "publish this code, not this history."

```bash
git checkout --orphan public-release   # new branch, no parent commit
git rm -rf --cached .                  # clear the index; files stay on disk

# Now remove anything that must not exist in the new history, from disk:
rm -rf path/to/real-data-dir
mkdir -p path/to/real-data-dir && touch path/to/real-data-dir/.gitkeep

# ... make code fixes, add scaffolding files, generate demo data ...

git add -A
git commit -m "Initial public release"

# Verify it's truly parentless before pushing:
git log public-release --oneline        # should show exactly one commit
git cat-file -p public-release | head -5 # no "parent" line

# Fix commit identity if the checkout used a work git config:
git commit --amend --no-edit --author="Name <email>"

# Push to a brand-new GitHub repo — never the original private origin, and never by
# flipping the original repo's visibility to public (unreachable objects from before
# a force-push aren't guaranteed to be gone from GitHub's servers immediately, and the
# Activity feed can still point at them):

# If the release should keep the original name, free it up first:
gh repo rename <original-name>-private --repo <owner>/<original-name>   # old repo, stays private

gh repo create <owner>/<original-name> --public
git remote add personal https://github.com/<owner>/<original-name>.git

# Sanity-check the tip before pushing — a local branch can be stale relative to a
# remote-tracking ref from earlier work even when the working tree is clean:
git log --oneline -1 public-release

git push personal public-release:main --force   # force only for a brand-new/empty target repo
```

Force-push is safe here only because the target is a freshly created, unshared repo.
Never force-push over a repo other people have already cloned.

## Scaffolding checklist

- `LICENSE` — ask which license and what name/year for the copyright line. MIT for
  "anyone can use it freely," Apache-2.0 to add an explicit patent grant, GPL-3.0 if
  derivatives must stay open.
- `README.md` — generalize any "internal/company only" framing to the broader audience;
  keep the real quick-start/setup instructions; add a License and Contributing section.
- `.env.example` — one line per env var with a placeholder value and a comment, if the
  project reads secrets from `.env` but ships no template.
- `CONTRIBUTING.md` — dev setup, test command, PR expectations.
- `CODE_OF_CONDUCT.md` — Contributor Covenant is the standard low-effort choice.
- `SECURITY.md` — private reporting contact; note the deployment assumptions (e.g. "not
  designed to be exposed directly to the internet") if that's true.
- `.github/ISSUE_TEMPLATE/*.md`, `.github/PULL_REQUEST_TEMPLATE.md` — lightweight, a few
  prompts each.
- `.github/workflows/tests.yml` — CI running the existing test suite. Minimal example
  (adapt runtime/commands to the stack):
  ```yaml
  name: Tests
  on:
    push: { branches: [main] }
    pull_request: {}
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
          with: { python-version: "3.12" }
        - run: python -m pip install -r requirements.txt
        - run: python -m unittest discover -s tests
  ```

## README screenshots

Capture from a throwaway instance loaded with the demo dataset, never the real one.

- Start the app against a scratch data dir / fresh DB (an env var, a `--data-dir` flag, a
  temp copy) so no real workspace, and no login wall from a locally-set password, is in
  the way. Import the demo dataset, then drive it far enough that the screens have real
  output (run the planner/report/whatever the app's main action is) — empty states make
  a worse first impression than no screenshot.
- Turn off in-app help banners, tooltips and onboarding hints first (they usually sit in
  `localStorage`, so set the flag in an init script) — they eat the top third of a
  screenshot and date the image.
- Drive it with Playwright (or any headless browser). Desktop shots at 1440x900 with
  `device_scale_factor=2`; phone-shaped pages at ~430px wide. Full-page shots only for
  pages worth showing whole — a 9000px-tall form is useless in a README.
- Post-process: crop trailing empty space, downscale to ~1440px wide, and for map/photo
  heavy shots quantize to 256 colors. Aim for a few hundred KB each — a README that
  takes 10MB to load is its own problem.
- Animation: screenshot the animating element ~25 times at ~120ms and assemble the frames
  into a GIF (Pillow's `save_all=True`). Clip to the element, not the whole page, or the
  file balloons.
- Alt text is not optional: describe what the screen shows, not "screenshot".

### Layout: don't stack full-width images

A column of full-width screenshots, one per feature, pushes the install instructions
below three screens of scrolling. Use this shape instead:

- **Opening visual, under the intro paragraphs and above `## What it does`:** something
  small and alive — the animated GIF if there is one, otherwise a short banner-shaped
  crop. Not the tallest screenshot in the set.
- **`## Screenshots`, one hero:** the single screen that shows the product working
  (workspace, dashboard, main output), full width, clickable.
- **Then 3-4 thumbnails side by side in one row**, each linking to its full-size file so
  a click enlarges it. One `<sub>` caption of a few words per cell — the per-image
  paragraphs come out; the images carry the message.

```html
<table>
<tr>
<td width="25%" valign="top" align="center">
<a href="docs/screenshots/home.png"><img src="docs/screenshots/home.png" alt="Home page: …" width="100%"></a>
<br><sub><b>Home</b> — tonight's trip, one next action</sub>
</td>
<!-- 3 more cells; width="25%" per cell for a 4-up row, 33% for 3-up -->
</tr>
</table>
```

Markdown hero, same click-to-enlarge: `[![alt](<image-path>)](<image-path>)`.

Thumbnails link to the *full-resolution* file — `width="100%"` in the cell does the
shrinking, so don't generate separate small copies.

**Verify the rendering before pushing** — GitHub sanitizes README HTML, and silently
drops attributes it doesn't allow:

```bash
python - <<'EOF'
import json, re, urllib.request, pathlib
body = json.dumps({"text": pathlib.Path("README.md").read_text(encoding="utf-8"), "mode": "gfm"}).encode()
req = urllib.request.Request("https://api.github.com/markdown", data=body,
                             headers={"Content-Type": "application/json", "User-Agent": "readme-check"})
html = urllib.request.urlopen(req).read().decode()
print(re.findall(r"<td[^>]*>", html))                              # attributes kept?
print(len(re.findall(r'<a href="[^"]*screenshots[^"]*"', html)), "clickable images")
EOF
```

(Match on the parsed HTML rather than printing all of it — a README with em dashes will
blow up on a Windows console's cp1252 stdout.)

`<table>`, `<td width|valign|align>`, `<a href>`, `<img src|alt|width>`, `<sub>`, `<b>`
all survive today. Anything you invented beyond that, check — don't assume.

## Demo-data generation pattern

Don't hand-write fixture JSON for the public demo dataset — drive the app's own code
(its registration/creation routes, or its internal functions) with a small script, then
export through whatever export function the app already has. This guarantees IDs,
computed fields (ratings, derived stats, achievement unlocks), and foreign-key
relationships are all valid, because the app's real logic produced them. Use obviously
fictional names and `@example.com` emails. Keep the script in the repo (e.g.
`scripts/generate_demo_data.*`) so the dataset can be regenerated later.

## Stale git credential cache

Symptom: push fails with a permission error naming the *wrong* account, even right after
the user says they "logged in again" (usually in a browser or a GUI app, which uses a
different credential store than the command-line git credential helper).

- The fix has to happen in an interactive terminal — a non-interactive shell can't
  complete a browser/device-code OAuth flow.
- Clear the stale cached credential first, or the helper just reuses it silently:
  `git credential-manager github logout`, or remove the `git:https://github.com` entry
  from the OS credential store (Windows Credential Manager / macOS Keychain).
- Then retry the push from that terminal, confirming the correct account in the login prompt.
- Do not suggest dragging the project folder into GitHub's web upload UI as a workaround
  — it bypasses `.gitignore` (can upload `.env`, `.git`, build artifacts) and undoes any
  history scrubbing just performed.

## Discovery and contribution setup

What a mature public repo does (pattern taken from `ai-job-search-dev/ai-job-search`), scaled down:

```bash
R=<owner>/<repo>
gh repo edit $R --description "<one line: what it is and for whom>" --homepage "https://github.com/$R#readme" \
  --enable-discussions --enable-wiki=false
gh repo edit $R --add-topic <5-8 topics people search for>
gh api -X PUT repos/$R/private-vulnerability-reporting
git tag -a v<version> -m "<name> <version>" && git push origin v<version>
gh release create v<version> --repo $R --draft --title "<name> <version>" --notes "<what it does, install>"   # the user publishes
gh api repos/$R/community/profile --jq .health_percentage                     # aim for 100
```

- **CONTRIBUTING with a scope.** Sections: the one rule the project follows; what gets merged; what
  gets declined, with the reason (company- or person-specific content, duplicate copies of the
  workflow for another runtime, speculative features, bundles); "claims get verified" (show the
  failure on the real path — the documented command on a real-shaped input — not a hand-built value
  fed to a function); setup and test commands identical to CI; PR titles as release notes
  (Conventional Commits type). Most declined PRs are good work that did not know the scope.
- **`.github/ISSUE_TEMPLATE/config.yml`** with `contact_links`: questions and ideas to Discussions;
  a warning against attaching private or company material to a public tracker.
- **PR template** opening with an HTML comment: check the base repository (PRs from personalised
  forks target upstream by default), how the title is used.
- **SECURITY.md** for agent projects: private reporting link; the threat model in plain words —
  which untrusted content the agent reads and that it is treated as data, what runs locally and
  what touches the network, what it is not (a sandbox).
- **README**: badges for CI and license; who it is for in the first paragraph; install for the main
  runtime and, for skills, how other agents use it; a Contributing line that points questions to
  Discussions. Optional: an `AGENTS.md` that points other agents at the single source of truth
  instead of a second copy of the instructions.
- **Plugins and skills**: listing in a marketplace or directory is the author's call (an external
  submission); mention it, do not submit.
