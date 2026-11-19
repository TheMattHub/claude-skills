# repo-publishing

Two skills for getting a repository public and keeping its releases tidy.

- **open-source-repo-publication**: audits git history for secrets and personal data, publishes a clean history through a new repository, and adds LICENSE, README, CONTRIBUTING, security policy and CI. Example: "Make this private repo safe to open-source."
- **releasing-a-repo**: bumps the version, tags, and opens a DRAFT GitHub release with short notes; you publish it yourself. Example: "Prepare release 0.7.2."

## Requirements

- git
- the GitHub CLI (`gh`), logged in

## Operating system

Not tied to one operating system. The skills mention credential-cache troubleshooting and screenshot tooling; check the commands against your own system.

## Install

```text
/plugin install repo-publishing --marketplace TheMattHub/claude-skills
```
