# Memory

This page is for people who use Claude or Claude Code and are surprised by what it does or does not remember. After reading it you know what carries over between conversations, where it is stored, how to see and change it, and where a given piece of knowledge belongs.

Neither Claude nor Claude Code remembers a past conversation by itself. Each session starts with a fresh context (the text Claude has in view for the current conversation). What carries over is what is written down in the places below.

## Claude Code

Two mechanisms carry knowledge between sessions, and both are loaded at the start of every session.

### CLAUDE.md files: rules you write

A `CLAUDE.md` is a plain text file of instructions. Claude reads it as context, not as enforced configuration, so clear short rules work better than long ones.

| Kind | Where it lives | Who gets it |
| --- | --- | --- |
| User | `~/.claude/CLAUDE.md` | You, in every project |
| Project | `CLAUDE.md` or `.claude/CLAUDE.md` in the repository | Everyone who uses the repository, through git |
| Local | `CLAUDE.local.md` in the repository, listed in `.gitignore` (the file that tells git which files not to share) | You, in this project only |
| Organisation | A managed file set up by IT (on Windows, `C:\Program Files\ClaudeCode\CLAUDE.md`) | Everyone on the machine |

Claude also reads files in the folders above your working folder, and loads one in a subfolder when it works on files there. A repository that has an `AGENTS.md` (an instructions file that other AI coding tools use) and no `CLAUDE.md` is read through its `AGENTS.md`.

**What belongs in a CLAUDE.md.** Only what Claude cannot work out from the code: the commands to build, test and lint (check the code style), conventions that differ from the defaults, and gotchas ("the API tests need a local Redis"). Write each rule so it can be checked: "Run `npm test` before committing", not "test your changes". Give the reason when it is not obvious. Keep each file under 200 lines, because longer files cost context and Claude follows them less reliably. Do not describe the architecture or file layout, which Claude reads for itself. Do not shout: capitals and "IMPORTANT" make a current model over-apply a rule. A rule that can never have an exception belongs in a hook (a command that runs automatically at set moments) or a deny rule (a setting that blocks an action outright), not in prose. Both are Claude Code settings.

**Commands.** Run `/init` in a project to have Claude draft a starter `CLAUDE.md` from your code. It improves an existing file instead of overwriting it. Run `/memory` to list the instruction files that are loaded, open any of them in your editor, and toggle automatic memory. If Claude ignores a rule, `/memory` or `/context` (which lists what is currently loaded) shows whether the file is loaded at all.

A starting file for your personal `~/.claude/CLAUDE.md` is in [starter-CLAUDE.md](starter-CLAUDE.md). Copy it, then delete the rules you do not want.

### Automatic memory: notes Claude writes

As it works, Claude saves notes for itself: your role and preferences, corrections you gave and approaches you confirmed, ongoing work and decisions that are not in the code, and where to find outside information. It skips anything it can read from the code or that your `CLAUDE.md` already says. It does not save something every session. You can also say "remember that the API tests need a local Redis" and Claude saves it. To put a rule in the shared file instead, say "add this to CLAUDE.md".

- **Where.** One folder per repository: `~/.claude/projects/<project>/memory/`. It holds an index, `MEMORY.md`, and one file per topic. It is stored on your machine only, and is not shared with colleagues or other computers.
- **Size.** Only the first 200 lines or 25 KB of `MEMORY.md` load at the start of a session, whichever comes first. Claude reads the topic files when it needs them.
- **Correct or delete.** The files are plain text. Run `/memory`, choose the option that opens the auto memory folder, then edit or delete any file. A deleted note is forgotten.
- **Turn off.** Use the toggle in `/memory`, or set `"autoMemoryEnabled": false` in your Claude Code settings file (`~/.claude/settings.json`).

## Claude apps (claude.ai and desktop)

The apps can remember things from your chats. On a Team or Enterprise plan, this follows your organisation's settings: an Owner (the person who administers the organisation's Claude account) can switch memory off for everyone.

- **What is saved.** Topics such as your role, projects, and your communication and technical preferences. Sensitive topics (health, politics, religion) are saved only if you opt in. Government ID numbers, financial account numbers, criminal history and immigration status are never saved.
- **See, edit, delete.** Go to Settings, then Your Claude, and select "Manage" next to "Your memory". Open a topic to read it, use the edit icon to change it, or choose "Delete". You can also tell Claude in a chat to remember, change or forget something. "Reset memory" deletes everything, project memory included.
- **Pause.** In the same settings page, turn off "Generate memory from chats". Existing memory stays but is no longer used or added to.
- **One chat without memory.** Before your first message, click "+" and turn off "Memory". An incognito chat (ghost icon, outside a project) saves neither history nor memory. On a Team or Enterprise plan it can still appear in your organisation's data exports.
- **Projects** have their own memory plus their own instructions and files ([guide 1](1-using-claude.md)). Chats in a project use that project's memory and your memory from chats outside projects, not other projects'. Turn off "Use account memory" on the project page to keep a project fully separate.

On a Team or Enterprise plan, Owners cannot read members' individual memories.

## Worked example

You are a simulation engineer with one repository, `line-model`.

- **Belongs in the project `CLAUDE.md`:** "Run the model tests with `pytest tests/fast`. The full set in `tests/slow` takes 20 minutes; run it only before a release." Everyone on the repository needs it, and Claude cannot guess it.
- **Belongs in your personal file:** "Say what you are about to do in one sentence, then do it." It is about how you like to work, in every project.
- **Should be a skill** (a saved set of instructions that Claude loads only when a task needs it): a ten-step procedure for validating a conveyor model against a reference run. It is long, used occasionally, and only needed when you ask for it. A skill costs a short description every turn and loads its body only when used, while a long CLAUDE.md costs context on every turn ([guide 3](3-skills-and-plugins.md)).
- **Should not be written down:** the folder layout of `line-model`, or "the bug in `scheduler.py` was a wrong sign". Claude reads the layout from the code, and the fix lives in the git history. Notes like these go stale and then mislead.

## Learn more

- [How Claude remembers your project](https://code.claude.com/docs/en/memory.md)
- [Best practices](https://code.claude.com/docs/en/best-practices.md)
- [Use Claude's chat search and memory](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context)
- [Projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects)
