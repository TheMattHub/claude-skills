---
runs: 2
model: sonnet
max_turns: 8
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
---

I am designing a digital twin app. Its model file (YAML, shared between teams by email) will contain the OPC UA connection: url opc.tcp://10.1.4.20:4840, user, password, and the node ids to read. The twin will also write its recommended setpoints back to the PLC through OPC UA. The plant MQTT broker is on port 1883 without TLS and I plan to send the broker password to it. Give me your design review with what you would change.
