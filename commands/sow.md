---
description: Turn a proposal into a finished Statement of Work in your house format, derived from a sample you provided via `/setup-projects`. Flags — `--client <slug>` `--phase <label>` `--amendment` (addendum to an existing SOW/MSA).
---

# /sow [proposal source] [--client <slug>] [--phase <label>] [--amendment]

Input: a proposal (URL, attached file, Drive link, or pasted text).

No visual format is hardcoded in this plugin — everything about how the
output looks comes from `<config-root>/plugins/clients.sow-template.md`,
derived from the user's own sample SOW.

---

## Step 1 — Load the SOW template

Read `<config-root>/plugins/clients.sow-template.md`.

- **Missing** → run the Section 6 flow from `commands/setup-projects.md`
  (capture a sample SOW) before continuing. If the user doesn't have a
  sample handy, confirm they want to proceed with
  `references/sow-format-default.md` (generic styling) and say so plainly in
  the final delivery message.
- **Present** → extract the FORMAT SPEC (JSON block) and SECTION SKELETON for
  use in Steps 5–6.

---

## Step 2 — Pull the proposal

- **Pasted text / attached file** — use directly.
- **Drive link** — read via the Drive connector.
- **Client-portal URL that requires an access code** — use the browser (read
  page text after navigating and authenticating), not `WebFetch`. Portal
  pages are frequently behind auth that a plain fetch can't clear, and
  WebFetch has no way to hold portal session state.
- Get the proposal in full before doing anything else — partial reads produce
  SOWs with missing scope.

---

## Step 3 — Find prior agreements with this client

Search Drive and cortex memory (if installed) for a prior SOW or MSA with
this client. If `--client <slug>` was passed, go straight to
`<config-root>/memory/client/<slug>.md` for context; otherwise resolve the
client from the proposal content first.

- **Found** → treat the new SOW as an **addendum**: inherit defined terms,
  rates, and governing law from the prior document rather than re-deriving
  them. If `--amendment` was passed, structure the whole output as an
  amendment (references the base SOW/MSA by name/date, states only what
  changes) instead of a full SOW.
- **Not found** → this is a first SOW for the client; proceed normally.
- Load the client's cortex node (if it exists) for engagement context —
  contacts, known risks, prior conversations — even if no prior SOW exists.

---

## Step 4 — One round of questions

Ask everything the proposal doesn't already settle, in a single
`AskUserQuestion` round — do not trickle questions one at a time.

Typical gaps:
- **Pricing mechanics** — default for T&M is hourly rate + per-phase
  not-to-exceed caps; alternatives: fixed fee, per-unit, monthly capacity.
  Ask which applies if the proposal doesn't say.
- **Effective Date** — if not stated or implied by the proposal.
- **Open cost allocations** — anything ambiguous in the proposal (e.g., who
  pays production hosting, third-party tool costs, travel).

If the proposal fully answers a question, don't ask it — state the assumption
instead in Step 7's judgment-call summary.

---

## Step 5 — Fill the section skeleton

Using the SECTION SKELETON loaded in Step 1:

- **Engagement-specific sections** (scope, phases, deliverables, timeline,
  pricing, assumptions, open questions, client inputs) — write from the
  proposal's own language. Don't paraphrase into generic consulting-speak;
  preserve the proposal's specific deliverable names and phase structure.
- **Boilerplate sections** (relationship of the parties, reps & warranties,
  indemnification, non-solicit, termination, general provisions) — copy
  verbatim from the sample, adapting only party names and defined terms.
  Do not rewrite boilerplate language — it's there because someone already
  vetted it.

**Pricing conversion:** turn any proposal cost range (e.g., "$74k–$107k")
into a rate table where the top of each phase's range becomes a
not-to-exceed figure, with:
- an 80%-of-cap notice clause ("Vendor will notify Client when billed time
  for a phase reaches 80% of that phase's not-to-exceed amount")
- "Unused budget does not carry between phases" — unless the user said
  otherwise in Step 4.

Use the legal-entity name, governing law, and payment terms from the
template's defaults (or from Step 3's prior agreement, if this is an
addendum) rather than re-asking for them.

---

## Step 6 — Render, review, deliver

1. Build the .docx with `scripts/sow_build.py`, passing the resolved
   `clients.sow-template.md` path as the spec source.
2. Convert to PDF: `soffice --headless --convert-to pdf <file>.docx`.
3. View page 1, a table-bearing page, and the signature page. Fix anything
   that renders off (misaligned columns, wrong header fill, missing footer
   page field) before delivering — don't ship an unreviewed render.
4. Deliver the **.docx** to the user via `SendUserFile` (attach). **Do not**
   push the .docx through the Drive MCP connector — it rejects payloads over
   ~15 KB, which most SOWs exceed; hand the file to the user directly.
5. If a Drive folder for this client exists under the clients Drive layout
   (`references/templates/drive-structure.md`), offer to tell the user where
   to place it: `00_Contract & SOW`. Don't attempt the upload yourself.

---

## Step 7 — Close out

End with 2–3 sentences naming every judgment call made: rate assumptions,
caps chosen, governing law applied, cost allocations resolved without an
explicit answer. Be specific enough that the user can correct any one of
them without re-reading the whole document.

If cortex is installed, append a changelog line to the client's memory node
via `/remember --quick`, e.g.:
`client:<slug> LOG [today] — SOW drafted for [phase/engagement]. Caps: [...]. Governing law: [...].`

---

## Behavior rules

- Never invent format — if `clients.sow-template.md` is missing and the user
  declines to run setup, use `references/sow-format-default.md` and say so
  in the delivery message, not buried in a footnote.
- One round of questions, not a drip. If something genuinely can't be
  resolved without a second round (e.g., the user's first answer creates a
  new ambiguity), that's fine — but don't design the flow to ask twice by
  default.
- Boilerplate is not a place for creativity — copy it, adapt names only.
- `--amendment` changes the document shape (references the base agreement,
  states deltas only) — it is not the same as a low-effort full SOW.
