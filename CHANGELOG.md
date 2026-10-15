# Changelog

All notable changes to delivery are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/). Versions match `plugin.json`.

## [0.8.2] — Plugin-directory pre-submission fix (2026-10-15)

### Fixed
- The SOW scripts (`scripts/sow_build.py`, `scripts/sow_extract.py`) and `scripts/requirements-sow.txt` declared `python-docx>=1.1,<2` — an unpinned range. The Claude plugin directory's pre-submission checklist requires every package a `uv run` launcher resolves to be pinned to an exact version. Pinned to `python-docx==1.1.2` in all three places, plus the `uv run --with python-docx ...` test command in `README.md`.

## [0.8.1] — Billing-register handoff at project setup (2026-10-15)

### Changed
- `/project-setup` Step 6.4 now also runs `admin`'s `references/setup-notice-generation.md` Steps 1–3 (draft/confirm/write billing-register records: Customer, Project, Line Items, Cost Assignments) when `admin` is installed with a billing register configured — skipped and reported if either condition isn't met.
- `/project-setup` Step 6.5's finance-alert draft now generates the full accountant setup sheet (`setup-notice-generation.md` Steps 4–5) and sends it to `admin.user-context.md`'s configured accountant recipients when a billing register is in use, instead of the plain finance-terms email to Client Success's own notification list. Falls back to the prior plain finance alert when `admin`/the register isn't configured — no behavior change for users who don't use it. Still draft-only, never auto-sent.

## [0.8.0] — Executed-contract intake, access zones, real setup actions (2026-09-24)

### Breaking
- **`## Access zones` and `## Naming conventions` are now required** in
  `clients.user-context.md`. `/project-setup` refuses to run without them.
  **Upgrade:** re-run `/setup-projects` — it detects a pre-0.8.0 config and runs
  only the two new sections, leaving your existing offerings/identity/communication
  settings untouched.

### Added
- **No accounting connector.** `/project-setup` no longer touches QuickBooks (or
  any accounting software) directly. Instead it drafts a **finance-alert email**
  (recipients from the new `## Notification recipients` config, never hardcoded)
  with the new client/engagement's finance-only terms and the executed contract,
  so finance sets it up in accounting themselves — and a **delivery-team-alert
  email** with the project-safe scope summary and the immediate next step. Both
  draft-only, both pricing-leak-checked (the finance draft is the one place a
  figure belongs; it must never leak into the delivery-team draft).
- Renamed the drafts-and-redlines archive folder from `_Superseded` to `_Archive`
  — same behavior, clearer name.
- `/project-setup` now starts from the executed contract instead of interviewing
  for facts the signed SOW already answers. It finds and verifies the contract
  (executed vs. draft signal detection), classifies the run (new client / new
  engagement or phase / amendment), extracts terms into project-safe vs.
  finance-only fields, flags contradictions against memory/CRM, and asks the gap
  interview only for what the contract doesn't answer. No executed copy found →
  **prep mode**: build the full plan, write nothing, report "ready to run on
  signature."
- **Access zones** (`finance` / `pipeline` / `project`) — every output is assigned
  to a zone; financial data (amounts, rates, caps, phase estimates, payment terms,
  invoice/deal amounts, margin, vendor costs) can never land in the open `project`
  zone. A **pricing-leak check** (regex + semantic pass) runs before every write to
  the project zone or any shared surface (Claude Project prompt, phased plan,
  calendar descriptions, the Scope Brief, `/client-status` drafts) and stops the
  write on a finding instead of redacting or proceeding silently.
- `/project-setup` now does the setup instead of describing it: creates the folder
  tree, files and renames documents, moves drafts/superseded copies into
  `_Archive` in the finance zone, and hands off to `admin`, `client-status`,
  `cortex`, and connected apps (HubSpot, Calendar, email-draft) — all
  behind a single confirmable plan (`system | action | target zone | reversible?`).
  Supports `--dry-run`.
- **Evergreen client/engagement folder structure.** One folder per client, with
  dated `[YYYY-MM] [Engagement Name]` subfolders underneath for each engagement —
  a returning client or a new phase is a new sibling subfolder, never a second
  client folder. The per-engagement skeleton is now a flat, offering-agnostic
  four: `00_Scope`, `03_Deliverables`, `04_Client Assets`, `05_Meeting Notes`.
  Dropped `01_Kickoff` (folds into Meeting Notes) and offering-specific Folder 02
  variants.
- **Claude Project generation removed.** The cortex client node is now the
  client's public, portable project record — the phased plan and immediate next
  step live there instead of in a generated Claude Project system prompt.
  `references/templates/claude-project-prompt.md` is deleted; nothing replaces its
  `Contract Value` field anywhere, since the whole output no longer exists.
- **Permission audit** (report-only) after finance-zone filing: flags direct
  grants that differ from the drive's defaults, "anyone with the link" sharing on
  finance files, and unexpected project-zone access. Never changes a permission —
  always a separate, manually-confirmed action.
- **Naming conventions** captured once in config (client folder name, engagement
  folder pattern, executed-contract and superseded-draft file patterns, Scope Brief
  file name, date format) and applied to every folder/file the skill creates or
  files. `/setup-projects` can infer these from the existing Drive and confirm
  before saving.
- **Safe to re-run** — recognizes a returning client and reuses its canonical
  folder per zone instead of creating a duplicate; if duplicates already exist,
  lists them and asks which is canonical, then proposes (never forces) a rename
  and consolidation. Never deletes.
- Cortex handoff now targets cortex's **current** (v4.16+) node schema
  (frontmatter + `## Current state` + `## Open loops`, matching
  `references/workstream-schema.md`) instead of the outdated inline
  Summary/Knowledge/Changelog/`DASHBOARD.md` template.
- `skills/project-setup/SKILL.md` — fixed the contradictory
  `disable-model-invocation: true` + auto-trigger-phrase description; it now
  auto-fires only on explicit signed/starting signals, with the one-confirmation
  execution gate as the safety net. New eval case
  `evals/project-setup-natural-language/`.

### Changed
- `references/templates/drive-structure.md` — `00_Contract & SOW` replaced with
  `00_Scope`. The skill generates a Scope Brief Google Doc into it from
  project-safe fields only; excludes compensation/IP/liability/indemnification/
  termination-payment; carries one no-link, no-amount line naming where the
  contract is held. No shortcut to the contract is ever created in the project
  zone — a Drive shortcut reveals the target's file name even to people who can't
  open it.
- `commands/client-status.md` — client-facing budget/spend-against-cap lines may
  still appear (the client already knows the terms); any other draft containing
  figures is stored in the finance zone or kept out of Drive, never the project
  zone.

## [0.7.1] — OpenAI SOW production hardening (2026-09-16)

### Fixed
- Regenerated OpenAI metadata from the canonical Nucleus adapter source and kept the default-prompt surface within the three-prompt host limit.
- Declared `python-docx` with PEP 723 plus a requirements fallback, added a dependency preflight, and documented host-native document rendering/file delivery for ChatGPT and Codex.
- Added a structured JSON-to-DOCX build path, full footer placeholder substitution, packaged-default path resolution, paragraph spacing/alignment, table rules, repeated headers, and signature-layout handling.
- SOW template extraction now resolves inherited Word styles and captures section bodies so approved boilerplate can be retained verbatim instead of regenerated.
- `/sow` no longer assumes every prior agreement means the new document is an addendum, never invents missing legal boilerplate, and requires rendered-page QA before delivery.
- `/sow` is model-invocable from a specific natural-language request, with a matching eval case, so the OpenAI default prompt works when Clients is installed without Chief of Staff.

## [0.7.0] — Statement of Work generation (2026-09-16)

### Added
- **`/sow`** — turns a proposal into a finished Statement of Work in your house format. No format is hardcoded in the plugin; everything visual is derived from a sample SOW you provide.
- **`/setup-projects` Section 6** — captures a sample SOW (.docx preferred, Drive link, or PDF-content-only fallback), extracts a FORMAT SPEC (fonts/sizes/colors/spacing/table+signature layout, read from docx XML via python-docx — never eyeballed) and a SECTION SKELETON (ordered headings, boilerplate vs. engagement-specific), and writes both to `<config-root>/plugins/clients.sow-template.md`. Re-runnable; `--add-sample` merges a second sample and asks which to prefer on conflicts.
- `scripts/sow_extract.py` — docx → FORMAT SPEC/SECTION SKELETON JSON + markdown confirmation table.
- `scripts/sow_build.py` — python-docx builder (`title_block`, `heading`, `para`, `bullets`, `table`, `signature`, `exhibit`, `save`) that renders from the derived spec, with explicit fixed-width table columns, a footer PAGE field, and explicit run formatting so Google Docs import preserves fonts.
- `references/sow-format-default.md` — generic fallback styling used only when no sample has been captured.
- `/review-deliverable` now checks SOWs against `clients.sow-template.md` (sections present/ordered, format spec honored, defined terms consistent, every proposal cost line accounted for).
- `/project-setup` offers to chain into `/sow` when a proposal exists but no SOW has been drafted yet.
- `/status` and `/diagnose` (ops) report whether a SOW template is configured.

## [0.6.1] — OpenAI host adapter (2026-09-14)

### Added
- Native Codex/ChatGPT plugin manifest, durable `AGENTS.md` entrypoint, and an explicit OpenAI capability/degradation contract.
- GPT-discoverable skill aliases for canonical command workflows and read-only Codex role bindings where this plugin ships agents.
- Shared config-root resolution compatible with Cortex and Claude; all GPT tests use repository fixtures or temporary directories only.

## [0.6.0] — `/setup-voice` ownership moves to Comms Desk (2026-09-15)

### Changed
- `commands/setup-status.md` updated to attribute `/setup-voice` to `comms` instead of `cortex`.
- `commands/client-status.md` Step 3 now degrades gracefully with an explicit "No voice file found — using generic tone; run comms's `/setup-voice` to fix this" message when `<config-root>/memory/me/voice.md` doesn't exist, instead of silently assuming it's present.

## [0.5.0] — pipeline-analyst ownership moved to growth (2026-09-15)

### Changed
- `pipeline-analyst` now lives in the `growth` plugin (moved from `ops`). README and `/setup-projects` updated to reference `growth` and report "Growth Engine not installed; pipeline analysis skipped" when growth isn't present.

## [0.4.0] — renamed to clients (2026-09-15)

### Changed
- Renamed from `delivery` to `clients` (display name: Client Success) as part of the 2026-09-15 Nucleus plugin rename. Old plugin ID/repo name redirects; see marketplace catalog. This is the second rename in this plugin's history — it was previously renamed in-place from `project-setup` to `delivery`, also on 2026-09-15.

## [0.3.4] — canonical Delivery state ownership (2026-09-15)

### Changed
- Canonicalized engagement and status configuration as `delivery.user-context.md` and `delivery-status.user-context.md`, with non-destructive one-time legacy imports.
- Moved user template overrides under the config root and removed runtime edits to installed plugin files.
- Updated client-status workflows to read Delivery and the canonical private voice path.

## [0.3.3] — Codex adapter synchronization (2026-09-15)

### Fixed
- Updated the Codex manifest and portability contract for the consolidated engagement setup, client-status, and deliverable-QA surface.

## [0.3.2] — claude plugin eval suite (2026-09-15)

Nucleus Operating Model Refactor Phase 4 step 4.2.

### Added
- `evals/client-status-natural-language/` — eval case testing the client-status skill's natural-language trigger, with an `llm` grader
  checking the response acts on the natural-language request directly rather
  than asking the user to type the explicit command. Run with
  `claude plugin eval . --case client-status-natural-language`; `--ablation with-without`
  (the default when the plugin resolves) reports the delta between installed
  and not — a delta near zero means the skill's description isn't matching
  natural phrasing and needs work.
- `.gitignore` — excludes `evals/results/` (per-run output, not checked in).

## [0.3.1] — Skill auto-invocation audit (2026-09-15)

Nucleus Operating Model Refactor Phase 3 step 3.7. Ritual and side-effecting
skills marked `disable-model-invocation: true` so they only run on explicit
invocation, not loose natural-language matching — the model can still be
asked to run them by name. Read-mostly, low-stakes, or high-frequency
conversational skills are left auto-invocable. Marketplace-wide this brings
model-invocable skills from ~81 to 27, under the ≤30 target audited with
`/skill-doctor`.

### Changed
- Marked `disable-model-invocation: true` on: `project-setup`, `setup-projects`, `setup-status`.

## [0.3.0] — Renamed to delivery, absorbs client-status + review-deliverable (2026-09-15)

Nucleus Operating Model Refactor Phase 3 step 3.3. `project-setup` renamed to
`delivery` and now covers the whole client engagement lifecycle: start, status,
QA.

### Added
- `/client-status` and `/setup-status` (moved from the retired `client-status`
  plugin, unchanged) — weekly client-facing status draft generation.
- `/review-deliverable` (moved from `core-ops`, unchanged) — structured QA pass
  on a client deliverable against the user's brand guide. Reads brand/CRM
  config cross-plugin from `core-ops.user-context.md`, same pattern
  `relationships` already uses for CRM config.

### Changed
- Plugin renamed `project-setup` → `delivery`; repository renamed
  `BrightWayAI/project-setup` → `BrightWayAI/delivery` (GitHub redirects the
  old URL).
- `references/client-status-user-context.template.md` — renamed from
  `client-status`'s `user-context.template.md` to avoid a filename collision
  with this plugin's own template.
- Fixed stale legacy paths in `commands/project-setup.md` and
  `commands/client-status.md` — `~/Documents/Claude/identity.md` /
  `voice.md` / `memory/client/` / `memory/DASHBOARD.md` now correctly read
  `<config-root>/memory/me/identity.md`, `<config-root>/memory/me/voice.md`,
  `<config-root>/memory/client/`, `<config-root>/memory/DASHBOARD.md`. These
  were pre-existing bugs in the source plugins, predating the `<config-root>`
  convention; fixed opportunistically while porting.

### Removed
- Duplicate generic `skills/setup/SKILL.md` — this plugin already had
  `skills/setup-projects/SKILL.md` covering the same ground; the redundant
  `client-status` equivalent was not copied over.

## [0.2.6] — Identity/voice moved to memory/me/ (2026-09-15)

### Changed
- Path references updated from `<config-root>/identity.md` / `<config-root>/voice.md` to `<config-root>/memory/me/identity.md` / `<config-root>/memory/me/voice.md`, per the Nucleus Operating Model Refactor Phase 2 scopes restructure (identity/voice are personal, not org-shared facts). No behavior change beyond the path.

## [0.2.5] — OpenAI host adapter (2026-09-14)

### Added
- Native Codex/ChatGPT plugin manifest, durable `AGENTS.md` entrypoint, and an explicit OpenAI capability/degradation contract.
- GPT-discoverable skill aliases for canonical command workflows and read-only Codex role bindings where this plugin ships agents.
- Shared config-root resolution compatible with Cortex and Claude; all GPT tests use repository fixtures or temporary directories only.

## [0.2.4] — Primary contact person page (2026-05-12)

### Added
- **Output 5 — Primary contact person page (cortex graduation trigger #3).** When project-setup names a primary contact for a new engagement, the plugin now creates `<config-root>/memory/person/<slug>.md` using cortex's person-page schema. Identity, Relationship (temperature: Active, owner: you), Recent interactions (seeded with the kickoff entry), Open threads (Phase 1 kickoff P0), and Linked entities (the new client node) are pre-filled from the interview.
- **Returning client handling.** If the primary contact already has a graduated page (e.g., a returning client), the output is additive: append a Recent-interactions line for the new engagement, link the new `client/<name>` node to Linked entities, refresh Relationship temperature to Active.
- **Name-collision disambiguation.** If two people would slug to the same name (different company / email), prompts the user and recommends appending a client-name hint (`<slug>-<client>.md`).
- **Graceful degradation.** Skipped silently if cortex isn't installed (matches Output 4's behavior).

### Why this matters
Phase 3 of SECOND-BRAIN-V2-SPEC. New-engagement primary contacts are unambiguously page-worthy — they're who the user works with on the entire project. Creating the page at engagement initialization means cortex has context on the relationship from day one rather than waiting for organic graduation triggers to fire.

## [0.2.3] — Platform-agnostic Step 0 (2026-05-12)

### Changed
- **Setup command Step 0 now platform-agnostic.** Every `request_cowork_directory(...)` call is conditional: "In Cowork, call `request_cowork_directory(...)`. In Claude Code (or any environment with direct filesystem access), no mount is needed." Same plugin source works in both runtimes.

### Why this matters
Phase 0 of SECOND-BRAIN-V2-SPEC. Removes the implicit Cowork-only assumption so Claude Code users do not hit unsupported tool calls during setup.

## [0.2.0] — Config-root refactor

### Changed
- **Plugin config moved to a user-chosen folder.** Reads and writes now go to `<config-root>/plugins/project-setup.user-context.md`, where `<config-root>` is the folder the user chooses on first plugin setup (recorded at `~/Documents/.claude-plugin-config-root`). The old plugin-relative `references/user-context.md` path failed silently under Cowork's read-only mount.
- **`/setup-projects` gets Step 0** — resolves the config root via the pointer; prompts for it on first run; offers to migrate legacy `~/Documents/Claude/identity.md` / `voice.md` and any pre-staged `~/Documents/Claude/plugin-configs/*.user-context.md` files.
- **Operating skills/commands updated** — `/project-setup` reads from the new path.
- **User-facing prompts and skill descriptions debranded** for fork-friendliness.

## [0.1.0] — Initial release

### Added
- End-to-end client engagement initialization slash command (`/project-setup`) producing four outputs in a single response:
  - Drive folder structure (text — user creates manually in their shared drive)
  - Claude Project system prompt (copy-paste ready)
  - Phased project plan with single Immediate Next Step (offers to execute it)
  - Memory node initialization at `~/Documents/Claude/memory/client/[client-name].md` (only if `claude-cortex` is installed)
- User-customizable templates in `references/templates/`:
  - `drive-structure.md` — folder layouts per offering
  - `claude-project-prompt.md` — system-prompt template
  - `project-plans.md` — phased delivery plans per offering
- Starter templates ship with three example offerings (AI Operating Model, Custom Agent Systems, Learning Production System) — replace, remove, or extend per your firm.
- Setup interview captures offerings catalog, drive layout, communication defaults, companion plugin presence.
- Setup reads `~/Documents/Claude/identity.md` (shared identity from cortex) when available.
- Memory node init is conditional on cortex being installed — skipped gracefully otherwise.
