# clients user context (TEMPLATE)

_Run `/setup-projects` to generate your real `references/user-context.md` (gitignored)._

_Last updated: [filled by setup]_

## Identity
- **Name:** [your name]
- **Company:** [company name]
- **What we do:** [one sentence]
- **Role:** [Principal / Partner / Founder / etc.]

## Drive layout
- **Active Clients location:** [e.g., Google Drive → Shared drives → BrightWay AI → Active Clients]
- **Naming convention:** [e.g., "[Client Name] — [Offering Short Name]"]
- **Standard subfolder structure:** [defaults: 00_Scope, 03_Deliverables, 04_Client Assets, 05_Meeting Notes — same four for every client/engagement, no offering-specific variants. One evergreen client folder, dated engagement subfolders underneath.]

## Access zones

_Required. `/project-setup` refuses to run until this section is populated — see `/setup-projects`._

Every output `/project-setup` produces is assigned to one of these zones. Financial
data (dollar amounts, hourly/daily rates, budget caps or not-to-exceed figures, phase
cost estimates, payment terms, invoice/deal amounts, margin, vendor/subcontractor
costs) may never be written into the `project` zone. A zone may be marked "not used"
if you don't separate your Drive that way (not recommended).

- **finance** (restricted — executed contracts, SOW drafts/redlines, amendments,
  invoices, timesheets, rate cards, anything with a price)
  - Shared drive: [name] / [Drive ID]
  - Path pattern: [e.g., `Agreements/Contracts/Invoicing/Timesheets/[Client]/[YYYY-MM Engagement]/`]
  - Expected access: [who should have access — used for audits, e.g., "Zach only"]
- **pipeline** (restricted — proposals and pre-signature material)
  - Shared drive: [name] / [Drive ID]
  - Path pattern: [e.g., `Pipeline/[Client]/`]
  - Expected access: [e.g., "Zach only"]
- **project** (open — scope, plans, deliverables, meeting notes, client assets,
  internal working docs; may be shared with contractors)
  - Shared drive: [name] / [Drive ID]
  - Path pattern: [e.g., `Active Clients/[Client]/`]
  - Expected access: [e.g., "delivery team + contractors on this engagement"]

## Naming conventions

_Required alongside Access zones. Applied to every folder/file `/project-setup` creates or files. `/setup-projects` can infer these from your existing Drive._

- **Client folder name:** [one canonical, evergreen name per client, e.g.,
  "Barker & Scott" — no "and" / "&" / hyphen variants. Never a per-engagement
  folder — engagements are dated subfolders underneath.]
- **Engagement folder pattern:** [e.g., `YYYY-MM [Engagement Name]`, where YYYY-MM
  is the engagement's effective date from the SOW]
- **Executed-contract file pattern:** [e.g., `YYYY-MM-DD [Client] — [Engagement] SOW (Executed).pdf`]
- **Superseded-draft pattern:** [e.g., `_Archive/` subfolder under the engagement folder]
- **Scope Brief file name:** [e.g., `[Client] — [Engagement] Scope Brief`]
- **Date format:** [e.g., `YYYY-MM-DD`]

## Offerings
[Per offering — pulled from interview, also reflected in templates/project-plans.md and templates/drive-structure.md]
- **[Offering Full Name]** ([short name]) — [duration]
  - Phases: [list]
  - Offering-specific questions: [bulleted]
  - Standard deliverables: [named outputs]

## Communication defaults
- **Cadence:** [e.g., "weekly async update + biweekly sync"]
- **Response time:** [e.g., "1 business day"]
- **Communication tools:** [Email / Slack / Teams / etc.]

## Notification recipients

_Used by `/project-setup` for its new-engagement alert drafts. Never hardcoded in
the plugin — captured here on first use and reused after._

- **Finance list:** [names/emails — who gets the new-client/new-engagement alert
  with terms and the executed contract, so they can set the client/engagement up
  in accounting themselves]
- **Delivery-team list:** [names/emails — who gets the scope-and-next-step alert]

## Companion plugins
- **cortex:** [installed / not installed]
- **ops:** [installed / not installed]
- **growth:** [installed / not installed]
