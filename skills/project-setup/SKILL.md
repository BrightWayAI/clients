---
disable-model-invocation: true
name: project-setup
description: Initialize a new client engagement end-to-end. Auto-fires on "/project-setup", "set up a new project", "new client just signed", "onboard [client name]", "get [client] set up", "new engagement", "contract signed", "initialize [client] project", or any variation where the user is starting work with a new client. Also fires on client name + words like "kickoff", "starting", or "beginning". Produces Drive folder structure, Claude Project system prompt, phased project plan with immediate next step, and a memory node (if claude-cortex is installed).
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


See `commands/project-setup.md` for the full workflow.

## When this skill fires

- User runs `/project-setup` directly
- User says: "set up a new project", "new client just signed", "onboard [client]", "[client] kickoff", "starting work with [client]", "new engagement", "contract signed for [client]"
- User mentions a new client name with starting/kickoff/beginning words

## Pre-flight check

Confirm `<config-root>/plugins/delivery.user-context.md` exists with at least one offering configured. If missing, route to `/setup-projects` first — without an offerings catalog and template customizations, the outputs will be generic.

## What this skill is *not* for

- Updating an existing engagement. Initialization-only. Use `/recall [client]` for ongoing context.
- Generating SOWs/contracts. Bring those already signed.
- Project management. The phased plan is a starting point, not a tracking system.
