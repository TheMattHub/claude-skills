# Using Claude

This page is for someone who has just started using Claude. After reading it you can open Claude, ask for what you need in a way that gets a good first answer, set up a project for recurring work, and check what Claude gives you before you rely on it.

## Where Claude runs

Claude runs in your web browser at claude.ai, in desktop apps for macOS and Windows, and in mobile apps for iOS and Android. You sign in with the same account everywhere. The desktop app also contains Claude Code, the version of Claude that works on files and code on your computer. [Guide 2](2-using-claude-code.md) covers it.

## How to ask well

Claude cannot see what is in your head or on your screen. It only has what you type and attach. These habits give the biggest improvement:

- **Say the goal, not only the task.** "Summarise this report" gets a generic summary. "Summarise this report in five lines for a manager who decides on Friday whether to fund phase two" gets a useful one.
- **Give the context.** Say who the reader is, what the project is, and what constraints apply.
- **Say what a good answer looks like.** Give the length, the format (a table, a list, an e-mail) and the tone.
- **Attach the file instead of describing it.** Attach the spreadsheet, the log or the draft. Claude reads it, which is more accurate than your description of it.
- **Say what you already tried.** This stops Claude from suggesting it again.
- **Let Claude ask you.** If the task is unclear, add "Ask me questions first if you need more information." Claude then asks before it writes.

If the first answer is not right, say what is wrong and what you want instead. Claude adjusts. Starting a new conversation for an unrelated task keeps the old one from interfering.

## Projects

A project is a workspace for recurring work. It holds instructions that apply to every conversation in it, and files (the project knowledge) that Claude can use in every conversation in it. Use one when you often ask Claude about the same material, for example the documents of one client or the template of a weekly report.

To create one, open Projects at claude.ai/projects and select "+ New Project". Add a name, then write the project instructions and upload the files. On a Team or Enterprise plan, you choose whether the project is private or shared with your organisation, and you select "Share project" to add colleagues by name or e-mail, with either "Can view" or "Can edit" access. Context from one conversation does not carry into another unless it is in the project knowledge.

## What Claude can produce besides chat

- **Files.** Claude can create Excel (.xlsx), PowerPoint (.pptx), Word (.docx) and PDF files, and plain text files such as .csv, .md and .html. You download them from the conversation. The feature is called "Create and edit files" (in some layouts "Code execution and file creation") under Settings, then Capabilities. On a Team or Enterprise plan, an Owner (the person who administers the organisation's Claude account) can turn it off for everyone, so if you do not see it, ask your Owner. File creation uses more of your usage allowance than ordinary chat, and files are limited to 30 MB.
- **Artifacts.** An artifact is an interactive page or tool that Claude builds from your description and opens beside the conversation: a tracker, a quiz, a document, a set of slides. Describe what you need, answer Claude's questions, then ask it to build it as an artifact. Each artifact has its own link. Select Share to give teammates access. Viewers see the artifact but not your conversation.

## Connectors

A connector lets Claude read from and act in another tool you use. Claude can reach only what your own account can reach in that tool. On a Team or Enterprise plan, an Owner first adds the connector in Organization settings, and then each member connects with their own account. On a personal plan you connect it yourself. To connect, open the "+" menu in a chat, hover over "Connectors", select "Manage connectors" and follow the sign-in prompts. A connector can also change data, so connect only services you trust and need, and disconnect the ones you stop using.

## Check what Claude gives you

Claude can be wrong, and it sounds equally sure when it is. Before you rely on an answer:

- Ask where a claim comes from, and open the source yourself.
- Recompute numbers that matter. Do not trust a figure you could not reproduce.
- Read generated files in full before you send them on.
- Keep confidential material within what your organisation allows. Ask your administrator what may be shared with Claude and with each connector.
- Be careful with files or web pages from unknown sources. They can contain hidden instructions meant to steer Claude.

## Choosing a model and effort

In the Claude apps, select the model name next to the send button to change the model. Select "Effort" in the same menu to change how much work Claude puts into an answer. A stronger model or a higher effort gives more thorough answers but takes longer and uses more of your usage allowance, so you reach your limit sooner. Each model marks a default effort level. Use the default for daily work, and raise it for a hard problem you have already seen the default fail on.

## Learn more

- [Create and edit files with Claude](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude)
- [How can I create and manage projects?](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects)
- [Use connectors to extend Claude's capabilities](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)
- [Change the model, effort, and thinking settings](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings)
- [Use artifacts](https://academy.claude.com/tutorials/use-artifacts-to-visualize-and-create-ai-apps-without-ever-writing-a-line-of-code)
- [Claude Academy](https://academy.claude.com/): free self-paced courses
