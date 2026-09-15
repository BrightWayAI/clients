---
description: Run a structured QA pass on a client deliverable (deck, doc, spreadsheet, one-pager) against your brand guide and the original brief. Returns specific issues with locations and suggested fixes — not a vague "looks good." Loads brand context from references/user-context.md.
---

# /review-deliverable [path-or-url]

Structured review of a client-facing deliverable before you ship it.

This is a slash command, not a subagent — the review runs inline in your conversation so you can ask follow-up questions and iterate on the findings without losing context.

---

## Step 1 — Load brand context

Read `<config-root>/plugins/core-ops.user-context.md` from the core-ops plugin directory. Extract:

- Brand colors, typography, voice/tone rules, banned phrases
- Path to the canonical brand guide (PDF, Drive doc, Notion page, etc.)
- Any deliverable-type-specific rules (e.g., "decks always include the four-bar agenda on slide 2")

If `user-context.md` is missing or contains the placeholder, tell the user to run `/setup-core` and stop.

---

## Step 2 — Load the deliverable

Accept input as:

- **Local file path** — `/path/to/deck.pptx`, `/path/to/doc.docx`, `/path/to/sheet.xlsx`, `/path/to/page.pdf`, `/path/to/file.md`
- **Drive URL** — Google Drive shareable link (read via the Drive connector)
- **Markdown / text inline** — if the user pastes content directly

For binary files (.pptx, .xlsx, .docx, .pdf), use whichever skill the user has available to parse (the Anthropic skills `pptx`, `xlsx`, `docx`, `pdf` are the canonical paths). If parsing isn't available for the file type, tell the user and stop.

If the deliverable is over 50 pages or 10MB, ask the user to scope the review (specific pages/sections) rather than reviewing all of it.

---

## Step 3 — Ask for the brief (if not provided)

Before reviewing, you need to know what the deliverable is *for*. If the user hasn't included it, ask once:

> "Quick: what's the brief or context for this? (One paragraph is fine — what's the client trying to accomplish, who's the audience, what should the reader walk away with.)"

If the user says "skip it, just review the work," proceed but note in the review that brief-fit couldn't be assessed.

---

## Step 4 — Run the review

Cover four axes. Be specific — "Slide 4, second bullet" not "the bullets feel weak."

### A. Brief Fit

Does the deliverable answer the brief? Are the audience and the takeaway clear from a quick scan? Is anything missing that the brief implies should be there?

### B. Brand Compliance

Compare against the brand context loaded in Step 1. Flag specific deviations — wrong color codes, off-brand fonts, banned phrases, voice mismatch. Reference the brand guide rules by name when possible (e.g., "Voice rule #3 — avoid 'leverage' as a verb").

### C. Quality Issues (ranked by severity)

Hunt for:
- **Logic gaps** — claims without support, arguments that don't flow
- **Visual issues** — overcrowded slides, inconsistent formatting, misaligned tables, low-contrast text
- **Copy issues** — typos, awkward phrasing, jargon, passive voice in places where active is stronger
- **Data issues** — numbers that don't add up, charts mislabeled, units missing

Order by severity (must-fix → nice-to-fix). For each: location, issue, suggested fix.

### D. What's Working

2–3 things genuinely worth keeping. Not flattery — concrete strengths the user should preserve in revisions.

---

## Step 5 — Verdict

End with a clear ship/no-ship call.

```
## Brief Fit
[Pass | Concerns | Fail] — [reasoning]

## Brand Compliance
[Pass | Concerns | Fail] — [specific findings, with brand-guide references]

## Quality Issues (ranked by severity)
1. **[Location]** — [issue] — *Fix:* [suggested fix]
2. ...

## What's Working
- [strength 1]
- [strength 2]
- [strength 3]

## Ready to Ship?
**[Yes | No | With fixes]** — [if "with fixes," list the minimum bar to ship]
```

---

## Behavior rules

- **Be specific.** Locations, line numbers, slide numbers, cell addresses. Vague feedback is failure.
- **Reference the brand guide by name** when flagging brand issues. "Doesn't match brand" is unhelpful; "Heading uses Inter Bold; brand spec is Sora Semibold (page 4 of brand guide)" is helpful.
- **Severity discipline.** A typo and a missing slide are not the same severity. Order matters.
- **No padding.** If there's nothing to flag in a section, say so. Don't manufacture issues to look thorough.
- **Stay in your lane.** This is QA, not strategy. Don't second-guess the user's strategic decisions in the deliverable — only flag if a strategic claim contradicts the brief.
- **Iterate.** After the first review pass, the user may ask follow-ups ("rewrite the third bullet," "give me three options for slide 6 title"). Engage — that's why this is a slash command and not a subagent.
