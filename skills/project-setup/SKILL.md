---
name: project-setup
description: Initialize a new client engagement end-to-end. Auto-fires only on explicit signals that a contract was signed or an engagement is starting — "new client just signed", "contract signed [for client]", "SOW is executed", "we just closed [client]", "onboard [client name] — they signed", "kickoff for [client], contract's in". Does not fire on ambiguous phrasing ("set up a new project", "new engagement", bare "kickoff"/"starting"/"beginning") — ask for confirmation or route to `/project-setup` explicitly instead. Produces Drive folder structure and, in the cortex client node (the public project record — not a Claude Project), the phased project plan with immediate next step and a memory node (if cortex is installed). Nothing writes before the single plan confirmation in Step 5.
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
- User states an explicit signed/starting signal: "new client just signed", "contract signed for [client]", "SOW is executed", "we just closed [client]", "[client]'s contract came back signed"
- Ambiguous phrasing alone ("set up a new project", "new engagement", bare "[client] kickoff" with no signature signal) does not auto-fire — confirm intent or point the user at `/project-setup` instead of guessing whether a contract exists

## Pre-flight check

Confirm `<config-root>/plugins/clients.user-context.md` exists with at least one offering configured. If missing, route to `/setup-projects` first — without an offerings catalog and template customizations, the outputs will be generic.

## What this skill is *not* for

- Updating an existing engagement. Initialization-only. Use `/recall [client]` for ongoing context.
- Generating SOWs/contracts. Bring those already signed.
- Project management. The phased plan is a starting point, not a tracking system.
