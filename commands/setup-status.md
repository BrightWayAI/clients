---
description: Configure client-status for your cadence, voice match, status template, per-client overrides, and delivery channel. Re-run anytime to update.
---

# /setup-status

Short interview that captures what client-status needs to draft useful updates.

---

## Step 0 — Resolve plugin config root

Per-plugin config in this marketplace lives under a user-chosen folder, recorded at `~/Documents/.claude-plugin-config-root` (single-line text file in the user's home).

### A — Try the pointer

Ensure access to `~/Documents`. In Cowork, call `request_cowork_directory(~/Documents)` once if not already granted. In Claude Code (or any environment with direct filesystem access), no mount is needed. Then read `~/Documents/.claude-plugin-config-root`.
- **Exists**: read line 1 → that's the config root path. Ensure access to `<config-root>`. If running in Cowork and the folder isn't already mounted in this session, call `request_cowork_directory(<config-root>)`. If running in Claude Code or another environment with direct filesystem access, no mount call is needed. Skip to section C.
- **Missing**: continue to section B.

### B — First-time bootstrap

Prompt: "First-time plugin setup. Where should I store your plugin config — identity, voice, and per-plugin settings? Pick a folder you control (e.g., `~/Documents/Claude/` or `~/Documents/PluginConfig/`). The folder will hold `identity.md`, `voice.md`, and a `plugins/` subdirectory."

Then:
1. Ensure access to `<path>`. If running in Cowork and the folder isn't already mounted in this session, call `request_cowork_directory(<path>)`. If running in Claude Code or another environment with direct filesystem access, no mount call is needed. Create `<path>/plugins/`. Write absolute path to `~/Documents/.claude-plugin-config-root`.

### C — Read shared identity and voice

Read `<config-root>/memory/me/identity.md` (cortex's `/setup-identity`) and `<config-root>/memory/me/voice.md` (cortex's `/setup-voice`). If both are populated, you have most of what's needed for tone — only ask about cadence and delivery below. If missing, offer to run those commands first or proceed inline.

For the rest of this document, **`<config-root>`** refers to the resolved path. This plugin's config file lives at **`<config-root>/plugins/client-status.user-context.md`**.

---

## Step 1 — Cadence and timing

- **Cadence** — weekly / bi-weekly / monthly (default weekly)
- **Day to send** — Friday afternoon / Monday morning / other (default Friday)
- **Time of day** — when do you typically have 30 min to review and send? (e.g., Friday 2pm)

---

## Step 2 — Status template

The plugin ships with a starter template at `references/templates/status-template.md`. The default structure: What we did / What we learned / What's next / Anything we need from you.

Ask:
- Want to use the default template, or customize it now? (most users start default and refine over time)
- If customize: walk through which sections to add/remove/reorder

---

## Step 3 — Per-client overrides (optional)

Some clients prefer different formats. Ask:
- Any clients that want a longer / shorter / different format? (capture per-client overrides)
- Any clients that should be EXCLUDED from automatic drafting? (e.g., a client who prefers no weekly updates)

If user has `project-setup` installed and wants to use those engagements, walk through each active engagement to capture overrides.

---

## Step 4 — Optional inclusions

- **Time-tracking hours** — if `time-tracking` plugin is installed, do you want hours logged per client included in the update? (Y/N, default N — most clients don't need that level of transparency)
- **Thought-leadership shares** — should drafts include a "relevant share" section (an article / framework / insight tied to their work)? (Y/N, default N)
- **Auto-send** — leave default off. The plugin always drafts and waits for review. (Documented for clarity, not configurable.)

---

## Step 5 — Delivery channel

- **Channel** — email (default) / Slack DM / client portal / Drive folder upload / other
- **Per-client channel overrides** — some clients prefer different channels

---

## Step 6 — Write config

Populate `<config-root>/plugins/client-status.user-context.md` per the template structure.

---

## Step 7 — Confirm and offer next step

Summarize. Offer:
> "Try `/client-status` Friday afternoon to see drafts for all active engagements."

---

## Behavior rules

- One section at a time.
- Skip what doesn't apply.
- Idempotent — re-running updates fields without resetting everything.
