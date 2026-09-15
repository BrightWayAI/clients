# Changelog

All notable changes to delivery are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/). Versions match `plugin.json`.

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
