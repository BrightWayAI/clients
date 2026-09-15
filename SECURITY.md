# Security Policy

## What this plugin does with your data

Client Success manages new-engagement setup, client-status drafting, and deliverable QA. It writes only user-owned local configuration and confirmed Cortex memory updates.

**Reads:**
- **Information from the user during the interview** (no automated reads).
- **Plugin references** — immutable `references/*.template.md` and `references/templates/*.md` starter files.
- **Working memory** (if Cortex is installed) — `<config-root>/memory/DASHBOARD.md` and relevant client/person nodes.
- **Shared private profile** — `<config-root>/memory/me/identity.md` and `voice.md` (read-only).

**Writes:**
- **Plugin settings** — `<config-root>/plugins/clients.user-context.md` and `clients-status.user-context.md`.
- **Template overrides** — `<config-root>/plugins/clients/templates/`.
- **Memory node** (only if Cortex is installed and the user confirms) — `<config-root>/memory/client/[client-name].md` plus a small entry in `DASHBOARD.md`.
- **Outputs in the conversation** — Drive folder structure (text only; user creates manually), Claude Project system prompt (copy-paste ready), phased project plan, immediate next step.

**Does not:**
- **Create Drive folders.** Outputs the structure for the user to create manually in their Drive.
- **Modify the Claude Project.** Outputs the system prompt for the user to paste at claude.ai.
- **Read or modify the SOW or contract files.** The interview asks the user to summarize; the plugin doesn't access contract files directly.
- **Send any data outside your machine** beyond what the user pastes into Cowork's conversation.

## Where data lives

- Immutable reference templates inside the installed plugin directory.
- User settings and template overrides under `<config-root>/plugins/`.
- Memory node at `<config-root>/memory/client/[client-name].md` (if Cortex is installed).
- Shared private profile (read-only) under `<config-root>/memory/me/`.

## What gets sent off your machine

- Nothing the plugin initiates. The user copy-pastes outputs (system prompt, folder structure) into other tools manually.

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Reporting a vulnerability

Report privately via GitHub Security Advisories:

https://github.com/BrightWayAI/delivery/security/advisories/new

Do not open a public issue for security concerns. We aim to respond within 5 business days.
