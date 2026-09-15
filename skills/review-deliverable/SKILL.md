---
name: review-deliverable
description: Run a structured QA pass on a client deliverable before you ship. Auto-fires on "/review-deliverable", "review this deck", "QA this deliverable", "second pair of eyes on", "is this ready to ship", "check this against the brief", "review my one-pager", or similar. Loads brand context from user-context.md and produces specific, location-tagged findings — not vague feedback.
---

<!-- OPENAI-ADAPTER:START -->
## OpenAI host binding

Before acting, read `../../references/openai-portability.md`. That file translates
host-specific tools, agents, artifacts, scheduling, connectors, and config-root
access for ChatGPT and Codex. It overrides concrete Claude/Cowork tool names only;
the workflow, safety gates, and output contract in this skill remain canonical.
<!-- OPENAI-ADAPTER:END -->


See `commands/review-deliverable.md` for the full review workflow.

## When this skill fires automatically

- User runs `/review-deliverable [path]` directly
- User asks: "review this deck", "QA this", "is this ready to ship", "second pair of eyes", "check this against the brief", "what would you change about this"
- User shares a Drive link or local path to a deliverable and asks for feedback
- User says "I just finished the [deck/doc/one-pager], can you take a look?"

## Pre-flight check

Before running the review, confirm `<config-root>/plugins/core-ops.user-context.md` exists. If it doesn't, route to `/setup-core` first — the review is much sharper with brand context loaded.

## What this skill is *not* for

- Strategy review or feedback on the underlying ideas. This is QA on the execution.
- Generating new deliverables from scratch. (For that, use the relevant Anthropic skill — `pptx`, `docx`, `xlsx`, etc.)
- Bulk reviews. One deliverable per invocation. For batches, run sequentially.
