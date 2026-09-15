---
name: client-status
description: Draft weekly client status updates per active engagement. Auto-fires on "/client-status", "draft my client updates", "weekly client updates", "status update for [client]", "send client updates", "client check-ins", or any phrase about producing client-facing status drafts. Pulls from cortex memory, Client Success config, calendar, and CRM. Drafts go for your review before sending.
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


See `commands/client-status.md` for the full workflow.

## When this skill fires

- User runs `/client-status` directly
- User says: "draft my client updates", "weekly client updates", "status update for [client]", "client check-ins"
- A scheduled task triggers this (common pattern: Friday 2pm or Monday 9am)

## Pre-flight

Confirm `<config-root>/plugins/clients-status.user-context.md` exists. If missing, route to `/setup-status`.

Best results use Cortex memory and Client Success engagement data. Without them, drafts work but are thinner.

## What this skill is NOT for

- Auto-send. Drafts only; user reviews and sends.
- Internal status reports. Client-facing only.
- Quarterly business reviews. Weekly cadence; QBRs are bigger artifacts.
