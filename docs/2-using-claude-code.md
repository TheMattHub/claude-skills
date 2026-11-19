# Using Claude Code

This page is for engineers who have never used Claude Code. After reading it you can install it, sign in, run a first session on one of your own projects, and work in the habits that give the best results.

Claude Code is Claude with access to your project folder. It reads your files, edits them, runs commands such as your tests, and works with git (the tool that records the history of your files), while you watch and approve. You describe what you want in plain language.

## Where it runs

All of these use the same engine, so your project settings and instruction files work in each:

- **Terminal**: the full command-line version (`claude`). This page uses it.
- **VS Code extension** (also Cursor) and **JetBrains plugin**: Claude Code inside your editor, with inline diffs (the lines Claude added and removed, shown in the file).
- **Desktop app**: the Code tab of the Claude desktop app, with visual diff review.
- **Web**: claude.ai/code, which runs in the cloud with no local setup.

## Install and sign in

You need a paid Claude plan (Pro, Max, Team or Enterprise) and a terminal. On Windows, [Git for Windows](https://git-scm.com/downloads/win) is recommended so Claude Code can use the Bash tool (a shell that runs commands); without it Claude Code uses PowerShell.

1. Open a terminal. On Windows PowerShell, the prompt starts with `PS C:\`.
2. Run the install command for your system.

   Windows PowerShell:

   ```powershell
   irm https://claude.ai/install.ps1 | iex
   ```

   macOS (also Linux and WSL):

   ```bash
   curl -fsSL https://claude.ai/install.sh | bash
   ```

   The command shows no progress while it downloads. This is normal.
3. Open a new terminal window and check the install:

   ```text
   claude --version
   ```

   You should see a version number followed by `(Claude Code)`. If your shell says `claude` is not found, the install folder is not on your PATH (the list of folders your shell searches for programs) yet; see the official [troubleshooting page](https://code.claude.com/docs/en/troubleshoot-install.md#command-not-found-claude-after-installation).
4. Go to a project folder and start Claude Code:

   ```text
   cd path/to/your/project
   claude
   ```

   On first use it asks you to sign in. Follow the prompts in your browser and choose your Claude account (the one with your paid plan). You are signed in once; later sessions start directly.

The package managers Homebrew (`brew install --cask claude-code`) and WinGet (`winget install Anthropic.ClaudeCode`) also work, but do not update themselves. The native install above updates in the background.

## A first session

A session is one run of Claude Code, from the moment you type `claude` until you exit. Use a project you know, ideally a copy or a branch (a separate line of work in git) where a mistake costs nothing.

1. **Ask a question.** Type:

   ```text
   what does this project do, and where is the main entry point?
   ```

   Claude reads the files it needs and answers. You do not have to attach anything.
2. **Ask for a small change.** For example:

   ```text
   add a short docstring to the main function
   ```

   Claude finds the file and shows the change before or as it makes it.
3. **Answer permission prompts.** Claude asks before it does something with side effects, such as editing a file or running a command. Choose Yes to allow it once, or one of the options that allow it for the session. Choose No and say what to do instead if you do not want it. Recent versions start in "auto" mode, where a separate safety check approves routine actions for you and you are asked less often. Press `Shift+Tab` to cycle the permission modes, including Manual, where you are asked before every edit and command.
4. **Review the diff** (the list of lines Claude added and removed). Ask `what files have I changed?`, or run `git diff` in another terminal, and read the change before you keep it. In the VS Code extension and the desktop app the diff is shown visually.
5. **Undo if needed.** `/rewind` (or `Esc` twice on an empty prompt) rolls the code and the conversation back to an earlier point.
6. **Leave.** Type `/exit`, or press Ctrl+D twice.

Type `/help` to list commands, or `/` to see the commands and skills available to you. A skill is a saved set of instructions for one kind of task, which Claude loads when your request matches it ([guide 3](3-skills-and-plugins.md)).

## Habits that matter most

- **Give the goal and the context, not only the task.** "Fix the login bug where users see a blank screen after entering wrong credentials" works better than "fix the bug". Name the file, describe the symptom, say what fixed looks like.
- **Ask for a plan before a large change.** Press `Shift+Tab` until plan mode is on, or type `/plan`. Claude then proposes an approach without changing files. Correct the plan, then let it build.
- **Let Claude run the tests.** Tell it the test command and ask it to run the tests and fix failures. A result it has checked is worth more than one it believes is right. Put the test command in your project's `CLAUDE.md` (a text file of standing instructions that Claude reads at the start of every session, see [guide 4](4-memory.md)) so you say it once.
- **Use `/clear` between unrelated tasks.** It starts a new conversation. A focused conversation gives better answers and costs less, because the next task does not carry the old one's history. `/resume` returns to the earlier conversation.
- **Commit often.** Each commit (a saved snapshot of your files in git) is a point you can return to with git. Claude can write the commit message: `commit my changes with a descriptive message`.

## When something goes wrong

| What happens | What to do |
| --- | --- |
| Claude goes in a wrong direction | Press `Esc` to stop it. Your work so far is kept. Restate the goal and what to avoid. After two failed corrections, `/clear` and write one better prompt. |
| It changed something you did not want | `/rewind`, or `git restore` for files you have not committed. |
| A skill does not trigger | Name it: type `/skill-name`, for example `/writing-course-handbooks` ([guide 3](3-skills-and-plugins.md)). |
| Too many permission prompts | Run `/permissions` to see and add allow rules (actions Claude may take without asking), or `/fewer-permission-prompts` to add rules for common read-only commands. |
| Claude ignores a rule in your `CLAUDE.md` | Run `/memory` to check the file is loaded, and keep it short ([guide 4](4-memory.md)). |
| Setup problems | Run `/doctor`. |

## Learn more

- [Quickstart](https://code.claude.com/docs/en/quickstart.md)
- [Overview, with every surface](https://code.claude.com/docs/en/overview.md)
- [Best practices](https://code.claude.com/docs/en/best-practices.md)
- [Common workflows](https://code.claude.com/docs/en/common-workflows.md)
- [Permission modes](https://code.claude.com/docs/en/permission-modes.md)
- [Commands reference](https://code.claude.com/docs/en/commands.md)
- [Terminal guide](https://code.claude.com/docs/en/terminal-guide), if you have not used a terminal before
- [Claude Code 101](https://academy.claude.com/courses/claude-code-101), a free course
