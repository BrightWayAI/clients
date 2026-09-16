---
disable-model-invocation: true
name: setup-projects
description: "Configure Client Success for offerings, drive layout, companion-plugin integrations, and a derived SOW format template. Writes to `<config-root>/plugins/clients.user-context.md` and `<config-root>/plugins/clients.sow-template.md` using the shared vendor-neutral config-root resolver. Re-run anytime to add or update offerings; `--add-sample` merges a second SOW sample."
---

# setup-projects

Read `../../references/openai-portability.md`, then read
`../../commands/setup-projects.md` completely and follow it as the canonical workflow.
Treat `/setup-projects`, `$setup-projects`, natural-language activation, and the ChatGPT plugin
mention as equivalent entrypoints. Ignore Claude-only tool allowlists and model names;
apply the capability translation and degradation rules from the portability contract.

Do not duplicate or reinterpret the command here. Preserve its confirmation gates,
draft-only boundaries, file locations, and output contract.
