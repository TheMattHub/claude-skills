# Skills and plugins

This page is for someone who uses Claude Code and wants to add skills to it. After reading it you can install a plugin from this marketplace, switch it off or update it, keep only the plugins you use, and write a first skill of your own.

## What the words mean

- **Skill**: a folder that contains a file named `SKILL.md`. The file holds instructions for one kind of task, for example how to write a handbook a learner can follow alone. It can also hold scripts and reference files.
- **Plugin**: a package that can contain skills and, optionally, commands, agents, hooks (commands that run automatically at set moments) and MCP servers (connections to outside tools). You install and remove a plugin as one unit.
- **Marketplace**: a catalogue of plugins. You add a marketplace once, then install plugins from it by name. This repository is a marketplace named `thematthub`.

## How Claude decides to use a skill

In every session Claude sees only the short description of each installed skill. When your request matches a description, Claude loads the full instructions and follows them. You can also call a skill yourself by typing `/` and its name, for example `/writing-course-handbooks`. A skill that comes from a plugin may also appear as `/plugin-name:skill-name`. Typing `/` lists what is available.

## Add this marketplace and install a plugin

Do this inside Claude Code.

1. Add the marketplace:

   ```text
   /plugin marketplace add TheMattHub/claude-skills
   ```

   Claude Code downloads the catalogue. Run `/plugin` and open the Marketplaces tab: `thematthub` is listed there.
2. Install a plugin:

   ```text
   /plugin install writing-toolkit@thematthub
   ```

   This does not install at once. It opens the plugin's details page. The "Will install" section lists the skills, hooks and servers it adds. Read it.
3. Choose where it applies. "Install for you (user scope)" gives you the plugin in every project on this machine. "Install for you, in this repo only" limits it to the current repository. "Install for all collaborators on this repository" enables it for everyone who works in the repository through the committed `.claude/settings.json`.
4. Read the install summary. `Plugin is now active.` means you can use it now. `Run /reload-plugins to apply.` means Claude Code reloads for you, or you run that command yourself.
5. Confirm: type `/` and look for the plugin's skills in the list, or in a shell run `claude plugin list`.

The same steps work from a shell: `claude plugin marketplace add TheMattHub/claude-skills`, then `claude plugin install writing-toolkit@thematthub`.

## Enable, disable, update, remove

Run `/plugin` and open the Installed tab. Select a plugin to open its menu: enable or disable, update now, or uninstall. Press Space to toggle the selected plugin. The same actions exist in a shell:

```text
claude plugin disable writing-toolkit@thematthub
claude plugin enable writing-toolkit@thematthub
claude plugin update writing-toolkit@thematthub
claude plugin uninstall writing-toolkit@thematthub
```

Marketplaces from third parties, including this one, do not update automatically by default. To get newer versions, update the plugin as shown above, or open the Marketplaces tab, select `thematthub`, and choose "Update marketplace". The new version loads in your next session, or after `/reload-plugins`. You can turn automatic updates on in the same Marketplaces tab. Removing the marketplace (`claude plugin marketplace remove thematthub`) uninstalls every plugin you installed from it.

## Install the few you will use

Every installed skill's description is sent with every request, whether or not you use the skill. Claude Code gives that list a budget of 1% of the model's context window (how much text it can hold in view at once). Over budget, it drops the descriptions of the least used skills, and Claude can no longer match your request to them. So install the two or three plugins you will use, check what they cost, and remove what you do not use after a few weeks:

- `/skill-doctor` shows what each skill costs, how often it was used, and which were never used.
- `claude plugin details writing-toolkit` (in a shell) shows the always-on token cost (tokens are the units in which Claude counts text) of one plugin and which skill contributes most.
- The Installed tab in `/plugin` groups plugins you have not used recently under "Not used recently".

## Write your own first skill

A skill is a folder with a `SKILL.md` file that starts with two fields between lines of three dashes: `name` (the folder name) and `description` (what the skill does and when to use it, with the words you would naturally say). The rest of the file is plain instructions. Put the folder under `.claude/skills/` in a project to share it with that project, or in your personal skills folder to use it everywhere. Claude Code finds it without a plugin. Keep the file short: once loaded, its text stays in the conversation, so every line has a recurring cost. The official [skills page](https://code.claude.com/docs/en/skills.md) has a full worked example and how to test that the skill triggers.

## A plugin runs with your permissions

A plugin is instructions plus scripts. Hooks and servers it contains run as programs on your computer with your user permissions, and skills change what Claude does with the tools it already has. Anthropic does not check what a third-party plugin contains. Install only plugins you trust, and read the "Will install" section on the details page first. To go deeper, clone the repository and read the plugin's `hooks/hooks.json`, `.mcp.json` and `bin/` folder. If auto-update is on, the files you reviewed can change later. To remove a plugin you no longer trust, run `claude plugin uninstall <plugin>@<marketplace>`.

## Learn more

- [Skills](https://code.claude.com/docs/en/skills.md)
- [Install and manage plugins](https://code.claude.com/docs/en/plugins/install.md)
- [Plugin commands reference](https://code.claude.com/docs/en/plugins/cli-reference.md)
- [Plugin security and trust](https://code.claude.com/docs/en/plugins/security.md)
- [Manage Claude Code plugins for your organization](https://code.claude.com/docs/en/plugins/org.md), for administrators
