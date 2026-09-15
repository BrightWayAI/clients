---
description: Draft weekly status updates for active client engagements. Pulls from cortex memory, Client Success engagement data, calendar (this week's meetings), CRM activity, and optionally admin (time-tracking). Produces a draft per client ready for your review and send. Run weekly (Friday afternoon or Monday morning, per your cadence).
---

# /client-status [client?]

Weekly client status update drafting. The plugin reads everything you already have in your stack and writes a draft per active engagement.

---

## Step 0 — Preflight

Read `<config-root>/plugins/clients-status.user-context.md`. If missing, route to `/setup-status` and stop. Read shared identity at `<config-root>/memory/me/identity.md` and shared voice at `<config-root>/memory/me/voice.md`.

Extract from this plugin's user-context:
- Cadence (weekly / bi-weekly / monthly)
- Day-of-week to send
- Status template path (prefer `<config-root>/plugins/clients/templates/status-template.md`; fallback `references/templates/status-template.md`)
- Per-client overrides (length, sections to skip, etc.)
- Delivery channel
- Whether to include time-tracking hours (Y/N — default N)

---

## Step 1 — Identify target clients

If `/client-status [client]` was called with a specific client name → just that one.

Otherwise → all active engagements:
- If Client Success is configured: read `<config-root>/plugins/clients.user-context.md` and active engagements
- If `cortex` is installed: list nodes under `client:` prefix that are Active or Warm (per cortex's freshness markers)
- Else: ask the user "Which clients?" with a free-form list

---

## Step 2 — For each client, gather context

In parallel where possible:

**A. Cortex memory** (if installed)
- Read `<config-root>/memory/client/[client-name].md`
- Extract:
  - Living summary (current state)
  - Changelog entries from the last [cadence period] (typically 7 days)
  - Knowledge entries (insights, lessons, gotchas) committed this period
  - Open threads tagged with [WAITING:Client] or [ASK]
  - P0 / P1 next actions

**B. Client Success engagement data** (if configured)
- Engagement name, current phase, phase goal
- Deliverables completed this period
- Upcoming milestones (next 2 weeks)

**C. Calendar**
- External meetings with this client's domain in attendees, this period
- Capture: date, title, attendees (just first names + roles), brief outcome (if recorded)

**D. CRM**
- Recent notes / activity logged on the contact or deal
- Recent emails sent / received
- Open tasks the user owns related to this client

**E. Time-tracking** (optional, if installed and user-context says include)
- Hours logged for this client this period
- High-level breakdown by category (deep work / meetings / comms)

---

## Step 3 — Draft the status update

Use `references/templates/status-template.md` as the structure. Apply per-client overrides from user-context. Read `<config-root>/memory/me/voice.md` for voice rules. If `voice.md` doesn't exist, don't stop — draft in a generic tone and note in the response: "No voice file found — using generic tone; run comms's `/setup-voice` to fix this."

Default sections (template-defined, user-editable):

**📅 What we did this week**
- 3–5 bullets, lead with verbs ("Completed X," "Held Y interviews," "Drafted Z")
- Bias toward client-visible outputs (not internal prep)

**💡 What we learned**
- 1–3 bullets from cortex knowledge entries (Insights / Lessons most relevant to this client)
- Phrase as "what this means for [Client]" — make it useful, not just observational

**🔭 What's next**
- Upcoming meetings (date + topic)
- Milestones approaching (deliverables, decisions, dependencies)
- 2–3 bullets max — don't overpromise

**🤝 Anything we need from you**
- Blockers, asks, decisions pending — explicit and specific
- If nothing: "All clear on our side this week."

**[Optional] 📚 A relevant share**
- Per user-context, optionally include a relevant article / framework / insight
- One-liner with "thought you'd find this interesting because [specific reason]"

**Signature** — per `<config-root>/memory/me/voice.md` sign-off pattern

---

## Step 4 — Present drafts for review

Present each draft as:

```
**[Client Name] — Status Update for [date]**

[Full draft, ready to copy/edit]

---
```

After all clients, summarize:

```
Drafted [N] status updates. Review each, edit as needed, then send via [channel from user-context].

Want me to:
- Refine any specific update? (say "redo [client]" with what you want different)
- Skip any client? ("skip [client]")
- Include something I missed? ("add [thing] to [client]")
```

---

## Step 5 — (Optional) Mark as sent

Once the user confirms they've sent each update, offer:

> "Mark these as sent in cortex / CRM? Adds a LOG entry to each client memory node and (if CRM connected) a note that a status update was sent."

If yes: add a CHANGELOG entry to each client's memory node ("Sent weekly status update [date]") and (if CRM available) log a note on the contact record.

---

## Step 6 — Person-page side effect (cortex v4.2+)

After the user confirms a status update was sent (or, optionally, when a draft is produced), update the primary contact's person page if it exists.

For each engagement's primary contact (from Client Success's user-context if present, or the most-engaged contact in CRM):

1. Resolve `<config-root>` via the standard pointer.
2. Compute slug: `firstname-lastname`.
3. **If `<config-root>/memory/person/<slug>.md` exists** → append a line to **## Recent interactions**:
   `<today> — status-update-sent — week of <week-start>: <one-line on highlights or theme>` (or `status-update-drafted` if Step 5's send-confirmation was skipped).
   Update **Last meaningful contact** in Relationship. Update Relationship temperature toward Active if it had drifted to Warm/Cold.
4. **If the page does NOT exist** → do nothing. This plugin doesn't graduate new pages.

If cortex isn't installed, skip silently.

---

## Behavior rules

- **Don't auto-send.** Always review-then-send. The plugin drafts; the user delivers.
- **Be specific.** "We continued progress on the engagement" is filler. "Completed 4 stakeholder interviews; synthesized findings into draft Readiness Report" is specific.
- **Honor voice.** Read `<config-root>/memory/me/voice.md` first. If the user's voice is "warm, direct, low-jargon," don't ship a corporate-speak update.
- **Keep it scannable.** Clients skim. Bullets > paragraphs. Lead with verbs.
- **No padding.** If a client had a quiet week, the update should be short. "Nothing major to report; we're on track for [next milestone]" is honest and respectful of the client's time.
- **Don't overpromise in "What's next."** Use language from Client Success phase plans, not aspirational stretch goals.

## Edge cases

- **Client has no recent activity** — can be intentional (between phases, on hold). Generate a shorter "we're between phases; here's what's next" update or recommend skipping the week.
- **Multiple stakeholders per client** — draft one update; let the user CC additional contacts at send time.
- **Cortex memory thin for a client** — use whatever's there; recommend committing more during the week (or running `/end-day` to capture more).
- **Sensitive content** — don't surface anything from memory tagged as `[INTERNAL]` or `[CONFIDENTIAL]` — the update goes to the client, not internal team.

## What this is NOT for

- **Quarterly business reviews / formal QBRs** — those are bigger artifacts. Use this for weekly cadence touches.
- **One-off updates** — for a specific milestone hit or scope change, draft it directly with Client Success and keep it review-only.
- **Internal status reports** — this is for client-facing updates only.
