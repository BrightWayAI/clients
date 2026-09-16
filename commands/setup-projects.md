---
description: Configure Client Success for offerings, drive layout, companion-plugin integrations, and a derived SOW format template. Writes to `<config-root>/plugins/clients.user-context.md` and `<config-root>/plugins/clients.sow-template.md` using the shared vendor-neutral config-root resolver. Re-run anytime to add or update offerings; `--add-sample` merges a second SOW sample.
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

### Section 6 — Sample Statement of Work (powers `/sow`)

Ask for one SOW the user has already sent a client:
- **.docx** (preferred — styling is machine-readable)
- **Google Drive link** — export as .docx via the Drive connector, then process as above
- **PDF** — content only; formatting falls back to `references/sow-format-default.md`. Tell the user this explicitly: "PDFs don't carry machine-readable styling, so I'll use generic default formatting until you can supply a .docx sample."

If the user has no sample yet, skip this section — `/sow` will prompt for one on first use.

**Extraction (docx only):** run `python3 scripts/sow_extract.py <path-to-sample.docx>`. This reads rPr/pPr/tblPr/tcPr and the footer part with python-docx — never eyeball rendered text for spacing, colors, or sizes. It returns:

(a) **FORMAT SPEC** — page size/margins; fonts+sizes per role (title, doc title, byline, draft banner, section heading, body, table header, table body, signature captions, footer); colors; paragraph spacing; heading numbering style ("N.  Title"); bullet indent; table border/fill rules; signature-block layout; footer text pattern and page-number position.

(b) **SECTION SKELETON** — ordered list of section headings found. For each, ask the user (or infer from content) a one-line note on what it covers, and classify as:
- **boilerplate** (reusable verbatim, only party names/defined terms change): relationship of the parties, reps & warranties, indemnification, non-solicit, termination, general provisions
- **engagement-specific** (rewritten per SOW): term, services, inputs, cadence, acceptance, change requests, compensation, out of scope

Also capture from the sample: legal-entity name as it appears, default governing law, default payment terms (net days, late interest, suspension notice), default cure/convenience notice periods, and whether a "DRAFT FOR REVIEW — NOT EXECUTED" banner is used.

**Confirm before saving** — show a short table (element → derived value) built from `sow_extract.py`'s markdown output, e.g.:

| Element | Value |
|---|---|
| Fonts | Crimson Pro (headings) / Inter (body) |
| Title rule | Gold #D59F1E |
| Table header | Navy #0B131C fill, white text |
| Sections | 18, ordered |
| Signature block | Two-column, borderless |

Only write after the user confirms it looks right or corrects it.

**Write to `<config-root>/plugins/clients.sow-template.md`:**

```markdown
# clients SOW template
_Derived from: [sample filename], captured [date]_

## Format spec
```json
[FORMAT SPEC JSON from sow_extract.py, corrected per user feedback]
```

## Section skeleton
1. [Heading] — [one-line note] — [boilerplate | engagement-specific]
2. ...

## Defaults from sample
- Legal entity name (as shown): ...
- Governing law: ...
- Payment terms: net [N] days, late interest [rate], suspension notice [days]
- Cure / convenience notice periods: ...
- Draft banner used: yes/no
```

**Re-runnable:**
- Running this section again with a new sample **replaces** the template (confirm before overwriting — show a diff-style summary of what changed).
- `/setup-projects --add-sample` merges a second sample into the existing template: run `sow_extract.py` on it, and for any FORMAT SPEC or skeleton field that conflicts with the existing template, ask the user which to prefer. Non-conflicting fields (e.g., a section present in the new sample but not the old one) are added.

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

If a sample SOW was captured in Section 6:
> "Try `/sow` next time you have a proposal ready to turn into a Statement of Work — it'll match the format of the sample you just gave me."

If no sample was captured:
> "`/sow` is ready to use, but with generic default formatting until you give me a sample SOW — run `/setup-projects --add-sample` anytime to fix that."

---

## Behavior rules

- One section at a time.
- For Section 3 (offerings catalog), be patient — this is the most important section. The plugin is generic only if the offerings are well-captured.
- Idempotent — re-running adds new offerings or updates existing ones.
- Never edit bundled files in the installed plugin directory. All customizations live under `<config-root>/plugins/clients/`.
