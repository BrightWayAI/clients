---
name: setup
description: Configure project-setup for your offerings, drive layout, and companion plugins. Auto-fires on "/setup-projects", "set up project-setup", "configure my offerings", "add a new offering", or when /project-setup reports user-context.md is missing.
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


See `commands/setup-projects.md` for the full interview.

## When this skill fires

- User runs `/setup-projects` directly
- User says: "set up project-setup", "configure my offerings", "add a new offering", "update my project templates"
- The `/project-setup` command reports user-context.md is missing → auto-route here

## Quick path

If the user wants minimum-viable defaults to start: write a placeholder `<config-root>/plugins/project-setup.user-context.md` with one generic "Consulting Engagement" offering. The plugin will work but outputs will be generic. Recommend running the full interview when ready to capture real offerings.
