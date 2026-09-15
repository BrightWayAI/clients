---
description: Configure Client Success for offerings, drive layout, and companion-plugin integrations. Writes to `<config-root>/plugins/clients.user-context.md` using the shared vendor-neutral config-root resolver. Re-run anytime to add or update offerings.
---

# /setup-projects

Short interview that captures the catalog `/project-setup` needs to be useful for your firm.

**Quick path:** if the user wants minimum-viable defaults to start, write a placeholder `<config-root>/plugins/clients.user-context.md` with one generic "Consulting Engagement" offering. The plugin will work but outputs will be generic — recommend running the full interview when ready to capture real offerings.

---

## Step 0 — Resolve plugin config root

Resolve explicit override → `CORTEX_CONFIG_ROOT` → `~/.cortex/config-root` →
legacy pointer → default. Request access only to the resolved directory. If no root
has been intentionally configured, route to Cortex `/setup-identity` or the shared
configurator instead of creating a second pointer implementation here.

### Read shared identity

Read `<config-root>/memory/me/identity.md` (the canonical identity file populated by cortex's `/setup-identity`).

- **Exists and populated** → pre-fill Section 1 (Identity) of this interview from those values. Skip those questions; just confirm what you read.
- **Missing** → offer: "Want to capture name/company/role/tools once via `/setup-identity` (in cortex) so all marketplace plugins can read it? Or capture identity inline here only?" Route to `/setup-identity` if user prefers, then resume.

For the rest of this document, **`<config-root>`** refers to the resolved path. This plugin's config file lives at **`<config-root>/plugins/clients.user-context.md`**.

---

## Step 1 — Check for existing config

Read `<config-root>/plugins/clients.user-context.md`. Populated → ask whether to
update. If missing, check the former
`<config-root>/plugins/project-setup.user-context.md` path once and offer to import
it into the canonical Client Success file without deleting the old file. <!-- LEGACY_COMPAT -->

---

## Step 2 — The interview

### Section 1 — Identity
- Your name
- Your company
- One-sentence description of what your firm does
- Your role (Principal / Partner / Founder / etc.)

### Section 2 — Drive layout
- Where do you store active client work? (e.g., Google Drive shared drive name + path: "Active Clients")
- Naming convention for client folders (e.g., "[Client Name] — [Offering Short Name]")
- Any standardized subfolder structure beyond the defaults? (Defaults: 00_Contract, 01_Kickoff, 02_Discovery, 03_Deliverables, 04_Client Assets, 05_Meeting Notes, 06_Internal Working Docs)

### Section 3 — Offerings catalog

For each offering, capture:
- **Full name** (e.g., "AI Operating Model & Governance")
- **Short name** for folder/project labels (e.g., "AI Op Model")
- **Typical duration** (e.g., "6–8 weeks")
- **Phases** — usually 2–4. For each: name, goal (one sentence), typical week range
- **Offering-specific interview questions** — what questions do you ask clients during initialization that are unique to this offering?
- **Standard deliverables** — what outputs does this offering produce (named, not generic)?

Repeat for each offering. (If the user has 1 offering, that's fine. If 3+, work through them one at a time.)

After capturing, copy any customized templates to
`<config-root>/plugins/clients/templates/`. Bundled `references/templates/` files
are immutable defaults and are never edited at runtime.

### Section 4 — Communication defaults
- Default communication cadence (e.g., "weekly async update + biweekly sync")
- Default response time (e.g., "1 business day")
- Tools you typically use to communicate with clients (Email / Slack / Teams / etc.)

### Section 5 — Companion plugins
- Is `cortex` installed? (Y/N — drives whether memory node init runs in Output 4)
- Is `growth` installed? (Y/N — provides pipeline-analyst for periodic engagement reviews, and useful context when engagements originate in its signal pipeline; if not installed, note "Growth Engine not installed; pipeline analysis skipped")

---

## Step 3 — Write the config

Populate `<config-root>/plugins/clients.user-context.md`:

```markdown
# clients user context

_Last updated: [date]_

## Identity
- **Name:** ...
- **Company:** ...
- **What we do:** ...
- **Role:** ...

## Drive layout
- **Active Clients location:** ...
- **Naming convention:** ...
- **Standard subfolder structure:** ...

## Offerings
[For each offering — pulled from interview, also reflected in templates/project-plans.md and templates/drive-structure.md]
- **[Offering Full Name]** ([short name]) — [duration]
  - Phases: ...
  - Offering-specific questions: ...
  - Standard deliverables: ...

## Communication defaults
- **Cadence:** ...
- **Response time:** ...
- **Communication tools:** ...

## Companion plugins
- **cortex:** ...
- **ops:** ...
- **growth:** ...
```

---

## Step 4 — Create user-owned template overrides

Preview proposed copies of `project-plans.md` and `drive-structure.md` beneath
`<config-root>/plugins/clients/templates/`. Suggest specific edits based on the
offerings captured and write only after confirmation.

The immutable starter templates ship with three example offerings (AI Operating Model, Custom Agent Systems, Learning Production System). User-owned overrides can:
- Keep them if applicable
- Replace them with their own offerings
- Add additional offerings alongside

---

## Step 5 — Confirm and offer next step

Summarize. Offer:
> "Try `/project-setup` for your next client engagement."

---

## Behavior rules

- One section at a time.
- For Section 3 (offerings catalog), be patient — this is the most important section. The plugin is generic only if the offerings are well-captured.
- Idempotent — re-running adds new offerings or updates existing ones.
- Never edit bundled files in the installed plugin directory. All customizations live under `<config-root>/plugins/clients/`.
