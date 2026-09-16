---
description: Initialize a new client engagement end-to-end. Interviews you about the engagement, then produces Drive folder structure, Claude Project system prompt, phased project plan with immediate next step, and (if cortex is installed) a memory node so future sessions have context from day one.
---

# /project-setup

End-to-end client engagement initialization. A new client signs → run this command → 5 minutes later you have everything you need to start delivering.

---

## Step 0 — Preflight

Read `<config-root>/plugins/clients.user-context.md`. If missing, route to `/setup-projects` and stop.

Extract:
- Identity (your name, company, what you do)
- Offerings catalog (your service offerings, with names and durations)
- Drive layout (where Active Clients lives, naming conventions)
- Companion plugins (cortex installed → run memory init; ops installed → can pull pipeline context)
- Communication defaults (default cadence, response time)

Read user-owned template overrides when present, otherwise the bundled defaults:
- `<config-root>/plugins/clients/templates/drive-structure.md` → fallback `references/templates/drive-structure.md`
- `<config-root>/plugins/clients/templates/claude-project-prompt.md` → fallback `references/templates/claude-project-prompt.md`
- `<config-root>/plugins/clients/templates/project-plans.md` → fallback `references/templates/project-plans.md`

Bundled defaults:
- `references/templates/drive-structure.md`
- `references/templates/claude-project-prompt.md`
- `references/templates/project-plans.md`

Installed plugin files are read-only. User-owned overrides are the structural source
of truth when present; otherwise use bundled defaults.

---

## Outputs you will produce

1. **Google Drive folder structure** (you tell the user to create manually)
2. **Claude Project system prompt** (copy-paste ready)
3. **Phased project plan + single immediate next step** (offer to execute it)
4. **Memory node initialization** (only if cortex is installed)

---

## Phase 1 — Interview

Run conversationally. Don't dump all questions at once — group them, ask follow-ups, keep it human. If the user already shared context in the conversation, pull from it rather than re-asking.

Work through these groups in order. Mark each complete before moving on.

### Group 1: The basics
- Client organization name
- Primary contact: name, title, email
- Which of your offerings? (use offerings from user-context)
- Engagement start date and target end (or duration)
- Deal name in your CRM (for linking, if applicable)

### Group 2: Scope & deliverables
- Key deliverables per the SOW — ask the user to summarize or paste
- Total contract value (optional — informs prioritization)
- What problem is the client trying to solve? (in their words if possible)
- **If no SOW exists yet but a proposal does** — offer to chain into `/sow` right after this interview finishes, to produce the SOW before generating the rest of the outputs below. If the user accepts, run `/sow` (passing `--client <slug>` for this engagement) and use its output as the source of truth for deliverables/timeline/pricing in Outputs 1–3.

### Group 3: Context
- What's known about the client's org, culture, AI maturity (or whatever's relevant to your offering)
- Known risks, sensitivities, landmines
- Hard deadlines or external dependencies beyond engagement end
- Any contractors or collaborators involved? Who?

### Group 4: Communication
- Client's preferred communication style and cadence
- Tools or platforms the client uses that you'll need access to

### Group 5: Offering-specific questions
For each offering selected, ask the offering-specific questions documented in `references/templates/project-plans.md` for that offering. (User customizes which questions per offering during `/setup-projects`.)

If the user picks multiple offerings, blend the offering-specific questions and produce a combined project plan.

---

## Phase 2 — Generate outputs

After the interview, produce all outputs in a single response. Use the templates as the structure. Populate every field with real engagement data — no unfilled placeholders.

### Output 1: Drive folder structure

Present the folder tree clearly. Tell the user to create this manually in their Active Clients shared drive (or wherever their `drive-active-clients-path` from user-context says).

Use `references/templates/drive-structure.md` as the source. Adapt the offering-specific Folder 02 to match the active offering(s).

### Output 2: Claude Project system prompt

Generate a complete, copy-paste-ready system prompt using `references/templates/claude-project-prompt.md` as the structure. Replace every bracketed field with real data. Remove sections that are empty or not applicable — never leave placeholder text.

After presenting the system prompt, include this instruction:

> **To set up the Claude Project:** claude.ai → Projects → New Project → name it "[Client Name] — [Offering Short Name]" → paste this as the project instructions → upload the SOW and any relevant client documents as project files.

### Output 3: Project plan + immediate next step

Generate a phased delivery plan tailored to the active offering, using `references/templates/project-plans.md` as the source. Adjust week numbers based on the actual engagement timeline.

**Format for each phase:**
- Phase name and goal (one sentence)
- Key tasks (3–6 bullets)
- Estimated timeline (weeks, based on what the user shared)
- Primary owner (You / Client / Shared)

**After the project plan, surface a single Immediate Next Step:**
- The one thing to do in the next 24 hours
- Make it specific: name the person, the action, the channel
- Example: "Send the kickoff prep email to [Name] — want me to draft it now?"
- Offer to execute it if it's something Claude can help with (draft email, generate agenda, etc.)

### Output 4: Memory node initialization

**Only if `cortex` is installed** (per user-context).

Memory lives at `<config-root>/memory/`. Create the node file at `<config-root>/memory/client/[client-name-lowercase].md` using this structure:

```markdown
# client:[client-name-lowercase]
> Last updated: [today]

## Summary
client:[client-name-lowercase] SUMMARY (updated [today]): [Client Name] engagement — [offering]. [1-sentence scope from SOW]. Primary contact: [name, title]. Kickoff: [date]. Status: Initializing.

## Knowledge
### Models
### Gotchas
### Lessons
### Recipes
### Insights
### Corrections

## People
client:[client-name-lowercase] PEOPLE: [Primary contact name] ([title]) — Primary client contact. [email if known].

## Changelog
client:[client-name-lowercase] LOG [today] — Project initialized: Offering: [offering]. Contract value: [if shared]. Key deliverables: [2-3 items]. Phase 1 focus: [phase 1 goal]. Immediate next step: [the step from Output 3].

## Open Threads
- [FRESH] Complete Phase 1 kickoff activities

## Next Actions
- [P0] [Immediate next step from Output 3]

## Signals
```

Also update `<config-root>/memory/DASHBOARD.md` — add the new node to the Active Nodes section.

After committing, confirm: "Memory node `client:[name]` created — future sessions will have context on this engagement from the start."

If cortex is NOT installed, skip Output 4 and note in the final response that memory init was skipped.

### Output 5: Primary contact person page (cortex v4.2+)

**Only if cortex is installed.** This is graduation trigger #3 in cortex's CLAUDE.md schema — when project-setup names a primary contact, that person should have a canonical page.

1. Resolve `<config-root>` via the standard pointer.
2. Compute slug from the primary contact's name: `firstname-lastname` lowercased, hyphenated.
3. Check for name collision: if `<config-root>/memory/person/<slug>.md` already exists about someone else (different company / email), prompt the user once to disambiguate. Recommend appending the client slug: `<slug>-<client-name-lowercased>.md`.
4. **If the page does NOT exist** → create it using cortex's person-page schema:

```markdown
# person:[firstname-lastname]
> Last updated: [today]

## Identity
- **Full name:** [Primary contact full name]
- **Title / role:** [Title]
- **Company:** [client/[client-name-lowercase]]
- **Email:** [email if known]
- **LinkedIn / other:** [if known]
- **First mentioned:** [today] (project-setup for [client-name])

## Relationship
- **How we know each other:** Primary contact on the [offering] engagement. Kickoff [date].
- **Relationship temperature:** Active
- **Last meaningful contact:** [today] (kickoff prep)
- **Relationship owner:** [you]

## Recent interactions (last 90 days, append-only)
- [today] — project-setup — primary contact for new engagement [client-name]

## Open threads
- [P0] Complete Phase 1 kickoff activities (linked to [client/[client-name-lowercase]])

## Notes
[Any context from the interview that's specific to this person, not the client/company]

## Linked entities
- Projects: [client/[client-name-lowercase]]
```

5. **If the page DOES exist** (returning client, or same person appeared in a prior engagement) → append a Recent interaction line: `[today] — project-setup — primary contact for new engagement [client-name]`. Append `[client/[client-name-lowercase]]` to Linked entities if not already present. Refresh Relationship temperature to Active.

6. Add or refresh the "Active people" row in `<config-root>/memory/DASHBOARD.md`.

If cortex is NOT installed, skip this output silently (consistent with Output 4).

---

## Tone & behavior notes

- Pull from context already shared — don't re-ask what you already know.
- If something critical is missing, flag it as a gap rather than blocking progress.
- Use the client's real name, real deliverable names from the SOW, real contacts throughout.
- The system prompt and project plan should feel purpose-built for this client, not templated.
- If multiple offerings selected, blend offering-specific questions and produce a combined project plan.

---

## What this command is *not* for

- Updating an existing engagement. This is initialization-only. For ongoing updates, use `/recall [client]` (cortex) or edit the Claude Project directly.
- Generating SOWs or contracts directly — that's `/sow`, which this command can chain into (Group 2) when a proposal exists but no SOW yet. Bring signed SOWs in as-is otherwise.
- Replacing PM tools. The project plan is a starting point, not a Gantt chart.
