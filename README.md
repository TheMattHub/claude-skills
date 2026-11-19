# Claude skills

A catalogue (a "marketplace") of plugins for Claude Code, Anthropic's coding assistant. Each plugin adds skills: short instruction sets that make Claude work in a way we found reliable on real simulation, operations research and industrial automation projects.

If you have never used Claude Code, plugins or skills, start with the guides under [New to Claude?](#new-to-claude) and come back here.

## Example

Here is what a plugin does for you. With `thematthub-writing-toolkit` (the first plugin in the table below) installed, you type:

```text
Write the day-one setup guide for the course participants. They install the simulator and run the first model on their own.
```

Claude recognises that the request matches the skill `writing-course-handbooks`. It then writes for a reader who cannot ask you questions: every term is explained before it is used, every step shows the exact command and what the reader should see afterwards, and the guide ends with a table of what to do when a step fails.

## Quick start

You need Claude Code installed and signed in ([guide 2](docs/2-using-claude-code.md) shows how). Then, inside Claude Code, type:

```text
/plugin marketplace add TheMattHub/claude-skills
```

Claude Code adds the marketplace, which is named `thematthub`. Run `/plugin` and open the Marketplaces tab to see it listed. Then install one plugin:

```text
/plugin install thematthub-writing-toolkit@thematthub
```

Claude Code opens a details page for the plugin. Read it, choose "Install for you (user scope)", and the plugin is active. Type `/` to see its skills in the list.

The same commands work in a shell: `claude plugin marketplace add TheMattHub/claude-skills`, then `claude plugin install thematthub-writing-toolkit@thematthub`.

The plugin folders' own READMEs use a one-step form that adds the marketplace and installs in one command: `/plugin install <name> --marketplace TheMattHub/claude-skills`. It needs Claude Code 2.1.275 or later.

## Plugins

| | Plugin | What it helps with | Who should install it |
| --- | --- | --- | --- |
| <img src="plugins/thematthub-writing-toolkit/.claude-plugin/icon.png" width="40" alt=""> | `thematthub-writing-toolkit` | Writing texts a reader can follow without you: handbooks, documentation sites, research papers, Italian texts, competitor analyses | Everyone who writes reports, guides or papers |
| <img src="plugins/thematthub-repo-publishing/.claude-plugin/icon.png" width="40" alt=""> | `thematthub-repo-publishing` | Turning a private repository into a safe public release, and cutting versioned releases with draft notes | Anyone who publishes code |
| <img src="plugins/thematthub-web-pages/.claude-plugin/icon.png" width="40" alt=""> | `thematthub-web-pages` | Building shareable HTML pages (dashboards, viewers, monitors, reports) and choosing interface colours that are validated instead of eyeballed | Anyone who builds dashboards or viewers |
| <img src="plugins/thematthub-docs-export/.claude-plugin/icon.png" width="40" alt=""> | `thematthub-docs-export` | Exporting a project's markdown documentation to Word and PDF, with your own templates and rendered Mermaid diagrams | Anyone who sends documentation to clients or colleagues. Written for Windows |
| <img src="plugins/thematthub-plant-data/.claude-plugin/icon.png" width="40" alt=""> | `thematthub-plant-data` | Connecting apps, simulations and digital twins to plant systems (OPC UA, MQTT, MES, historians) safely | Simulation and automation engineers |
| <img src="plugins/thematthub-llm-integration/.claude-plugin/icon.png" width="40" alt=""> | `thematthub-llm-integration` | Adding language-model calls to an app: provider-agnostic client, validated JSON output, local models, a fake for tests | Developers who build apps that call a model |
| <img src="icons/thematthub-decks.png" width="40" alt=""> | `thematthub-decks` | Making presentations: brief and structure, design in Claude Slides, finishing in PowerPoint, company templates | Anyone who builds slide decks. The PowerPoint steps need Windows with desktop PowerPoint |
| <img src="icons/thematthub-naga.png" width="40" alt=""> | `thematthub-naga` | Running a simulation study for a decision (how many machines, staff or docks; will a change cope with demand) with the Naga engine | Anyone with a capacity or what-if question. Needs Python and the engine: `pip install "nagasim[mcp]"` |

The last two live in their own repositories and are only listed here, so installing them fetches from those repositories:

- `thematthub-decks` comes from [TheMattHub/decks](https://github.com/TheMattHub/decks). Its skill appears as `decks:making-presentations`, because the plugin keeps its own name inside. Its scripts drive the PowerPoint installed on your machine, and `uv` downloads their Python packages on first run; its README lists the requirements.
- `thematthub-naga` takes the `simulation-study` skill from [TheMattHub/naga](https://github.com/TheMattHub/naga) (Apache-2.0) and follows that repository's main branch. While the plugin is enabled, Claude Code starts the engine's tool server on your machine in every session (`naga mcp --tools study --root <your project folder>`). The server reads and writes model and study files only inside that folder, and network access is off. If the `naga` command is not installed, `/mcp` shows the plugin's server as failed to connect until you install the engine; the skill still loads. Keep the engine up to date (`pip install -U "nagasim[mcp]"`) so it matches the skill.

## Which ones should I install first?

Install the few plugins you will use: `thematthub-writing-toolkit` plus one that matches your work is a good start. Claude reads the short description of every installed skill on every request, so each plugin costs a little context (the text Claude holds in view) on every turn. Run `/skill-doctor` or `claude plugin details <plugin>` to see the cost, and after a few weeks remove what you did not use. [Guide 3](docs/3-skills-and-plugins.md) explains how.

The `thematthub-` prefix is there because plugin names are global in Anthropic's official directory, so these carry the owner's name.

## Official plugins worth adding

These come from Anthropic's official marketplace, which Claude Code already knows, so there is no marketplace to add first.

| Plugin | What it gives you | What it costs |
| --- | --- | --- |
| `superpowers` | A plan-first way of working: `brainstorming` (clarify a request before building), `writing-plans` (turn it into a step-by-step plan), `systematic-debugging` (find the root cause before fixing), and twelve more skills | About 850 tokens in every session for 15 skills, plus a session-start hook that tells Claude to look for a matching skill before each task. |
| `frontend-design` | Design guidance for web interfaces. The `thematthub-web-pages` skills use it when it is installed | One skill |

```text
/plugin install superpowers@claude-plugins-official
```

## New to Claude?

Four short pages, each readable on its own:

- [Using Claude](docs/1-using-claude.md): the Claude apps, asking well, projects, files and artifacts, connectors, checking the answers.
- [Using Claude Code](docs/2-using-claude-code.md): install, a first session, and the habits that matter most.
- [Skills and plugins](docs/3-skills-and-plugins.md): what they are, how to install, update and review them, and how to write your own.
- [Memory](docs/4-memory.md): what Claude remembers between sessions, where it is stored, and what to write in a `CLAUDE.md`. A starter file to copy is in [docs/starter-CLAUDE.md](docs/starter-CLAUDE.md).

## Sharing with a team

To offer this marketplace to everyone who works in one repository, add these keys to that repository's `.claude/settings.json` (create the file if it does not exist):

```json
{
  "extraKnownMarketplaces": {
    "thematthub": {
      "source": { "source": "github", "repo": "TheMattHub/claude-skills" }
    }
  },
  "enabledPlugins": { "thematthub-writing-toolkit@thematthub": true }
}
```

People who open the repository and accept Claude Code's trust dialog get the marketplace. Each person still runs `claude plugin install thematthub-writing-toolkit@thematthub --scope project` once, because the setting marks the plugin as enabled for the project, but each person's Claude Code downloads it only on install. On a Team or Enterprise plan, an Owner (the person who administers the organisation's Claude account) can also provision plugins from the claude.ai organisation settings; see [Manage Claude Code plugins for your organization](https://code.claude.com/docs/en/plugins/org.md).

## Reporting a problem or proposing a change

Open an issue on this repository. Before a pull request, run both checks and fix what they report:

```text
python -I tools/check_repo.py
claude plugin validate . --strict
```

## Licence and credits

[MIT](LICENSE). The two plugins listed from other repositories carry their own licences (`decks`: MIT; `naga`: Apache-2.0).
