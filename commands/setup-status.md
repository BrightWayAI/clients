---
description: Configure Delivery status drafting for cadence, voice match, user-owned template overrides, per-client rules, and delivery channel. Writes `<config-root>/plugins/delivery-status.user-context.md`. Re-run anytime to update.
---

# /setup-status

Short interview that captures what Delivery needs to draft useful client updates.

---

## Step 0 — Resolve plugin config root

Resolve explicit override → `CORTEX_CONFIG_ROOT` → `~/.cortex/config-root` →
legacy pointer → default. Request access only to the resolved directory. If no root
has been intentionally configured, route to Cortex setup instead of creating a
plugin-specific pointer.

### Read shared identity and voice

Read `<config-root>/memory/me/identity.md` (cortex's `/setup-identity`) and `<config-root>/memory/me/voice.md` (cortex's `/setup-voice`). If both are populated, you have most of what's needed for tone — only ask about cadence and delivery below. If missing, offer to run those commands first or proceed inline.

For the rest of this document, **`<config-root>`** refers to the resolved path. This plugin's status config lives at **`<config-root>/plugins/delivery-status.user-context.md`**.

If the canonical file is missing, check
`<config-root>/plugins/client-status.user-context.md` once and offer to import it
without deleting the old file. <!-- LEGACY_COMPAT -->

---

## Step 1 — Cadence and timing

- **Cadence** — weekly / bi-weekly / monthly (default weekly)
- **Day to send** — Friday afternoon / Monday morning / other (default Friday)
- **Time of day** — when do you typically have 30 min to review and send? (e.g., Friday 2pm)

---

## Step 2 — Status template

The plugin ships with an immutable starter at `references/templates/status-template.md`.
Customized copies live at
`<config-root>/plugins/delivery/templates/status-template.md`. The default structure:
What we did / What we learned / What's next / Anything we need from you.

Ask:
- Want to use the default template, or customize it now? (most users start default and refine over time)
- If customize: preview a user-owned copy, then write it after confirmation; never edit the bundled reference

---

## Step 3 — Per-client overrides (optional)

Some clients prefer different formats. Ask:
- Any clients that want a longer / shorter / different format? (capture per-client overrides)
- Any clients that should be EXCLUDED from automatic drafting? (e.g., a client who prefers no weekly updates)

If Delivery has configured engagements, walk through each active engagement to capture overrides.

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

Populate `<config-root>/plugins/delivery-status.user-context.md` per the template structure.

---

## Step 7 — Confirm and offer next step

Summarize. Offer:
> "Try `/client-status` Friday afternoon to see drafts for all active engagements."

---

## Behavior rules

- One section at a time.
- Skip what doesn't apply.
- Idempotent — re-running updates fields without resetting everything.
