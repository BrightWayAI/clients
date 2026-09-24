# Drive Folder Structure Template

One evergreen folder per client. Engagements are dated subfolders underneath —
this is what lets a returning client (new phase, new SOW, an amendment) get a new
engagement folder without ever needing a second client folder or a folder-naming
collision.

```
📁 [Client Name]
└── 📁 [YYYY-MM] [Engagement Name]
    ├── 📁 00_Scope
    ├── 📁 03_Deliverables
    ├── 📁 04_Client Assets
    └── 📁 05_Meeting Notes
```

The same four subfolders are stamped into every engagement, for every client,
every time — no offering-specific variants, no per-offering Folder 02, no
`06_Internal Working Docs`. This is the **project zone** structure (see the
user-context `## Access zones` section) — the open, contractor-visible Drive
location. No financial data and no shortcut to the executed contract may be
written here.

**Naming convention:**
- Client folder: `[Client Name]` — one canonical name per client, no "and" / "&" /
  hyphen variants.
- Engagement folder: `[YYYY-MM] [Engagement Name]` — the year-month is the
  engagement's effective date from the SOW, not the filing date. A second
  engagement for the same client is a sibling folder, e.g. `2026-04 Discovery` and
  `2026-10 Phase 2 Build` under the same client folder — never a second client
  folder, and never nested inside the first engagement.

## `00_Scope` — the Scope Brief

`00_Scope` never holds the contract itself, a copy of it, or a shortcut to it — a
Drive shortcut shows the target file's name even to people who can't open it,
which leaks the engagement's existence to anyone with project-zone access. It
holds one generated Google Doc, the **Scope Brief**, built from the executed SOW's
project-safe fields only:

- purpose and objectives
- phases with durations
- deliverables per phase
- client inputs and responsibilities (roles only, not rates)
- how we work together (cadence and tracker)
- out-of-scope items
- the timeline, expressed as calendar dates

It explicitly **excludes**: compensation, IP terms, liability, indemnification, and
termination-payment terms. It carries exactly one line naming where the governing
contract is held (e.g., "Governing contract: filed in Finance — Barker & Scott —
2026-10 Phase 2 Build"), with no link and no amounts. Run the pricing-leak check on
the Scope Brief before writing it — see `commands/project-setup.md` Step 6.3.

## `03_Deliverables`

Name deliverable subfolders after the SOW's actual phases at runtime (e.g.,
"Phase 0 — Knowledge Capture & Setup", "Phase 1A — Marketplace Inventory"), not a
generic template phase name.

## Naming convention notes

- No per-offering variation in this skeleton. If a future offering genuinely needs
  a Drive subfolder beyond the four above, add it explicitly here rather than
  reintroducing an offering-specific branch — keep this evergreen across clients.
- The Claude Project system prompt is **not** part of this structure and is not
  written to Drive — see `commands/project-setup.md`. The client's canonical
  working context lives in cortex as the public project node.
