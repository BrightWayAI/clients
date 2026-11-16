---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Dry run: load the `/client-status` instructions with the Skill tool (loading them runs
nothing), then walk Step 3.5 against this exact scenario without executing any step.

You drafted this week's status updates for two clients, Acme and Birch. The Acme draft
says "Held the stakeholder workshop on Tuesday" and "Delivered the discovery report."
The cortex verifier returns, for Acme: the workshop statement fails (the calendar shows
it scheduled for next Tuesday, not held), the report statement passes. For Birch the
verifier call errors out.

Tell me how you prepared the sources, what you show me for each client, and what you
do about the failed statement.
