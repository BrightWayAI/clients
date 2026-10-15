---
description: Initialize a new client engagement end-to-end, starting from the executed contract. Verifies the SOW is signed, extracts terms into project-safe and finance-only fields, asks only about what the contract doesn't answer, then executes one confirmed plan — Drive filing, folder structure, cortex memory node (the public project record), and companion-plugin/connector handoffs — respecting access-zone boundaries throughout.
---

# /project-setup

End-to-end client engagement initialization, driven by the executed contract. A
contract comes back signed → run this command → one confirmation → Drive is filed
and organized, the cortex client node (the phased plan, immediate next step, and
engagement context) is written, and companion plugins/connected apps are updated.

This command does not create or maintain a Claude Project. Cortex's client node is
the canonical, portable project record — it works the same whether the session is
Claude Code, Claude.ai, ChatGPT, or Codex.

Supports `--dry-run` (produce the plan in Step 5, show it, stop — nothing executes).

---

## Step 0 — Preflight

Read `<config-root>/plugins/clients.user-context.md`.

- **Missing entirely** → route to `/setup-projects` and stop.
- **Missing `## Access zones` or `## Naming conventions`** → this is a pre-0.8.0
  config. Explain: "This is a breaking change in v0.8.0 — `/project-setup` now
  requires Access zones and Naming conventions configured, so financial data can
  never land in a contractor-visible folder. Run `/setup-projects` to add them (your
  existing offerings/identity/communication settings are untouched)." Stop.
- **Present and complete** → continue.

Extract from user-context: Identity, Offerings catalog, Drive layout, **Access
zones**, **Naming conventions**, Companion plugins (cortex / ops / growth), and
Communication defaults.

**Connector check.** Determine which of file storage, email, calendar, and CRM are
available. Report any that aren't checked as unavailable; skip their steps later
rather than failing. This plugin never connects to accounting software — the
finance-alert email in 6.5 is how accounting setup gets requested.

**Zone-access check.** Determine the current user's access to each configured zone
(skip zones marked "not used"). If the current user lacks finance-zone access:
still carry out every project-zone step in full, and instead of the finance-zone
actions in Step 6.1–6.2, produce a **finance handoff list** — the exact filing and
permission-audit actions someone with finance access needs to do — for the finance
owner named in Access zones' expected-access description. Never fail the whole run
because one zone is inaccessible to this user.

Read user-owned template overrides when present, otherwise the bundled defaults:
- `<config-root>/plugins/clients/templates/drive-structure.md` → fallback `references/templates/drive-structure.md`
- `<config-root>/plugins/clients/templates/project-plans.md` → fallback `references/templates/project-plans.md`

Installed plugin files are read-only. User-owned overrides are the structural source
of truth when present; otherwise use bundled defaults.

---

## Step 1 — Find and verify the contract

Accept, in order of preference: an attached file, a Drive link, or a search of Drive
and email for the client name plus "SOW", "agreement", or "signed".

**Tell executed copies apart from drafts.** Signals that a copy is executed:
- a completed e-signature PDF, such as a Google Workspace eSignature copy named
  `<doc> - M/D/YY, h:mm AM`
- a DocuSign or Dropbox Sign completion email and certificate
- a signature block with names and dates actually filled in
- the absence of markers like "DRAFT" or "NOT EXECUTED"

A title containing "DRAFT FOR REVIEW" or "NOT EXECUTED" is a draft regardless of any
other signal, even if a signature-shaped block exists elsewhere in the doc.

**No executed copy found** → switch to **prep mode**: pull the terms from the best
available draft (Step 3), build the full plan and every downstream artifact, but
write nothing to Drive or any connector. Report "Ready to run on signature — nothing
was written." Continue through Steps 2–5 in prep mode so the plan is ready the moment
the contract executes; do not run Step 6.

---

## Step 2 — Classify the run

Check memory (cortex `client:` nodes if installed), the file-storage zones, and the
CRM for existing records of this client.

Classify as one of:
- **new client** — no prior record anywhere
- **new engagement or phase for an existing client**
- **amendment** to an existing SOW

**A returning client never gets a second client folder.** The project-zone
structure is one evergreen folder per client with dated engagement subfolders
underneath (`[Client]/[YYYY-MM] [Engagement Name]/`), so a new engagement or phase
is just a new sibling subfolder — never a reason to create a second client folder.
If several client-level folders already exist for the same client in the same zone
(e.g., "Barker and Scott" and "Barker & Scott"), list them and ask which is
canonical. Once confirmed: propose renaming the canonical one to match the naming
convention, and propose moving any content — including any existing engagement
subfolders — from the non-canonical folder(s) into it. **Never delete** — if a move
isn't supported by the connector, copy and list originals for manual removal.

---

## Step 3 — Extract the terms

Build a structured record, sorted into zones:

**Project-safe fields** (may appear in the project zone):
- client name and address
- effective date
- phases with durations and deliverables
- total duration as a range, and the resulting calendar end-date range
- client roles and responsibilities
- meeting cadence and tracker commitments
- out-of-scope items
- the defect or warranty window

**Finance-only fields** (finance zone / finance config only):
- billing model (fixed / T&M / retainer)
- rates
- per-phase cost estimates
- cap or not-to-exceed amount
- invoicing cadence and itemization requirements (e.g. "itemized by phase")
- payment terms and suspension terms
- expense policy
- maintenance estimates

**Flag contradictions** against memory or the CRM — e.g., memory says "negotiating
at $80K" but the contract has a cap of $107,000. Report the mismatch; don't silently
prefer one source.

---

## Step 4 — Gap interview

Ask only for what the contract doesn't answer. Typically:
- the named client product owner and executive sponsor, if the contract gives only roles
- the kickoff date
- which CRM deal to update, and which amount to record
- subcontractors involved
- risks and landmines

Keep the offering-specific questions from `references/templates/project-plans.md`
for each selected offering, but skip any the contract already answers. Run
conversationally — group questions, don't dump them all at once.

---

## Step 5 — One plan, one confirmation

Present every action as a table: **system | action | target zone | reversible?**
Cover every action in Step 6 that applies to this run (prep-mode runs show the same
table but note nothing executes). The user can approve everything or strike
individual rows.

`--dry-run` stops here — produce this table and the artifacts it describes, then
stop. Nothing in Step 6 runs.

---

## Step 6 — Execute (approved rows only, in this order)

### 6.1 — Finance zone

- File the executed contract under `[Client]/[YYYY-MM] [Engagement Name]/` using
  the configured executed-contract file pattern.
- Move every draft, redline, and superseded copy found in **any** zone — including
  ones sitting in the project zone — into `[YYYY-MM] [Engagement Name]/_Archive/`.
- Moving into the finance drive applies the finance drive's permissions
  automatically. If the connector can't move a file between shared drives, copy it
  and list the originals for manual removal. **Never delete.**
- If the current user lacks finance-zone access (Step 0), skip this and add the
  equivalent actions to the finance handoff list instead.

### 6.2 — Permission audit (report-only)

- After filing, read the permissions on every file in the finance zone the skill
  touched.
- Flag: any access granted directly on a file that differs from what the drive
  grants by default; any "anyone with the link" sharing found on a finance-zone
  file; anyone with project-zone access who isn't on the expected-access
  description in config.
- **Report only.** Never change a permission — that requires the user to act
  separately, with their own confirmation, outside this command.

### 6.3 — Project zone

- Create the client-level folder if it doesn't already exist, then create the
  dated engagement subfolder `[YYYY-MM] [Engagement Name]/` with the four standard
  subfolders from `drive-structure.md`: `00_Scope`, `03_Deliverables`,
  `04_Client Assets`, `05_Meeting Notes`. No other subfolders — this skeleton is
  the same for every offering and every client.
- Name `03_Deliverables` subfolders after the SOW's **actual** phases (e.g.,
  "Phase 0 — Knowledge Capture & Setup", "Phase 1A — Marketplace Inventory"), not a
  generic template phase name.
- Write the **Scope Brief** into `00_Scope` per `drive-structure.md`'s spec
  (project-safe fields only; one no-link line naming where the contract is held; no
  shortcut to the contract).
- **Before writing**, run the pricing-leak check (below) on the Scope Brief. A
  finding stops the write and is shown to the user instead — never written with
  the flagged content redacted silently, and never skipped.

There is no Claude Project prompt and no phased-plan document written to Drive.
The phased plan, immediate next step, and ongoing engagement context live in the
cortex client node (6.4) — that's the portable, canonical project record.

**Pricing-leak check.** Before any write to the project zone, and for any content
bound for a shared surface (the Scope Brief, the cortex client node, calendar event
descriptions, `/client-status` drafts): run a regex pass for currency amounts,
per-hour/per-day rate patterns, "not to exceed", and `net \d+`, plus a semantic pass
for restated dollar figures, rate language, or cap language that the regex might
miss (e.g., "one hundred seven thousand dollars", "capped at approximately $107K").
If anything is found, **stop and show exactly what was found and where** instead
of writing it. Client-facing `/client-status` budget lines are the one documented
exception — see `commands/client-status.md`.

### 6.4 — Companion plugins

Skip any that aren't installed; report the skip in Step 7.

- **`admin` `/setup-time`** — pass the billing model, rate, cap, and **phase tags**
  so `/track-time` records the phase from day one. This matters whenever the SOW
  requires invoices itemized by phase. Phase *names* are project-safe and may be
  passed freely; rates and caps stay in finance config, passed only to `admin`'s
  own finance-scoped storage, never echoed back into a project-zone artifact.
  If `admin` has a billing register configured (`admin.user-context.md`'s
  `## Billing register`), also run `admin`'s
  `references/setup-notice-generation.md` Steps 1–3 (draft register records,
  confirm with the user, write to the register backend) — this is what gets the
  new customer/project into the register the accountant packet later reads from.
  Steps 4–5 of that procedure (setup sheet + accountant email) run as part of the
  finance-alert step below, not here.
- **`clients` `/client-status`** — register the client and cadence. If the SOW
  requires spend/forecast reporting against a cap, include that in the
  client-facing budget line per `commands/client-status.md`'s storage rule.
- **`cortex`** — write the client node and the primary contact's person page using
  cortex's **current** (v4.16+) schema, not the inline Summary/Knowledge/Changelog
  template from earlier versions of this command. This node — not a Claude
  Project — is the client's public, portable project record. Concretely:
  - Read `<config-root>/memory/client/[client-slug].md` if it exists, else create
    it at that path.
  - New node: frontmatter (`type: client`, `status`, `created`, `last_active`,
    `decay_profile`) + `# client:[client-slug]` + `## Current state` + `## Open
    loops` + `## Linked entities`, matching the shape in cortex's
    `references/workstream-schema.md`. Populate `## Current state` with the
    engagement summary — offering, primary contact, kickoff date, current phase and
    goal, and the phased plan (project-safe fields only). Populate `## Open loops`
    with the Phase 1 kickoff P0 and the single Immediate Next Step (see Outputs
    below).
  - Returning client → append the new engagement to `## Current state` / `## Open
    loops` rather than replacing them; don't create a second node.
  - Do **not** write a `DASHBOARD.md` — that file belongs to a pre-restructure
    cortex layout. Run cortex's own `/reindex` (or note that it should be run) so
    `index.md` picks up the new/updated node instead.
  - Person page: `<config-root>/memory/person/[slug].md`, same current-schema
    shape. If it already exists for a different person (name collision), ask once
    to disambiguate and recommend `<slug>-<client>.md`.
  - Finance-only fields (rate, cap, billing model) never go into a shared cortex
    node — cortex's private/finance-scoped storage only, if cortex offers one;
    otherwise finance config stays in this plugin's finance zone/config, not memory.
  - If cortex's schema references (`references/workstream-schema.md`,
    `references/node-taxonomy.md`) aren't readable at run time, fall back to
    asking the user whether to proceed with a best-effort current-shape node or
    skip cortex writes for this run — never guess and write the outdated
    Summary/Knowledge/Changelog/DASHBOARD shape.

### 6.5 — Connected apps

Each optional; skip and report if its connector isn't available.

- **CRM (HubSpot):** move the deal to closed-won with the amount the user chose in
  Step 4, link the contact, set start and end dates.
- **Calendar:** suggest kickoff times and create holds. Create the recurring
  meeting the SOW calls for. Event descriptions carry no pricing — pricing-leak
  check applies here too.
- **Email — kickoff:** draft the kickoff email to the primary contact, built from
  the SOW's client-inputs section. **Draft only — never send.**
- **Email — finance alert:** if `admin` has a billing register configured, run
  `admin`'s `references/setup-notice-generation.md` Steps 4–5 against the records
  confirmed in 6.4 — this produces the setup sheet (customer, project, terms,
  contract value, billing schedule, full line-item catalog, cost assignments,
  start date, first expected invoice) and drafts the accountant-handoff email to
  the recipients configured in `admin.user-context.md`'s
  `## Billing packet / accountant handoff`, using that plugin's own recipient
  list rather than Client Success's `## Notification recipients`. If `admin`
  isn't installed or has no register configured, fall back to the plain finance
  alert: an email to the recipients configured in `## Notification recipients`
  (finance list) with the contract's finance-only terms (billing model, rate,
  cap, invoicing cadence/itemization, payment terms) and the executed contract
  attached or linked from its finance-zone location. Either way, this is the
  request for finance/the accountant to set the engagement up in accounting — the
  plugin never touches accounting software directly. **Draft only — never send.**
- **Email — delivery-team alert:** draft an email to the recipients configured in
  `## Notification recipients` (delivery-team list) announcing the new engagement,
  with the project-safe scope summary (offering, phases, deliverables, timeline,
  primary contact) and the single Immediate Next Step from Outputs. Run the
  pricing-leak check on both drafts before presenting them — the finance draft is
  the one place a figure is expected, but it must never reach the delivery-team
  draft. **Draft only — never send.**

If `## Notification recipients` isn't configured yet, ask for the finance and
delivery-team recipient lists once during this run, offer to save them to
user-context so future runs don't ask again, and still produce both drafts this
time.

---

## Step 7 — Report

- A checklist of everything created, moved, or renamed, with links.
- Anything skipped, and why (missing connector, missing cortex, prep mode).
- The finance handoff list, if any (Step 0/6.1).
- The permission-audit findings (Step 6.2) — report only, no changes made.
- The next step.

---

## Outputs (produced across Steps 3–6, in prep mode too — minus the writes)

1. **Drive folder structure** — created directly in the project zone (not described
   for manual creation): the client folder, the dated engagement subfolder, and the
   four standard subfolders.
2. **Scope Brief** — written into `00_Scope`.
3. **Phased project plan + single immediate next step** — written into the cortex
   client node's `## Current state` / `## Open loops` (6.4), the client's public
   project record. Surface one Immediate Next Step in the response either way: the
   one thing to do in the next 24 hours, specific about person/action/channel
   (e.g., "Send the kickoff prep email to [Name] — want me to draft it now?").
   Offer to execute it if it's something Claude can help with. **If cortex isn't
   installed**, present the phased plan and next step in the response only — it
   isn't written anywhere — and note in Step 7 that memory init was skipped.
4. **Memory node + person page** — only if cortex is installed (6.4).

---

## Tone & behavior notes

- Pull from context already shared — don't re-ask what the contract or the
  conversation already answered.
- If something critical is missing, flag it as a gap rather than blocking progress.
- Use the client's real name, real deliverable names from the SOW, real contacts
  throughout.
- The project plan should feel purpose-built for this client, not templated.
- If multiple offerings are selected, blend offering-specific questions and produce
  a combined project plan.

---

## What this command is *not* for

- Updating an existing engagement after initialization. For ongoing updates, use
  `/recall [client]` (cortex).
- Generating SOWs or contracts — that's `/sow`. Bring signed SOWs in as-is; in prep
  mode this command works from the best available draft and writes nothing.
- Replacing PM tools. The project plan is a starting point, not a Gantt chart.
- Changing any permission it flags in Step 6.2 — that's always a separate, manual,
  user-confirmed action.
