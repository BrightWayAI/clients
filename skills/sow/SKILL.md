---
name: sow
description: "Turn a proposal into a finished Statement of Work in your house format, derived from a sample you provided via `/setup-projects`. Flags — `--client <slug>` `--phase <label>` `--amendment`."
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


# sow

Read `../../references/openai-portability.md`, then read
`../../commands/sow.md` completely and follow it as the canonical workflow.
Treat `/sow`, `$sow`, natural-language activation, and the ChatGPT plugin
mention as equivalent entrypoints. Ignore Claude-only tool allowlists and model names;
apply the capability translation and degradation rules from the portability contract.

Do not duplicate or reinterpret the command here. Preserve its confirmation gates,
draft-only boundaries, file locations, and output contract.
