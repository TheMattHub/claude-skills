# plant-data

One skill for software that touches plant or industrial data.

`connecting-to-plant-data` covers how to:

- read live data from OPC UA, MQTT/Sparkplug B, REST, MES, SQL, historians or PLC tag servers (Kepware);
- keep hosts and credentials out of model files, config files and agent tools;
- bound and validate what a server sends before using it;
- send recommendations back through an operator-owned outbox instead of writing setpoints;
- review such a connector for security.

Example request: "My digital twin must read tags from our OPC UA server and suggest setpoints. How do I connect it safely?"

## Requirements

None. It is guidance for Claude.

## What it reads, writes and runs

- Instructions only; the plugin contains no scripts and no hooks.
- It connects to nothing by itself. It has no network access of its own and stores no credentials.
- Any code Claude writes for you with this skill runs with your credentials and your network access, so read it before you run it, and test against a fake or loopback server first.
- Writes to plant systems are proposed for a person to confirm. The skill tells Claude to produce recommendations as records for an operator to review, not to send setpoints or commands.

## Install

```text
/plugin install plant-data --marketplace TheMattHub/claude-skills
```
