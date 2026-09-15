# delivery

Client engagement lifecycle for Claude (Cowork + Claude Code): start, status, QA.

The plugin covering the full arc of a client engagement — from kickoff through
weekly status updates to shipping a reviewed deliverable. Renamed from
`project-setup`, 2026-09-15 — absorbs the retired `client-status` plugin and
core-ops's `/review-deliverable`.

## What it does

- **`/project-setup`** — a new client signs, you run this. Interviews you about
  the engagement and generates: Drive folder structure, a Claude Project system
  prompt, a phased project plan with an immediate next step, and (if
  `claude-cortex` is installed) a memory node so every future session has
  context from day one.
- **`/client-status`** — drafts a weekly client-facing status update from
  recent activity.
- **`/review-deliverable`** — a structured QA pass on a client deliverable
  (deck, doc, spreadsheet, one-pager) against your brand guide and the
  original brief. Returns location-tagged findings ranked by severity, plus a
  ship/no-ship verdict.

## Install

Recommended: via the [BrightWayAI marketplace](https://github.com/BrightWayAI/nucleus).

```
/plugin marketplace add BrightWayAI/nucleus
/plugin install delivery@nucleus
```

## First-time setup

Run `/setup-projects`. Captures:

- **Identity** — you, your company, what you do
- **Offerings** — your service offerings, with names, durations, and which template applies to each
- **Drive layout** — where Active Clients lives, naming conventions, folder structure preferences
- **Memory** — whether claude-cortex is installed (drives whether memory init runs)
- **Communication defaults** — your default cadence for client comms

Run `/setup-status` to configure `/client-status`.

`/review-deliverable` reads brand/CRM config from `core-ops.user-context.md`
cross-plugin (same pattern `relationships` uses) — no separate setup step.

Saved to `<config-root>/plugins/delivery.user-context.md` and
`<config-root>/plugins/delivery-status.user-context.md`.

## Customizing templates

The plugin ships with **starter templates** in `references/templates/`:

- `drive-structure.md` — folder layouts per offering
- `claude-project-prompt.md` — the system-prompt template
- `project-plans.md` — phased delivery plans per offering
- `status-template.md` — weekly status update structure

Copy any template you want to customize into
`<config-root>/plugins/delivery/templates/`. Bundled references remain immutable.

## Companion plugins

- **claude-cortex** — for memory node initialization. If not installed, `/project-setup` skips that output.
- **core-ops** — provides `pipeline-analyst` for reviewing recently-signed deals, and brand/CRM config that `/review-deliverable` reads.

Works without them.

## What's inside

```
.claude-plugin/plugin.json
commands/
  project-setup.md           New-engagement interview + generation workflow
  setup-projects.md          Plugin configuration interview
  client-status.md           Weekly client status draft
  setup-status.md            Client-status configuration interview
  review-deliverable.md      Deliverable QA pass
skills/
  project-setup/SKILL.md     Auto-fires on new-engagement phrases
  setup-projects/SKILL.md    Auto-fires on setup phrases
  client-status/SKILL.md     Auto-fires on status-update phrases
  setup-status/SKILL.md      Auto-fires on client-status setup phrases
  review-deliverable/SKILL.md Auto-fires on QA/review phrases
references/
  user-context.template.md              Project-setup config structure (committed)
  client-status-user-context.template.md Client-status config structure (committed)
  templates/
    drive-structure.md       Folder layouts (committed; user-editable)
    claude-project-prompt.md System prompt template
    project-plans.md         Phased plans per offering
    status-template.md       Weekly status update structure
```

<!-- OPENAI-SUPPORT:START -->
## ChatGPT and Codex

Delivery ships as a native OpenAI plugin as well as a Claude plugin. In
ChatGPT desktop Local Work, enable **Delivery** and ask naturally or mention
`@Delivery`. In Codex, use natural language or the namespaced skills exposed
by the plugin. Claude slash-command names in this README remain workflow aliases.

All hosts resolve the same `<config-root>` used by Cortex, so Claude, ChatGPT desktop,
and Codex can share identity, voice, memory, and per-plugin settings without copying
them. The installed plugin directory is read-only at runtime. See
[`references/openai-portability.md`](references/openai-portability.md) for capability
mapping, connector checks, permissions, and honest degraded behavior.

Import the full catalog from
[`BrightWayAI/nucleus`](https://github.com/BrightWayAI/nucleus); Nucleus is the master
marketplace, while each plugin remains independently installable.
<!-- OPENAI-SUPPORT:END -->


## License

MIT.
