---
disable-model-invocation: true
name: setup-status
description: "Configure Client Success status drafting for cadence, voice match, user-owned template overrides, per-client rules, and delivery channel. Writes `<config-root>/plugins/clients-status.user-context.md`. Re-run anytime to update."
---

# setup-status

Read `../../references/openai-portability.md`, then read
`../../commands/setup-status.md` completely and follow it as the canonical workflow.
Treat `/setup-status`, `$setup-status`, natural-language activation, and the ChatGPT plugin
mention as equivalent entrypoints. Ignore Claude-only tool allowlists and model names;
apply the capability translation and degradation rules from the portability contract.

Do not duplicate or reinterpret the command here. Preserve its confirmation gates,
draft-only boundaries, file locations, and output contract.
